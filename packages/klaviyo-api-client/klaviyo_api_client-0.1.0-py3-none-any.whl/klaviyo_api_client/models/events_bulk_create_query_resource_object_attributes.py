from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.events_bulk_create_query_resource_object_attributes_events import (
        EventsBulkCreateQueryResourceObjectAttributesEvents,
    )
    from ..models.events_bulk_create_query_resource_object_attributes_profile import (
        EventsBulkCreateQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="EventsBulkCreateQueryResourceObjectAttributes")


@_attrs_define
class EventsBulkCreateQueryResourceObjectAttributes:
    """
    Attributes:
        profile (EventsBulkCreateQueryResourceObjectAttributesProfile):
        events (EventsBulkCreateQueryResourceObjectAttributesEvents):
    """

    profile: "EventsBulkCreateQueryResourceObjectAttributesProfile"
    events: "EventsBulkCreateQueryResourceObjectAttributesEvents"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile = self.profile.to_dict()

        events = self.events.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.events_bulk_create_query_resource_object_attributes_events import (
            EventsBulkCreateQueryResourceObjectAttributesEvents,
        )
        from ..models.events_bulk_create_query_resource_object_attributes_profile import (
            EventsBulkCreateQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        profile = EventsBulkCreateQueryResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        events = EventsBulkCreateQueryResourceObjectAttributesEvents.from_dict(d.pop("events"))

        events_bulk_create_query_resource_object_attributes = cls(
            profile=profile,
            events=events,
        )

        events_bulk_create_query_resource_object_attributes.additional_properties = d
        return events_bulk_create_query_resource_object_attributes

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
