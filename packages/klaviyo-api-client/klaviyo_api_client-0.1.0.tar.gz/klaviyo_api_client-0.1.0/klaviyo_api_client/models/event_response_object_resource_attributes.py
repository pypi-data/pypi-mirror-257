import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event_response_object_resource_attributes_event_properties import (
        EventResponseObjectResourceAttributesEventProperties,
    )


T = TypeVar("T", bound="EventResponseObjectResourceAttributes")


@_attrs_define
class EventResponseObjectResourceAttributes:
    """
    Attributes:
        timestamp (Union[Unset, int]): Event timestamp in seconds
        event_properties (Union[Unset, EventResponseObjectResourceAttributesEventProperties]): Event properties, can
            include identifiers and extra properties
        datetime_ (Union[Unset, datetime.datetime]): Event timestamp in ISO8601 format (YYYY-MM-DDTHH:MM:SS+hh:mm)
            Example: 2022-11-08T01:23:45+00:00.
        uuid (Union[Unset, str]): A unique identifier for the event, this can be used as a cursor in pagination
    """

    timestamp: Union[Unset, int] = UNSET
    event_properties: Union[Unset, "EventResponseObjectResourceAttributesEventProperties"] = UNSET
    datetime_: Union[Unset, datetime.datetime] = UNSET
    uuid: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp

        event_properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event_properties, Unset):
            event_properties = self.event_properties.to_dict()

        datetime_: Union[Unset, str] = UNSET
        if not isinstance(self.datetime_, Unset):
            datetime_ = self.datetime_.isoformat()

        uuid = self.uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if event_properties is not UNSET:
            field_dict["event_properties"] = event_properties
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_
        if uuid is not UNSET:
            field_dict["uuid"] = uuid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_response_object_resource_attributes_event_properties import (
            EventResponseObjectResourceAttributesEventProperties,
        )

        d = src_dict.copy()
        timestamp = d.pop("timestamp", UNSET)

        _event_properties = d.pop("event_properties", UNSET)
        event_properties: Union[Unset, EventResponseObjectResourceAttributesEventProperties]
        if isinstance(_event_properties, Unset):
            event_properties = UNSET
        else:
            event_properties = EventResponseObjectResourceAttributesEventProperties.from_dict(_event_properties)

        _datetime_ = d.pop("datetime", UNSET)
        datetime_: Union[Unset, datetime.datetime]
        if isinstance(_datetime_, Unset):
            datetime_ = UNSET
        else:
            datetime_ = isoparse(_datetime_)

        uuid = d.pop("uuid", UNSET)

        event_response_object_resource_attributes = cls(
            timestamp=timestamp,
            event_properties=event_properties,
            datetime_=datetime_,
            uuid=uuid,
        )

        event_response_object_resource_attributes.additional_properties = d
        return event_response_object_resource_attributes

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
