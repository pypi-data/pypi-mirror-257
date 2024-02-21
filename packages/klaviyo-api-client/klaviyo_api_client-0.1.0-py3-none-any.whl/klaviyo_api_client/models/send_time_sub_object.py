import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SendTimeSubObject")


@_attrs_define
class SendTimeSubObject:
    """
    Attributes:
        datetime_ (datetime.datetime): The datetime that the message is to be sent Example: 2022-11-08T00:00:00.
        is_local (bool): Whether that datetime is to be a local datetime for the recipient
    """

    datetime_: datetime.datetime
    is_local: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_ = self.datetime_.isoformat()

        is_local = self.is_local

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datetime": datetime_,
                "is_local": is_local,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datetime_ = isoparse(d.pop("datetime"))

        is_local = d.pop("is_local")

        send_time_sub_object = cls(
            datetime_=datetime_,
            is_local=is_local,
        )

        send_time_sub_object.additional_properties = d
        return send_time_sub_object

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
