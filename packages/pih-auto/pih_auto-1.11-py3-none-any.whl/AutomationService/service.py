import shutil
import locale
import calendar
import requests
from typing import Any
from datetime import timedelta
from collections import defaultdict

import ipih

from pih import A, PIHThread
from pih.collections import Mark
from pih.consts.errors import NotFound
from pih.tools import j, b, js, n, nn, e, ne, one, BitMask as BM

from AutomationService.const import *
from MobileHelperService.client import Client as MIO
from MobileHelperService.api import MobileOutput, mio_command
from AutomationService.api import TimeTrackingReportConfiguration
from MobileHelperService.collection import MobileHelperUserSettings
from MobileHelperService.const import (
    COMMAND_KEYWORDS,
    FLAG_KEYWORDS,
    Flags,
)

# version 0.982
SC = A.CT_SC

ISOLATED: bool = False

def start(as_standalone: bool = False) -> None:
    from pih.tools import ParameterList
    from datetime import datetime
    from pih.collections import (
        ResourceStatus,
        ChillerIndicationsValueContainer,
        ActionWasDone,
        PersonDivision,
        CTIndicationsValueContainer,
        WhatsAppMessage,
        User,
        NewMailMessage,
        Result,
        CTIndicationsValue,
        EmailInformation,
        PolibasePerson,
    )
    from pih.collections.service import SubscribtionResult

    time_attack_report_configuration_map: dict[str, TimeTrackingReportConfiguration] = {
        "kag": TimeTrackingReportConfiguration(
            tab_number_list=lambda: A.S.get(A.CT_S.TIME_TRACKING_FOR_POLYCLINIC),
            division_id=one(
                A.R_M.by_name(A.R_U.by_login(USER_LOGIN.CHIEF_DOCTOR).data.name)
            ).DivisionID,
        ),
        "rvg": TimeTrackingReportConfiguration(
            tab_number_list=["022-0-", "163", "190"]
        ),
        "kes": TimeTrackingReportConfiguration(
            tab_number_filter_function=lambda item: item.GroupName.lower().find("олд")
            != -1,
            addition_tab_number_list=["174-0-"],
            folder_name="ОЛД",
        ),
        USER_LOGIN.LABARATORY_HEAD: TimeTrackingReportConfiguration(
            tab_number_filter_function=lambda item: item.GroupName.lower().find(
                "лабаратория"
            )
            != -1,
            division_id=2,
            addition_tab_number_list=lambda: [
                one(
                    A.R_M.by_name(A.D_U.by_login(USER_LOGIN.LABARATORY_HEAD).name)
                ).TabNumber
            ],
            folder_name="КЛД",
        ),
        USER_LOGIN.SERVICE_CONTROL_HEAD: TimeTrackingReportConfiguration(
            addition_tab_number_list=lambda: [
                one(A.R_M.by_name("Пятикопов")).TabNumber
            ],
            division_id=1,
        ),
        "eak": TimeTrackingReportConfiguration(additional_division_id=6),
        "mnb": TimeTrackingReportConfiguration(
            tab_number_filter_function=lambda item: A.D.equal(
                item.GroupName, "рег.касса.кт"
            )
            or A.D.equal(item.GroupName, "Деж менеджер")
        ),
        "vvs": TimeTrackingReportConfiguration(),
    }

    class DH:
        resource_problem_status_map: dict[str, ProblemState] = defaultdict(str)
        hr_user: str | None = None

    def get_resource_status_address(resource_status: ResourceStatus) -> str:
        resource_status_address: str = resource_status.address
        address_list: list[str] = [
            A.CT_R_D.VPN_PACS_SPB.address,
            A.CT_R_D.PACS_SPB.address,
        ]
        if resource_status.address in address_list:
            resource_status_address = address_list[0]
        return resource_status_address

    def get_problem_state(resource_status: ResourceStatus) -> ProblemState:
        return DH.resource_problem_status_map[
            get_resource_status_address(resource_status)
        ]

    def set_problem_state(resource_status: ResourceStatus, value: ProblemState) -> None:
        DH.resource_problem_status_map[get_resource_status_address(resource_status)] = (
            value
        )

    def service_call_handler(
        sc: SC,
        parameter_list: ParameterList,
        subscribtion_result: SubscribtionResult | None,
    ) -> Any:
        if sc == SC.heart_beat:
            current_datetime: datetime = A.D_Ex.parameter_list(parameter_list).get()
            PIHThread(
                lambda: A.R_F.execute(
                    "@on_heart_beat", {"current_datetime": current_datetime}
                )
            )
            if A.C_IND.ct_notification_start_time(current_datetime):
                send_ct_indications()
            if current_datetime.minute == 0:
                A.A_D.create_statistics_chart(A.CT_STAT.Types.CT)
            if A.C_S.by_time(current_datetime, A.CT_S.HOSPITAL_WORK_DAY_START_TIME):
                A.A_D.create_statistics_chart(A.CT_STAT.Types.CHILLER_FILTER)
                A.A_ACT.was_done(A.CT_ACT.TIME_TRACKING_REPORT)
            if (A.SE.life_time.seconds / 60) % 2 == 0:
                A.SYS.start_windows_service_if_stopped(
                    A.CT_WINDOWS.SERVICES.WIA, A.CT_H.WS816.NAME
                )
            return
        if sc == SC.register_chiller_indications_value:
            result: dict[str, Any] | None = subscribtion_result.result
            if ne(result):
                if A.C_IND.chiller_on():
                    indications_value_container: ChillerIndicationsValueContainer = (
                        A.D.fill_data_from_source(
                            ChillerIndicationsValueContainer(), result
                        )
                    )
                    shutil.copy(
                        A.PTH_IND.CHILLER_DATA_IMAGE_LAST_RESULT,
                        A.PTH_IND.CHILLER_DATA_IMAGE_RESULT(
                            A.PTH.replace_prohibited_symbols_from_path_with_symbol(
                                A.D_F.datetime(indications_value_container.timestamp)
                            ),
                            indications_value_container.temperature,
                            indications_value_container.indicators,
                        ),
                    )
            return
        if sc == SC.send_event:
            if subscribtion_result.result:
                event: A.CT_E | None = None
                event_parameters: list[Any] | None = None
                event, event_parameters = A.D_Ex_E.with_parameters(parameter_list)
                PIHThread(
                    lambda event_and_parameters: A.R_F.execute(
                        "@on_event", event_and_parameters
                    ),
                    args=({"event": event, "event_parameters": event_parameters},),
                )
                if event == A.CT_E.WHATSAPP_MESSAGE_RECEIVED:
                    message: WhatsAppMessage = A.D_Ex_E.whatsapp_message(parameter_list)
                    if nn(message):
                        if message.chatId == A.D.get(
                            A.CT_ME_WH.GROUP.CONTROL_SERVICE_INDICATIONS
                        ):
                            send_all_indications()
                            return
                        if message.chatId == A.D.get(A.CT_ME_WH.GROUP.CT_INDICATIONS):
                            send_ct_indications()
                            return
                if event in [A.CT_E.RESOURCE_ACCESSABLE, A.CT_E.RESOURCE_INACCESSABLE]:
                    resource_status: ResourceStatus = A.D.fill_data_from_source(
                        ResourceStatus(), event_parameters[1]
                    )
                    if event == A.CT_E.RESOURCE_ACCESSABLE:
                        set_problem_state(resource_status, ProblemState.FIXED)
                    else:
                        reason_value: str | None = event_parameters[4]
                        reason: A.CT_R_IR | None = (
                            None
                            if e(reason_value)
                            else A.D.get(
                                A.CT_R_IR, event_parameters[4], return_value=False
                            )
                        )
                        if (
                            get_problem_state(resource_status)
                            == ProblemState.WAIT_FOR_FIX_RESULT
                        ):
                            set_problem_state(resource_status, ProblemState.NOT_FIXED)
                        if get_problem_state(resource_status) != ProblemState.AT_FIX:
                            resource_status_address: str = get_resource_status_address(
                                resource_status
                            )
                            if resource_status_address in [
                                A.CT_ADDR.SITE_ADDRESS,
                                A.CT_ADDR.EMAIL_SERVER_ADDRESS,
                                A.CT_ADDR.API_SITE_ADDRESS,
                            ]:
                                if reason == A.CT_R_IR.CERTIFICATE_ERROR:
                                    set_problem_state(
                                        resource_status, ProblemState.AT_FIX
                                    )
                                    for command in [
                                        "certbot renew",
                                        "service postfix restart",
                                        "service nginx restart",
                                        "service dovecot restart",
                                    ]:
                                        A.R_SSH.execute(
                                            command, resource_status.address
                                        )
                            if resource_status_address == A.CT_R_D.VPN_PACS_SPB.address:
                                openVPN_folder: str = "C:\\Program Files\\OpenVPN"
                                set_problem_state(resource_status, ProblemState.AT_FIX)
                                A.EXC.kill_process("openvpn", A.CT.HOST.WS255.NAME)
                                A.EXC.execute(
                                    A.EXC.create_command_for_psexec(
                                        (
                                            A.PTH.join(
                                                openVPN_folder, "bin", "openvpn"
                                            ),
                                            "--config",
                                            A.PTH.join(
                                                openVPN_folder, "config", "cmrt.ovpn"
                                            ),
                                            "--auth-user-pass",
                                            A.PTH.join(
                                                openVPN_folder, "config", "auth.txt"
                                            ),
                                        ),
                                        A.CT.HOST.WS255.NAME,
                                    ),
                                    True,
                                )
                            set_problem_state(
                                resource_status, ProblemState.WAIT_FOR_FIX_RESULT
                            )
                    return
                if event == A.CT_E.NEW_EMAIL_MESSAGE_WAS_RECEIVED:
                    mail_message: NewMailMessage = A.D_Ex.new_mail_message(
                        event_parameters[3]
                    )
                    if n(DH.hr_user):
                        DH.hr_user = one(A.R_U.by_job_position(A.CT_AD.JobPositions.HR))
                    if mail_message.from_ in [DH.hr_user.mail, A.CT.TEST.EMAIL_ADDRESS]:
                        subject: str = mail_message.subject.lower()
                        if (
                            subject.find("т/у") != -1
                            or subject.find("трудоустройство") != -1
                        ):
                            recipient: str = A.D.get(A.CT_ME_WH.GROUP.PIH_CLI)
                            mobile_output: MobileOutput = MIO.create_output(recipient)
                            mobile_output.write_line(
                                j(
                                    (
                                        "Получено новое сообщение об трудоустройстве от ",
                                        b("Отдела кадров"),
                                        " (",
                                        DH.hr_user.name,
                                        ")",
                                    )
                                )
                            )
                            with mobile_output.make_separated_lines():
                                for line in A.D.not_empty_items(
                                    mail_message.text.splitlines()
                                ):
                                    text_list: list[str] = line.split(":")
                                    has_separator: bool = len(text_list) > 1
                                    title: str = (
                                        text_list[0].strip() if has_separator else line
                                    )
                                    text: str | None = (
                                        text_list[1].strip() if has_separator else None
                                    )
                                    mobile_output.write_line(b(title))
                                    if ne(text):
                                        mobile_output.write_line(text)
                            A.A_MIO.send_command_to(
                                js(
                                    (
                                        mio_command(COMMAND_KEYWORDS.CREATE),
                                        mio_command(COMMAND_KEYWORDS.USER),
                                    )
                                ),
                                recipient,
                                recipient,
                            )
                    return
                if event in (A.CT_E.EMPLOYEE_CHECKED_IN, A.CT_E.EMPLOYEE_CHECKED_OUT):
                    checked_in: bool = event == A.CT_E.EMPLOYEE_CHECKED_IN
                    try:
                        name: str = event_parameters[0]
                        user: User = one(A.D_U.by_name(name))
                        telephone_number: str | None = A.D_F.telephone_number(
                            user.telephoneNumber
                        )
                        if e(telephone_number) or not A.C.telephone_number(
                            telephone_number
                        ):
                            A.L.debug(
                                js(
                                    (
                                        "Пользователь",
                                        user.samAccountName,
                                        "имеет плохой номер",
                                    )
                                )
                            )
                        else:
                            mobile_helper_user_settings: MobileHelperUserSettings = (
                                MIO.SETTINGS.USER.get(user.samAccountName)
                            )
                            mobile_helper_user_flags: int = (
                                mobile_helper_user_settings.flags
                            )
                            if not BM.has(
                                mobile_helper_user_flags,
                                A.CT_AD_UP.TimeTrackingless,
                            ):
                                A.A_MIO.write(
                                    telephone_number,
                                    j(
                                        (
                                            (
                                                "Добро пожаловать,"
                                                if checked_in
                                                else "До свидания,"
                                            ),
                                            " ",
                                            b(A.D.to_given_name(name)),
                                            ". Вы отметились на ",
                                            "вход" if checked_in else "выход",
                                            ".",
                                        )
                                    ),
                                    A.CT_ME_WH_W.Profiles.IT,
                                )
                                if not (
                                    BM.has(
                                        mobile_helper_user_flags,
                                        A.CT_AD_UP.Jokeless,
                                    )
                                    or A.C_U.has_property(
                                        user,
                                        A.CT_AD_UP.Jokeless,
                                    )
                                ):
                                    A.A_MIO.write(
                                        telephone_number,
                                        "Вот Вам анекдот:",
                                        A.CT_ME_WH_W.Profiles.IT,
                                    )
                                    A.A_MIO.send_command_to(
                                        mio_command(COMMAND_KEYWORDS.JOKE),
                                        telephone_number,
                                        flags=BM.value(Flags.ONLY_RESULT),
                                    )

                        PIHThread(
                            lambda: A.R_F.execute(
                                "@on_employee_checked_event",
                                {"user": user, "checked_in": checked_in},
                            )
                        )
                    except NotFound as _:
                        pass
                    return

                if event == A.E_B.chiller_temperature_alert_was_fired():
                    send_message_to_control_service(
                        j(
                            (
                                "ВНИМАНИЕ: превышена температруа чиллера (",
                                A.S.get(A.CT_S.CHILLER_ALERT_TEMPERATURE),
                                A.CT_V.TEMPERATURE_SYMBOL,
                                ")",
                            )
                        ),
                        True,
                    )
                    return
                if event == A.E_B.polibase_person_email_was_added():
                    email_information: EmailInformation = A.D.fill_data_from_source(
                        EmailInformation(),
                        A.E.get_parameter(event, event_parameters),
                    )
                    polibase_person: PolibasePerson = A.R_P.person_by_pin(
                        email_information.person_pin
                    ).data
                    params: dict[str, str] = {
                        "format": "json",
                        "api_key": "65ddrin3zh791hxarbkwe4fmah5p44hkg4cjwsuy",
                        "list_ids": "407",
                        "fields[email]": polibase_person.email,
                        "fields[Name]": polibase_person.FullName,
                        "tags": "Polibase",
                    }
                    requests.get(
                        "https://api.unisender.com/ru/api/subscribe",
                        verify=False,
                        params=params,
                    )

                if event == A.E_B.action_was_done():
                    action_data: ActionWasDone = A.D_Ex_E.action(event_parameters)
                    action: A.CT_ACT = action_data.action
                    action_parameters: list = action_data.parameters
                    PIHThread(
                        lambda: A.R_F.execute(
                            "@on_action",
                            {"action": action, "action_data": action_data},
                        )
                    )
                    if action == A.CT_ACT.ACTION:
                        pass
                    if action in (A.CT_ACT.DOOR_OPEN, A.CT_ACT.DOOR_CLOSE):
                        return A.A_M.door_operation(
                            action_parameters[0],
                            "open" if action == A.CT_ACT.DOOR_OPEN else "close",
                        )
                    if action == A.CT_ACT.TIME_TRACKING_REPORT:
                        for (
                            watcher_user_login
                        ) in time_attack_report_configuration_map.keys():
                            time_tracking_report_configuration: (
                                TimeTrackingReportConfiguration
                            ) = time_attack_report_configuration_map[watcher_user_login]
                            division_id: int | None = (
                                time_tracking_report_configuration.division_id
                            )
                            division_name: str | None = None
                            if nn(division_id):
                                division: PersonDivision = one(
                                    A.R.filter(
                                        lambda division: division.id == division_id,
                                        A.R_M.person_divisions(),
                                    )
                                )
                                division_name = division.name
                            else:
                                mark: Mark = one(
                                    A.R_M.by_full_name(
                                        A.R_U.by_login(watcher_user_login).data.name
                                    )
                                )
                                division_id = mark.DivisionID
                                division_name = mark.DivisionName

                            report_folder_path: str = A.PTH.join(
                                A.PTH.SHARE.PATH,
                                "0.2 Отметки Ориона",
                                time_tracking_report_configuration.folder_name
                                or division_name,
                            )
                            A.PTH.make_directory_if_not_exists(report_folder_path)
                            tab_number_list: list[str] | None = A.D.as_value(
                                time_tracking_report_configuration.tab_number_list
                            )
                            if e(tab_number_list):
                                tab_number_list = A.D.filter(
                                    lambda tab_number: ne(tab_number),
                                    A.R.map(
                                        lambda item: item.TabNumber,
                                        A.R.filter(
                                            lambda item: A.D.check(
                                                n(
                                                    time_tracking_report_configuration.tab_number_filter_function
                                                ),
                                                True,
                                                lambda: time_tracking_report_configuration.tab_number_filter_function(
                                                    item
                                                ),
                                            ),
                                            A.R_M.by_division(division_id),
                                        ),
                                    ).data,
                                )
                            if ne(
                                time_tracking_report_configuration.additional_division_id
                            ):
                                tab_number_list += A.D.map(
                                    lambda mark: mark.TabNumber,
                                    A.R_M.by_division(
                                        time_tracking_report_configuration.additional_division_id
                                    ).data,
                                )
                            if ne(
                                time_tracking_report_configuration.addition_tab_number_list
                            ):
                                tab_number_list += A.D.as_value(
                                    time_tracking_report_configuration.addition_tab_number_list
                                )

                            now: datetime | None = None
                            for now in [
                                (
                                    (A.D.now() - timedelta(days=1))
                                    if A.D.now().day == 1
                                    else None
                                ),
                                A.D.now(),
                            ]:
                                if nn(now):
                                    A.A_TT.save_report(
                                        A.PTH.add_extension(
                                            A.PTH.join(
                                                report_folder_path,
                                                calendar.month_name[now.month],
                                            ),
                                            A.CT_F_E.EXCEL_NEW,
                                        ),
                                        now.replace(day=1),
                                        now,
                                        tab_number_list,
                                    )
                    if action == A.CT_ACT.ATTACH_SHARED_DISKS:
                        output: str = str(
                            A.EXC.execute(
                                A.EXC.create_command_for_psexec(
                                    (
                                        A.CT.POWERSHELL.NAME,
                                        BACKUP_COMMANDS.ATTACH_SHARED_DISKS.PATH(),
                                    ),
                                    A.CT_H.BACKUP_WORKER.NAME,
                                    interactive=None,
                                    run_from_system_account=True,
                                ),
                                True,
                                True,
                            ).stdout
                        )
                        return output.strip().count("Attached          : True") == 2
                    if action == A.CT_ACT.SWITCH_TO_INTERNAL_WATER_SOURCE:
                        send_message_to_control_service(
                            "УВЕДОМЛЕНИЕ: переход на внутреннее водоснабжение"
                        )
                    if action == A.CT_ACT.SWITCH_TO_EXTERNAL_WATER_SOURCE:
                        send_message_to_control_service(
                            "УВЕДОМЛЕНИЕ: переход на городское водоснабжение"
                        )
                    if action == A.CT_ACT.CHILLER_FILTER_CHANGING:
                        A.D_MR.add_count(A.CT_MR.TYPES.CHILLER_FILTER, -1)
                        A.A_D.create_statistics_chart(A.CT_STAT.Types.CHILLER_FILTER)
                    return
        return True

    def send_message_to_control_service(
        value: str, on_workstation: bool = False
    ) -> None:
        if on_workstation:
            A.ME_WS.by_login(A.CT_AD_U.CONTROL_SERVICE, value, 60 * 60 * 24)
        MIO.create_output(A.CT_ME_WH.GROUP.CONTROL_SERVICE_INDICATIONS).write_line(
            value
        )
        MIO.create_output(A.D_TN.by_login(A.CT_AD_U.CONTROL_SERVICE)).write_line(value)

    def service_starts_handler() -> None:
        A.A_F.sync()
        locale.setlocale(locale.LC_ALL, "ru_RU")
        A.SRV_A.subscribe_on(SC.heart_beat)
        A.SRV_A.subscribe_on(SC.send_event)
        A.SRV_A.subscribe_on(SC.register_chiller_indications_value)

    def send_ct_indications() -> None:
        indications_value_container: CTIndicationsValueContainer | None = one(
            A.R_IND.last_ct_value_containers(True)
        )
        if ne(indications_value_container):
            MIO.create_output(A.CT_ME_WH.GROUP.CT_INDICATIONS).write_result(
                Result(
                    A.CT_FC.INDICATIONS.CT_VALUE,
                    CTIndicationsValue(
                        indications_value_container.temperature,
                        indications_value_container.humidity,
                    ),
                ),
                title="Показания в помещение КТ:",
            )

    def send_all_indications() -> None:
        A.A_MIO.send_command_to(
            js(("indications", FLAG_KEYWORDS.ALL_SYMBOL, FLAG_KEYWORDS.SILENCE)),
            A.CT_ME_WH.GROUP.CONTROL_SERVICE_INDICATIONS,
        )

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":

    start()
