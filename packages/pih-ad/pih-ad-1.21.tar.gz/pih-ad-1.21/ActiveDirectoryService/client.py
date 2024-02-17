import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")

from pih.service_collection import ServiceCommands as SC
from pih.collection import (
    Result,
    User,
    Mark,
    FullName,
    Workstation,
    WorkstationDescription,
    UserBase,
    PolibasePerson,
    SessionBase
)
from pih.const import LogMessageFlags
from pih.ad import AD
from pih.errors import NotFound
from pih.names import FIELD_COLLECTION, USER_PROPERTIES
from ActiveDirectoryService.const import SD
from shared.facade import FACADE as F
from typing import Any

NAME: str = "U"

@staticmethod
def get_not_found_error(title: str, active: bool, value: str) -> str:
    start: str | None = None
    if F.D.is_none(active):
        start = "Пользователь"
    elif active:
        start = "Активный пользователь"
    else:
        start = "Неактивный пользователь"
    return NotFound(f"{start} с {title} '{value}' не найден", value)


class RESULT:
    @staticmethod
    def by_login(
        value: str, active: bool | None = None, cached: bool | None = None
    ) -> Result[User]:
        result: Result[User] = F.D.to_result(
            F.SRV.call_command(SC.get_user_by_login, (value, active, cached)),
            User
        )
        if F.R.is_empty(result):
            raise get_not_found_error("логином", active, value)
        return result

    @staticmethod
    def by_telephone_number(value: str, active: bool | None = None) -> Result[User]:
        result: Result[User] = F.D.to_result(
            F.SRV.call_command(SC.get_user_by_telephone_number, (value, active)),
            User,
            True,
        )
        if F.R.is_empty(result):
            raise get_not_found_error("номером телефона", active, value)
        return result

    @staticmethod
    def by_internal_telephone_number(value: int) -> Result[User]:
        workstation_list: list[Workstation] = RESULT.all().data
        result_worksation: Workstation = None
        for workstation in workstation_list:
            if not F.D.is_empty(workstation.description):
                index: int = workstation.description.find(
                    F.CT.INTERNAL_TELEPHONE_NUMBER_PREFIX
                )
                if index != -1:
                    internal_telephone_number_text: str = workstation.description[
                        index:
                    ]
                    internal_telephone_number: int = F.D.EXTRACT.decimal(
                        internal_telephone_number_text
                    )
                    if internal_telephone_number == value:
                        result_worksation = workstation
                        break
        if (
            result_worksation is not None
            and result_worksation.accessable
            and not F.D.is_empty(result_worksation.samAccountName)
        ):
            return RESULT.by_login(workstation.samAccountName)
        else:
            raise get_not_found_error("внутренним номером телефона", True, str(value))

    @staticmethod
    def by_polibase_pin(value: int) -> Result[User]:
        return F.R.with_first_item(
            RESULT.by_name(F.R.POLIBASE.person_by_pin(value).data.FullName)
        )

    @staticmethod
    def by_workstation_name(name: str) -> Result[User]:
        name = name.lower()
        user_workstation: Workstation = F.D.to_result(
            F.SRV.call_command(SC.get_user_by_workstation, name),
            Workstation,
            True,
        ).data
        if F.D.is_empty(user_workstation):
            details: str = f"Компьютер с именем '{name}' не найден!"
            raise NotFound(details)
        if F.D.is_empty(user_workstation.samAccountName):
            raise NotFound(
                f"За компьютером {name} нет залогиненного пользователя", name
            )
        return RESULT.by_login(user_workstation.samAccountName)

    @staticmethod
    def by_any(value: Any, active: bool | None = None) -> Result[list[User]]:
        def by_number(value: int) -> Result[list[User]]:
            try:
                return F.R.as_list(RESULT.by_tab_number(value))
            except NotFound:
                try:
                    return F.R.as_list(
                        RESULT.by_login(
                            RESULT.by_internal_telephone_number(
                                value
                            ).data.samAccountName
                        )
                    )
                except:
                    return F.R.as_list(RESULT.by_polibase_pin(value))

        if isinstance(value, Mark):
            return RESULT.by_name(value.FullName)
        elif isinstance(value, FullName):
            return RESULT.by_full_name(value, False, active)
        elif isinstance(value, (WorkstationDescription, Workstation)):
            return RESULT.by_any(value.name, active)
        elif isinstance(value, str):
            if value.lower().startswith(F.CT.GROUP_PREFIX):
                value = str(value[len(F.CT.GROUP_PREFIX) :])
                return RESULT.by_group_name(value)
            try:
                value_as_telephone_number: str = F.D.FORMAT.telephone_number(value)
                if F.C.telephone_number(value_as_telephone_number):
                    return F.R.as_list(
                        RESULT.by_telephone_number(value_as_telephone_number, active)
                    )
            except Exception:
                pass
            if F.D.CHECK.decimal(value):
                return by_number(value)
            if F.C_W.name(value):
                return F.R.as_list(RESULT.by_workstation_name(value))
            if F.C.login(value):
                return F.R.as_list(RESULT.by_login(value, active))
            if value == "" or F.C.name(value):
                return RESULT.by_name(value, active)
        elif isinstance(value, int):
            return by_number(value)
        raise get_not_found_error("поисковым значением", active, value)

    @staticmethod
    def by_job_position(value: F.CT_AD.JobPisitions) -> Result[list[User]]:
        return F.D.to_result(
            F.SRV.call_command(SC.get_users_by_job_position, value.name),
            User,
        )

    @staticmethod
    def by_group(value: F.CT_AD.Groups) -> Result[list[User]]:
        return RESULT.by_group_name(value.name)

    @staticmethod
    def by_group_name(value: str) -> Result[list[User]]:
        return F.D.to_result(F.SRV.call_command(SC.get_users_by_group, value), User)

    @staticmethod
    def template_list() -> Result[list[User]]:
        return F.D.to_result(F.SRV.call_command(SC.get_template_users), User)

    @staticmethod
    def containers() -> Result[list[UserBase]]:
        return F.D.to_result(F.SRV.call_command(SC.get_containers), UserBase)

    @staticmethod
    def by_full_name(
        value: FullName, get_first: bool = False, active: bool | None = None
    ) -> Result[list[User] | User]:
        return F.D.to_result(
            F.SRV.call_command(SC.get_user_by_full_name, (value, active)),
            User,
            get_first,
        )

    @staticmethod
    def by_name(
        value: str, active: bool | None = None, cached: bool | None = None
    ) -> Result[list[User]]:
        result: Result[list[User]] = F.D.to_result(
            F.SRV.call_command(SC.get_users_by_name, (value, active, cached)),
            User,
        )
        if F.R.is_empty(result):
            raise get_not_found_error("именем", active, value)
        return result

    @staticmethod
    def all(active: bool | None = None) -> Result[list[User]]:
        return RESULT.by_name(F.CT_AD.SEARCH_ALL_PATTERN, active)

    @staticmethod
    def list_with_telephone_number(active: bool | None = None) -> Result[list[User]]:
        def user_with_telephone_number(user: User) -> bool:
            return F.C.telephone_number(user.telephoneNumber)

        return F.R.filter(
            RESULT.all(active), lambda user: user_with_telephone_number(user)
        )

    @staticmethod
    def by_tab_number(value: str) -> Result[User]:
        result: Result[Mark] = F.R.MARK.by_tab_number(value)
        if F.R.is_empty(result):
            details: str = f"Карта доступа с номером {value} не найдена"
            raise NotFound(details)
        return RESULT.by_mark(result.data)

    @staticmethod
    def by_mark(value: Mark) -> Result[User]:
        return Result(
            FIELD_COLLECTION.AD.USER,
            F.D.check_not_none(
                value,
                lambda: F.D.get_first_item(
                    RESULT.by_full_name(F.D.fullname_from_string(value.FullName)).data
                ),
            ),
        )


