from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_bulk_create_enum import EventBulkCreateEnum

if TYPE_CHECKING:
    from ..models.events_bulk_create_query_resource_object_attributes import (
        EventsBulkCreateQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="EventsBulkCreateQueryResourceObject")


@_attrs_define
class EventsBulkCreateQueryResourceObject:
    """
    Attributes:
        type (EventBulkCreateEnum):
        attributes (EventsBulkCreateQueryResourceObjectAttributes):
    """

    type: EventBulkCreateEnum
    attributes: "EventsBulkCreateQueryResourceObjectAttributes"
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
        from ..models.events_bulk_create_query_resource_object_attributes import (
            EventsBulkCreateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = EventBulkCreateEnum(d.pop("type"))

        attributes = EventsBulkCreateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        events_bulk_create_query_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        events_bulk_create_query_resource_object.additional_properties = d
        return events_bulk_create_query_resource_object

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
