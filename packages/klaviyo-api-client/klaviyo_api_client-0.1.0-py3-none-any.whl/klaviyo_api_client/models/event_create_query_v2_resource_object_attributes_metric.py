from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_create_query_resource_object import MetricCreateQueryResourceObject


T = TypeVar("T", bound="EventCreateQueryV2ResourceObjectAttributesMetric")


@_attrs_define
class EventCreateQueryV2ResourceObjectAttributesMetric:
    """
    Attributes:
        data (MetricCreateQueryResourceObject):
    """

    data: "MetricCreateQueryResourceObject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_create_query_resource_object import MetricCreateQueryResourceObject

        d = src_dict.copy()
        data = MetricCreateQueryResourceObject.from_dict(d.pop("data"))

        event_create_query_v2_resource_object_attributes_metric = cls(
            data=data,
        )

        event_create_query_v2_resource_object_attributes_metric.additional_properties = d
        return event_create_query_v2_resource_object_attributes_metric

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
