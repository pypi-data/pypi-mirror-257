import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ThrottledScheduleOptions")


@_attrs_define
class ThrottledScheduleOptions:
    """
    Attributes:
        datetime_ (datetime.datetime): The time to send at
        throttle_percentage (int): The percentage of recipients per hour to send to. Allowed values: [10, 11, 13, 14,
            17, 20, 25, 33, 50]
    """

    datetime_: datetime.datetime
    throttle_percentage: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_ = self.datetime_.isoformat()

        throttle_percentage = self.throttle_percentage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datetime": datetime_,
                "throttle_percentage": throttle_percentage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datetime_ = isoparse(d.pop("datetime"))

        throttle_percentage = d.pop("throttle_percentage")

        throttled_schedule_options = cls(
            datetime_=datetime_,
            throttle_percentage=throttle_percentage,
        )

        throttled_schedule_options.additional_properties = d
        return throttled_schedule_options

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
