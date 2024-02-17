# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ......core.datetime_utils import serialize_datetime
from ...types.types.ticket_priority import TicketPriority
from ...types.types.ticket_status import TicketStatus

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class TaskTicketWrite(pydantic.BaseModel):
    name: str = pydantic.Field(description="Name of the task.")
    assignees: typing.List[str] = pydantic.Field(description="collection of IDs belonging to assignees.")
    description: str = pydantic.Field(description="Description of the task.")
    status: TicketStatus = pydantic.Field(description="Current status of the task.")
    priority: TicketPriority = pydantic.Field(description="Priority of the task.")
    creator_id: str = pydantic.Field(alias="creatorId", description="ID of the task creator.")
    due_date: str = pydantic.Field(alias="dueDate", description="Due date for the given task.")
    completed_date: str = pydantic.Field(alias="completedDate", description="Date at which task was completed.")
    parent_id: str = pydantic.Field(alias="parentId", description="Id of the parent task.")
    list_id: str = pydantic.Field(alias="listId", description="Id of the list")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
