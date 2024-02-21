from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_aggregate_enum import MetricAggregateEnum

if TYPE_CHECKING:
    from ..models.metric_aggregate_query_resource_object_attributes import MetricAggregateQueryResourceObjectAttributes


T = TypeVar("T", bound="MetricAggregateQueryResourceObject")


@_attrs_define
class MetricAggregateQueryResourceObject:
    """
    Attributes:
        type (MetricAggregateEnum):
        attributes (MetricAggregateQueryResourceObjectAttributes):
    """

    type: MetricAggregateEnum
    attributes: "MetricAggregateQueryResourceObjectAttributes"
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
        from ..models.metric_aggregate_query_resource_object_attributes import (
            MetricAggregateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = MetricAggregateEnum(d.pop("type"))

        attributes = MetricAggregateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        metric_aggregate_query_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        metric_aggregate_query_resource_object.additional_properties = d
        return metric_aggregate_query_resource_object

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
