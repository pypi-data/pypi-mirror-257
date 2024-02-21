import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="StaticScheduleOptions")


@_attrs_define
class StaticScheduleOptions:
    """
    Attributes:
        datetime_ (datetime.datetime): The time to send at Example: 2022-11-08T00:00:00.
        is_local (Union[Unset, bool]): If the campaign should be sent with local recipient timezone send (requires UTC
            time) or statically sent at the given time. Defaults to False.
        send_past_recipients_immediately (Union[Unset, bool]): Determines if we should send to local recipient timezone
            if the given time has passed. Only applicable to local sends. Defaults to False.
    """

    datetime_: datetime.datetime
    is_local: Union[Unset, bool] = UNSET
    send_past_recipients_immediately: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_ = self.datetime_.isoformat()

        is_local = self.is_local

        send_past_recipients_immediately = self.send_past_recipients_immediately

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datetime": datetime_,
            }
        )
        if is_local is not UNSET:
            field_dict["is_local"] = is_local
        if send_past_recipients_immediately is not UNSET:
            field_dict["send_past_recipients_immediately"] = send_past_recipients_immediately

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datetime_ = isoparse(d.pop("datetime"))

        is_local = d.pop("is_local", UNSET)

        send_past_recipients_immediately = d.pop("send_past_recipients_immediately", UNSET)

        static_schedule_options = cls(
            datetime_=datetime_,
            is_local=is_local,
            send_past_recipients_immediately=send_past_recipients_immediately,
        )

        static_schedule_options.additional_properties = d
        return static_schedule_options

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
