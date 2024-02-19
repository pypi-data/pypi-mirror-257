import importlib.util
import sys

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")

from pih.a import A
from pih.service_collection import ServiceCommands
from pih.collection import (
    Result,
    User,
    Mark,
    FullName,
    Workstation,
    ComputerDescription,
    UserBase,
)
from pih.errors import NotFound
from pih.names import FIELD_COLLECTION
from typing import Any

NAME: str = "U"


@staticmethod
def get_not_found_error(title: str, active: bool, value: str) -> str:
    start: str | None = None
    if A.D.is_none(active):
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
        result: Result[User] = A.D.to_result(
            A.SRV.call_command(
                ServiceCommands.get_user_by_login, (value, active, cached)
            ),
            User,
        )
        if A.R.is_empty(result):
            raise get_not_found_error("логином", active, value)
        return result

    @staticmethod
    def by_telephone_number(value: str, active: bool | None = None) -> Result[User]:
        result: Result[User] = A.D.to_result(
            A.SRV.call_command(
                ServiceCommands.get_user_by_telephone_number, (value, active)
            ),
            User,
            True,
        )
        if A.R.is_empty(result):
            raise A.ER.USER.get_not_found_error("номером телефона", active, value)
        return result

    @staticmethod
    def by_internal_telephone_number(value: int) -> Result[User]:
        workstation_list: list[Workstation] = A.R.WORKSTATION.all().data
        result_worksation: Workstation = None
        for workstation in workstation_list:
            if not A.D.is_empty(workstation.description):
                index: int = workstation.description.find(
                    A.CT.INTERNAL_TELEPHONE_NUMBER_PREFIX
                )
                if index != -1:
                    internal_telephone_number_text: str = workstation.description[
                        index:
                    ]
                    internal_telephone_number: int = A.D.EXTRACT.decimal(
                        internal_telephone_number_text
                    )
                    if internal_telephone_number == value:
                        result_worksation = workstation
                        break
        if (
            result_worksation is not None
            and result_worksation.accessable
            and not A.D.is_empty(result_worksation.samAccountName)
        ):
            return A.R.USER.by_login(workstation.samAccountName)
        else:
            raise A.ER.USER.get_not_found_error(
                "внутренним номером телефона", True, str(value)
            )

    @staticmethod
    def by_polibase_pin(value: int) -> Result[User]:
        return A.R.with_first_item(
            A.R.USER.by_name(A.R.POLIBASE.person_by_pin(value).data.FullName)
        )

    @staticmethod
    def by_workstation_name(name: str) -> Result[User]:
        name = name.lower()
        user_workstation: Workstation = A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_user_by_workstation, name),
            Workstation,
            True,
        ).data
        if A.D.is_empty(user_workstation):
            details: str = f"Компьютер с именем '{name}' не найден!"
            raise NotFound(details)
        if A.D.is_empty(user_workstation.samAccountName):
            raise NotFound(
                f"За компьютером {name} нет залогиненного пользователя", name
            )
        return A.R.USER.by_login(user_workstation.samAccountName)

    @staticmethod
    def by_any(value: Any, active: bool | None = None) -> Result[list[User]]:
        def by_number(value: int) -> Result[list[User]]:
            try:
                return A.R.as_list(A.R.USER.by_tab_number(value))
            except NotFound:
                try:
                    return A.R.as_list(
                        A.R.USER.by_login(
                            A.R.WORKSTATION.by_internal_telephone_number(
                                value
                            ).data.samAccountName
                        )
                    )
                except:
                    return A.R.as_list(A.R.USER.by_polibase_pin(value))

        if isinstance(value, Mark):
            return A.R.USER.by_name(value.FullName)
        elif isinstance(value, FullName):
            return A.R.USER.by_full_name(value, False, active)
        elif isinstance(value, (ComputerDescription, Workstation)):
            return A.R.USER.by_any(value.name, active)
        elif isinstance(value, str):
            if value.lower().startswith(A.CT.GROUP_PREFIX):
                value = str(value[len(A.CT.GROUP_PREFIX) :])
                return A.R.USER.by_group_name(value)
            try:
                value_as_telephone_number: str = A.D.FORMAT.telephone_number(value)
                if A.C.telephone_number(value_as_telephone_number):
                    return A.R.as_list(
                        A.R.USER.by_telephone_number(value_as_telephone_number, active)
                    )
            except Exception:
                pass
            if A.D.CHECK.decimal(value):
                return by_number(value)
            if A.C.WORKSTATION.name(value):
                return A.R.as_list(A.R.USER.by_workstation_name(value))
            if A.C.login(value):
                return A.R.as_list(A.R.USER.by_login(value, active))
            if value == "" or A.C.name(value):
                return A.R.USER.by_name(value, active)
        elif isinstance(value, int):
            return by_number(value)
        raise A.ER.USER.get_not_found_error("поисковым значением", active, value)

    @staticmethod
    def by_job_position(value: A.CT_AD.JobPisitions) -> Result[list[User]]:
        return A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_users_by_job_position, value.name),
            User,
        )

    @staticmethod
    def by_group(value: A.CT_AD.Groups) -> Result[list[User]]:
        return A.R.USER.by_group_name(value.name)

    @staticmethod
    def by_group_name(value: str) -> Result[list[User]]:
        return A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_users_by_group, value), User
        )

    @staticmethod
    def template_list() -> Result[list[User]]:
        return A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_template_users), User
        )

    @staticmethod
    def containers() -> Result[list[UserBase]]:
        return A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_containers), UserBase
        )

    @staticmethod
    def by_full_name(
        value: FullName, get_first: bool = False, active: bool | None = None
    ) -> Result[list[User] | User]:
        return A.D.to_result(
            A.SRV.call_command(ServiceCommands.get_user_by_full_name, (value, active)),
            User,
            get_first,
        )

    @staticmethod
    def by_name(
        value: str, active: bool | None = None, cached: bool | None = None
    ) -> Result[list[User]]:
        result: Result[list[User]] = A.D.to_result(
            A.SRV.call_command(
                ServiceCommands.get_users_by_name, (value, active, cached)
            ),
            User,
        )
        if A.R.is_empty(result):
            raise A.ER.USER.get_not_found_error("именем", active, value)
        return result

    @staticmethod
    def all(active: bool | None = None) -> Result[list[User]]:
        return A.R.USER.by_name(A.CT_AD.SEARCH_ALL_PATTERN, active)

    @staticmethod
    def list_with_telephone_number(active: bool | None = None) -> Result[list[User]]:
        def user_with_telephone_number(user: User) -> bool:
            return A.C.telephone_number(user.telephoneNumber)

        return A.R.filter(
            user_with_telephone_number, A.R.USER.all(active)
        )

    @staticmethod
    def by_tab_number(value: str) -> Result[User]:
        result: Result[Mark] = A.R.MARK.by_tab_number(value)
        if A.R.is_empty(result):
            details: str = f"Карта доступа с номером {value} не найдена"
            raise NotFound(details)
        return A.R.USER.by_mark(result.data)

    @staticmethod
    def by_mark(value: Mark) -> Result[User]:
        return Result(
            FIELD_COLLECTION.AD.USER,
            A.D.check(
                value,
                lambda: A.D.get_first_item(
                    A.R.USER.by_full_name(A.D.fullname_from_string(value.FullName)).data
                ),
            ),
        )
