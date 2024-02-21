import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.event_create_query_v2_resource_object_attributes_metric import (
        EventCreateQueryV2ResourceObjectAttributesMetric,
    )
    from ..models.event_create_query_v2_resource_object_attributes_profile import (
        EventCreateQueryV2ResourceObjectAttributesProfile,
    )
    from ..models.event_create_query_v2_resource_object_attributes_properties import (
        EventCreateQueryV2ResourceObjectAttributesProperties,
    )


T = TypeVar("T", bound="EventCreateQueryV2ResourceObjectAttributes")


@_attrs_define
class EventCreateQueryV2ResourceObjectAttributes:
    """
    Attributes:
        properties (EventCreateQueryV2ResourceObjectAttributesProperties): Properties of this event. Any top level
            property (that are not objects) can be
            used to create segments. The $extra property is a special property. This records any
            non-segmentable values that can be referenced later. For example, HTML templates are
            useful on a segment but are not used to create a segment. There are limits
            placed onto the size of the data present. This must not exceed 5 MB. This must not
            exceed 300 event properties. A single string cannot be larger than 100 KB. Each array
            must not exceed 4000 elements. The properties cannot contain more than 10 nested levels. Example: {'Brand':
            'Kids Book', 'Categories': ['Fiction', 'Children'], 'ProductID': 1111, 'ProductName': 'Winnie the Pooh',
            '$extra': {'URL': 'http://www.example.com/path/to/product', 'ImageURL':
            'http://www.example.com/path/to/product/image.png'}}.
        metric (EventCreateQueryV2ResourceObjectAttributesMetric):
        profile (EventCreateQueryV2ResourceObjectAttributesProfile):
        time (Union[Unset, datetime.datetime]): When this event occurred. By default, the time the request was received
            will be used.
            The time is truncated to the second. The time must be after the year 2000 and can only
            be up to 1 year in the future. Example: 2022-11-08T00:00:00.
        value (Union[Unset, float]): A numeric value to associate with this event. For example, the dollar amount of a
            purchase. Example: 9.99.
        unique_id (Union[Unset, str]): A unique identifier for an event. If the unique_id is repeated for the same
            profile and metric, only the first processed event will be recorded. If this is not
            present, this will use the time to the second. Using the default, this limits only one
            event per profile per second.
    """

    properties: "EventCreateQueryV2ResourceObjectAttributesProperties"
    metric: "EventCreateQueryV2ResourceObjectAttributesMetric"
    profile: "EventCreateQueryV2ResourceObjectAttributesProfile"
    time: Union[Unset, datetime.datetime] = UNSET
    value: Union[Unset, float] = UNSET
    unique_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        properties = self.properties.to_dict()

        metric = self.metric.to_dict()

        profile = self.profile.to_dict()

        time: Union[Unset, str] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        value = self.value

        unique_id = self.unique_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "properties": properties,
                "metric": metric,
                "profile": profile,
            }
        )
        if time is not UNSET:
            field_dict["time"] = time
        if value is not UNSET:
            field_dict["value"] = value
        if unique_id is not UNSET:
            field_dict["unique_id"] = unique_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_create_query_v2_resource_object_attributes_metric import (
            EventCreateQueryV2ResourceObjectAttributesMetric,
        )
        from ..models.event_create_query_v2_resource_object_attributes_profile import (
            EventCreateQueryV2ResourceObjectAttributesProfile,
        )
        from ..models.event_create_query_v2_resource_object_attributes_properties import (
            EventCreateQueryV2ResourceObjectAttributesProperties,
        )

        d = src_dict.copy()
        properties = EventCreateQueryV2ResourceObjectAttributesProperties.from_dict(d.pop("properties"))

        metric = EventCreateQueryV2ResourceObjectAttributesMetric.from_dict(d.pop("metric"))

        profile = EventCreateQueryV2ResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        _time = d.pop("time", UNSET)
        time: Union[Unset, datetime.datetime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        value = d.pop("value", UNSET)

        unique_id = d.pop("unique_id", UNSET)

        event_create_query_v2_resource_object_attributes = cls(
            properties=properties,
            metric=metric,
            profile=profile,
            time=time,
            value=value,
            unique_id=unique_id,
        )

        event_create_query_v2_resource_object_attributes.additional_properties = d
        return event_create_query_v2_resource_object_attributes

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