class ACTION:
    @staticmethod
    def drop_user_cache() -> bool:
        return F.D.rpc_unrepresent(F.SRV.call_command(SC.drop_user_cache))

    @staticmethod
    def create_from_template(
        container_dn: str,
        full_name: FullName,
        login: str,
        password: str,
        description: str,
        telephone: str,
        email: str,
    ) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(
                SC.create_user_by_template,
                (
                    container_dn,
                    full_name,
                    login,
                    password,
                    description,
                    telephone,
                    email,
                ),
            )
        )

    @staticmethod
    def create_in_container(
        container_dn: str,
        full_name: FullName,
        login: str,
        password: str,
        description: str,
        telephone: str,
        email: str,
    ) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(
                SC.create_user_in_container,
                (
                    container_dn,
                    full_name,
                    login,
                    password,
                    description,
                    telephone,
                    email,
                ),
            )
        )

    @staticmethod
    def set_telephone_number(user: User, telephone: str) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(
                SC.set_user_telephone_number, (user.distinguishedName, telephone)
            )
        )

    @staticmethod
    def set_password(user: User, password: str) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(SC.set_user_password, (user.distinguishedName, password))
        )

    @staticmethod
    def set_status(user: User, status: str, container: UserBase) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(
                SC.set_user_status,
                (
                    user.distinguishedName,
                    status,
                    F.D.check(container, lambda: container.distinguishedName),
                ),
            )
        )

    @staticmethod
    def remove(user: User) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(SC.remove_user, user.distinguishedName)
        )


