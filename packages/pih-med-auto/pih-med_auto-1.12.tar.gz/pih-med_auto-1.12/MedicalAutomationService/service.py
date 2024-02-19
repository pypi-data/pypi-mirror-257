import time
import shutil
import locale
from typing import Any

import ipih

from pih import A
from pih.collections import PolibaseDocument
from MedicalAutomationService.const import SD
from MobileHelperService.client import Client as MIO
from pih.tools import j, js, one, while_not_do, nn, n
from MobileHelperService.const import COMMAND_KEYWORDS
from MobileHelperService.api import MobileOutput, mio_command
from pih.consts.errors import OperationExit, OperationCanceled


# version 0.982
SC = A.CT_SC

ISOLATED: bool = False

target_GROUP: A.CT_ME_WH.GROUP = A.CT_ME_WH.GROUP.SCANNED_DOCUMENT_HELPER_CLI
target: MobileOutput = MIO.create_output(target_GROUP)


def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD, as_standalone=as_standalone):

        from pih.tools import ParameterList
        from pih.collections import User, ActionWasDone
        from pih.collections.service import SubscribtionResult

        def service_call_handler(
            sc: SC,
            parameter_list: ParameterList,
            subscribtion_result: SubscribtionResult | None,
        ) -> Any:
            if sc == SC.heart_beat:
                if (A.SE.life_time.seconds / 60) % 2 == 0:
                    A.SYS.start_windows_service_if_stopped(
                        A.CT_WINDOWS.SERVICES.WIA, A.CT_H.WS816.NAME
                    )
                return
            if sc == SC.send_event:
                if subscribtion_result.result:
                    event: A.CT_E | None = None
                    event_parameters: list[Any] | None = None
                    event, event_parameters = A.D_Ex_E.with_parameters(parameter_list)

                    if event == A.E_B.action_was_done():
                        action_data: ActionWasDone = A.D_Ex_E.action(event_parameters)
                        action: A.CT_ACT = action_data.action
                        if action == A.CT_ACT.VALENTA_SYNCHRONIZATION:
                            A.SYS.start_windows_service_if_stopped(
                                A.CT_WINDOWS.SERVICES.WIA, A.CT_H.WS816.NAME
                            )
                            scanned_file_path_list: list[str] = (
                                A.PTH.get_file_list_by_directory_info(
                                    A.PTH.WS_816_SCAN.VALUE
                                )
                            )
                            scanned_file_list_length: int = len(scanned_file_path_list)
                            user: User = A.R_U.by_login(action_data.user_login).data
                            user_output: MobileOutput = MIO.create_output(
                                user.telephoneNumber
                            )
                            forced: bool = action_data.forced
                            new_document_is_present: bool = scanned_file_list_length > 0
                            if new_document_is_present or forced:
                                with user_output.personalized():
                                    if new_document_is_present:
                                        user_output.write_line(
                                            js(
                                                (
                                                    "Cинхронизация Валенты: найдены новые исследования в количестве:",
                                                    scanned_file_list_length,
                                                    ".",
                                                )
                                            )
                                        )
                                    else:
                                        user_output.write_line(
                                            "Принудительная синхронизация Валенты."
                                        )
                                    user_output.write_line(
                                        "Начат процесс синхронизации Валенты: закрытие программы Валента на компьютерах."
                                    )
                                    close_valenta_clients()
                                    user_output.write_line(
                                        "Идёт процесс синхронизации Валенты: начато копирование файлов."
                                    )
                                    synchronize_valenta_files()
                                    user_output.write_line(
                                        "Завершён процесс синхронизации Валенты."
                                    )
                                    doctor_user: User = one(
                                        A.R_U.by_group(
                                            A.CT_AD.Groups.FunctionalDiagnostics
                                        )
                                    )
                                    doctor_output: MobileOutput = MIO.create_output(
                                        doctor_user.telephoneNumber
                                    )
                                    for scanned_file_path in scanned_file_path_list:
                                        doctor_output.write_line(
                                            js(
                                                (
                                                    "День добрый,",
                                                    j(
                                                        (
                                                            doctor_output.user.get_formatted_given_name(),
                                                            ".",
                                                        )
                                                    ),
                                                    "Новое исследование",
                                                )
                                            )
                                        )
                                        while_not_do(
                                            check_action=lambda: doctor_output.write_image(
                                                "Журнал пациента",
                                                A.D_CO.file_to_base64(
                                                    scanned_file_path
                                                ),
                                            ),
                                            success_handler=lambda: A.E.new_polibase_scanned_document_processed(
                                                scanned_file_path
                                            ),
                                        )
                                    A.A_PTH.listen(A.PTH.WS_816_SCAN.VALUE)
                        return
                    if event == A.CT_E.NEW_FILE_DETECTED:
                        path: str = A.PTH.path(event_parameters[0])
                        if path.startswith(A.PTH.path(A.PTH.SCAN_TEST.VALUE)):
                            pass
                        elif path.startswith(A.PTH.path(A.PTH.WS_816_SCAN.VALUE)):
                            A.L.polibase_document(
                                js(("Кандидат на документ Полибейс:", path)),
                                image_path=path,
                            )
                            polibase_document: PolibaseDocument | None = one(
                                A.R_RCG.polibase_document(path)
                            )
                            if n(polibase_document):
                                while True:
                                    try:
                                        polibase_document = A.D.fill_data_from_source(
                                            PolibaseDocument(),
                                            MIO.waiting_for_result(
                                                js(
                                                    (
                                                        mio_command(
                                                            COMMAND_KEYWORDS.CHECK
                                                        ),
                                                        mio_command(
                                                            COMMAND_KEYWORDS.SCAN
                                                        ),
                                                    )
                                                ),
                                                A.CT_ME_WH.GROUP.PIH_CLI,
                                                target_GROUP,
                                                args=(path,),
                                            ),
                                        )

                                    except OperationCanceled as _:
                                        target.good("Это не документ Полибейс")
                                        return
                                    except OperationExit as _:
                                        target.error("Нельзя отменить")
                                        continue
                                    if nn(polibase_document):
                                        break
                            A.E.new_polibase_scanned_document_detected(
                                polibase_document
                            )
                            polibase_person_pin: int = (
                                polibase_document.polibase_person_pin
                            )
                            document_name: A.CT_P_DT = A.D.get(
                                A.CT_P_DT, polibase_document.document_type
                            )
                            if document_name in [
                                A.CT_P_DT.HOLTER_JOURNAL,
                                A.CT_P_DT.ABPM_JOURNAL,
                            ]:
                                is_holter: bool = (
                                    document_name == A.CT_P_DT.HOLTER_JOURNAL
                                )
                                file_name: str = A.PTH.get_file_name(path)
                                test: bool = file_name.startswith(A.CT.TEST.NAME)
                                only_notify: bool = file_name.startswith("-")
                                path_destination: str = A.PTH.join(
                                    A.PTH.POLIBASE.person_folder(polibase_person_pin),
                                    A.PTH.add_extension(
                                        (
                                            "holter_journal"
                                            if is_holter
                                            else "abpm_journal"
                                        ),
                                        A.PTH.get_extension(path),
                                    ),
                                )
                                if not (test or only_notify):
                                    close_valenta_clients()
                                    synchronize_valenta_files()
                                doctor_user: User = A.R_U.by_login(
                                    A.CT.TEST.USER
                                    if test
                                    else one(
                                        A.R_U.by_group(
                                            A.CT_AD.Groups.FunctionalDiagnostics
                                        )
                                    ).samAccountName
                                ).data
                                doctor_output: MobileOutput = MIO.create_output(
                                    doctor_user.telephoneNumber
                                )
                                patient_name: str = A.R_P.person_by_pin(
                                    polibase_person_pin
                                ).data.FullName
                                doctor_output.write_line(
                                    j(
                                        (
                                            "День добрый, ",
                                            doctor_output.user.get_formatted_given_name(),
                                            ". Новое исследование - монитор ",
                                            (
                                                "Холтера"
                                                if is_holter
                                                else "артериального давления"
                                            ),
                                            ": ",
                                            patient_name,
                                            ".",
                                        )
                                    )
                                )
                                while_not_do(
                                    check_action=lambda: doctor_output.write_image(
                                        "Журнал пациента",
                                        A.D_CO.file_to_base64(path),
                                    ),
                                    success_handler=lambda: A.E.new_polibase_scanned_document_processed(
                                        path
                                    ),
                                )
                                if not (test or only_notify):
                                    A.ME_WS.by_workstation_name(
                                        A.CT.HOST.WS816.NAME,
                                        js(
                                            (
                                                "Журнал пациента",
                                                patient_name,
                                                "отсканирован. Спасибо!",
                                            )
                                        ),
                                    )
                                    shutil.copy(path, path_destination)
                                target.write_image(
                                    j(
                                        (
                                            "Документ отправлен доктору: ",
                                            doctor_user.name,
                                            " (",
                                            A.D_F.whatsapp_send_message_to(
                                                doctor_user.telephoneNumber,
                                                js(
                                                    (
                                                        "День добрый,",
                                                        A.D.to_given_name(
                                                            doctor_user.name
                                                        ),
                                                    )
                                                ),
                                            ),
                                            ")",
                                        )
                                    ),
                                    A.D_CO.file_to_base64(path),
                                )
                                A.L.polibase_document(
                                    js(("Отправленный документ Полибейс:", path))
                                )
            return True

        def close_valenta_clients() -> None:
            for host_name in [A.CT.HOST.WS816.NAME, A.CT.HOST.WS255.NAME]:
                A.A_WS.kill_process(A.CT.VALENTA.PROCESS_NAME, host_name)

        def synchronize_valenta_files() -> None:
            robocopy_job_name: str = A.CT.VALENTA.NAME
            while True:
                A.A_B.start_robocopy_job_by_name(robocopy_job_name, force=True)
                if A.E.on_robocopy_job_complete(robocopy_job_name):
                    break
                else:
                    time.sleep(2)
                    close_valenta_clients()

        def service_starts_handler() -> None:
            locale.setlocale(locale.LC_ALL, "ru_RU")
            A.SRV_A.subscribe_on(SC.heart_beat)
            A.SRV_A.subscribe_on(SC.send_event)
            A.A_PTH.listen(A.PTH.path(A.PTH.WS_816_SCAN.VALUE))
            if not A.C_WS.accessibility(A.PTH.WS_816_SCAN.HOST):
                A.L.it_bot(
                    j(
                        (
                            "При попытке прослушать папку: ",
                            A.PTH.path(A.PTH.WS_816_SCAN.VALUE),
                            ", определено, что компьютер ",
                            A.PTH.WS_816_SCAN.HOST,
                            " не доступен.",
                        )
                    ),
                    A.CT_L_ME_F.ERROR,
                )
            A.A_PTH.listen(A.PTH.path(A.PTH.SCAN_TEST.VALUE))

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
