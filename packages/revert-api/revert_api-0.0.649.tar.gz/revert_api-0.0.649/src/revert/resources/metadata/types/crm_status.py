# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class CrmStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    def visit(self, active: typing.Callable[[], T_Result], inactive: typing.Callable[[], T_Result]) -> T_Result:
        if self is CrmStatus.ACTIVE:
            return active()
        if self is CrmStatus.INACTIVE:
            return inactive()