class CHECK:

    @staticmethod
    def by_group(user: User, group: AD.Groups) -> bool:
        return not F.D.is_empty(
            F.R.do_while(
                RESULT.by_group(group),
                lambda check_user: check_user.samAccountName == user.samAccountName,
            )
        )

    @staticmethod
    def exists_by_login(value: str) -> bool:
        return F.D.rpc_unrepresent(
            F.SRV.call_command(SC.check_user_exists_by_login, value)
        )

    @staticmethod
    def user(user: User) -> bool:
        return F.C.full_name(user.name)

    @staticmethod
    def active(user: User) -> bool:
        return user.distinguishedName.find(AD.ACTIVE_USERS_CONTAINER_DN) != -1

    @staticmethod
    def exists_by_full_name(value: FullName) -> bool:
        return not F.R.is_empty(RESULT.by_full_name(value))

    @staticmethod
    def search_attribute(value: str) -> bool:
        return value in AD.SEARCH_ATTRIBUTES

    @staticmethod
    def property(
        value: str | None, default_value: str = USER_PROPERTIES.PASSWORD
    ) -> str:
        return value or default_value

    @staticmethod
    def accessibility() -> bool:
        return F.SRV.check_on_accessibility(SD)
    
    class ACCESS:

        @staticmethod
        def by_group(group: AD.Groups, exit_on_access_denied: bool = False, session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            session = session or F.SE
            user: User = session.get_user()
            result: bool = False
            notify: bool = notify_on_success or notify_on_fail
            if group in session.allowed_groups:
                result = True
                notify = False
            else:
                result = CHECK.by_group(user, group)
                if result:
                    session.add_allowed_group(group)
            if notify:
                F.L.it(
                    f"Запрос на доступа к группе: {group.name} от пользователя {user.name} ({user.samAccountName}). Доступ {'разрешен' if result else 'отклонен'}.", LogMessageFlags.NORMAL if result else LogMessageFlags.ERROR)
            if not result and exit_on_access_denied:
                session.exit(5, "Функционал недоступен...")
            return result

        @staticmethod
        def admin(exit_on_access_denied: bool = False, session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            return CHECK.ACCESS.by_group(AD.Groups.Admin, exit_on_access_denied, session, notify_on_fail, notify_on_success)

        @staticmethod
        def service_admin(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            return CHECK.ACCESS.by_group(AD.Groups.ServiceAdmin, False, session, notify_on_fail, notify_on_success)

        @staticmethod
        def inventory(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            return CHECK.ACCESS.by_group(AD.Groups.Inventory, False, session, notify_on_fail, notify_on_success)

        @staticmethod
        def polibase(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            return CHECK.ACCESS.by_group(AD.Groups.Polibase, False, session, notify_on_fail, notify_on_success)

        @staticmethod
        def card_registry(session: SessionBase = None, notify_on_fail: bool = True, notify_on_success: bool = True) -> bool:
            return CHECK.ACCESS.by_group(AD.Groups.CardRegistry, False, session, notify_on_fail, notify_on_success)



class DATA:

    @staticmethod
    def by_login(
        value: str, active: bool | None = None, cached: bool | None = None
    ) -> User:
        return RESULT.by_login(value, active, cached).data

    @staticmethod
    def by_name(value: str) -> User:
        return RESULT.by_name(value).data


class EVENT:

    @staticmethod
    def polibase_person_with_inaccessable_email_was_detected(
        person: PolibasePerson | None = None,
        registrator_person: PolibasePerson | None = None,
        actual: bool = False,
    ) -> tuple[F.CT_E | tuple[Any]] | F.CT_E:
        def get_information() -> tuple[Any]:
            workstation_name: str = "<не определён>"
            workstation_description: str = "<не определён>"
            if actual:
                try:
                    user: User = RESULT.by_polibase_pin(registrator_person.pin).data
                    workstation: Workstation = (
                        F.R.get_first_item(F.R_W.by_login(user.samAccountName))
                        or F.R_W.by_name(F.CT.TEST.WORKSTATION_MAME).data
                    )
                    if F.D.is_not_none(workstation):
                        workstation_name = workstation.name
                        workstation_description = workstation.description
                except NotFound:
                    pass
            return (
                person.FullName,
                person.pin,
                person.email,
                registrator_person.FullName,
                workstation_name,
                workstation_description,
            )

        event: F.CT_E = F.CT_E.POLIBASE_PERSON_WITH_INACCESSABLE_EMAIL_WAS_DETECTED
        return F.E_B.create_event(
            event,
            registrator_person,
            get_information,
            F.D.check_not_none(person, lambda: (None, person.pin)),
        )

    @staticmethod
    def login() -> None:
        login: str = F.SE.get_login()
        user: User = RESULT.by_login(login).data
        F.E.send(F.CT_E.LOG_IN, (user.name, login, F.OS.host()))

    @staticmethod
    def hr_notify_about_new_employee(login: User) -> None:
        user: User = RESULT.by_login(login).data
        hr_user: User = F.R.get_first_item(RESULT.by_job_position(AD.JobPisitions.HR))
        F.E.send(
            F.CT_E.HR_NOTIFY_ABOUT_NEW_EMPLOYEE,
            (F.D.to_given_name(hr_user.name), user.name, user.mail),
        )

    @staticmethod
    def it_notify_about_user_creation(login: str, password: str) -> None:
        it_user_list: list[User] = RESULT.by_job_position(AD.JobPisitions.IT).data
        me_user_login: str = F.SE.get_login()
        it_user_list = list(
            filter(lambda user: user.samAccountName != me_user_login, it_user_list)
        )
        it_user: User = it_user_list[0]
        user: User = RESULT.by_login(login).data
        F.E.send(
            F.CT_E.IT_NOTIFY_ABOUT_CREATE_USER,
            (
                user.name,
                user.description,
                user.samAccountName,
                password,
                user.telephoneNumber,
                user.mail,
            ),
        )
        F.E.send(
            F.CT_E.IT_TASK_AFTER_CREATE_NEW_USER,
            (F.D.to_given_name(it_user.name), user.name, user.mail, password),
        )

class TELEPHONE_NUMBER:

    @staticmethod
    def by_login(value: str, format: bool = True, active: bool = True, cached: bool = True) -> str:
        result: str = DATA.by_login(value, active, cached).telephoneNumber
        return F.D_F.telephone_number(result) if format else result