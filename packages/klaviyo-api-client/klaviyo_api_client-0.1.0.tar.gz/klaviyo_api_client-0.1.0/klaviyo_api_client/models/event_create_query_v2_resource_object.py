from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_enum import EventEnum

if TYPE_CHECKING:
    from ..models.event_create_query_v2_resource_object_attributes import EventCreateQueryV2ResourceObjectAttributes


T = TypeVar("T", bound="EventCreateQueryV2ResourceObject")


@_attrs_define
class EventCreateQueryV2ResourceObject:
    """
    Attributes:
        type (EventEnum):
        attributes (EventCreateQueryV2ResourceObjectAttributes):
    """

    type: EventEnum
    attributes: "EventCreateQueryV2ResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_create_query_v2_resource_object_attributes import EventCreateQueryV2ResourceObjectAttributes

        d = src_dict.copy()
        type = EventEnum(d.pop("type"))

        attributes = EventCreateQueryV2ResourceObjectAttributes.from_dict(d.pop("attributes"))

        event_create_query_v2_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        event_create_query_v2_resource_object.additional_properties = d
        return event_create_query_v2_resource_object

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
