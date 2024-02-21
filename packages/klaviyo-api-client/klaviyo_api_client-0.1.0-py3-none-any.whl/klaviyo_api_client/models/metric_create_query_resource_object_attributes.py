from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricCreateQueryResourceObjectAttributes")


@_attrs_define
class MetricCreateQueryResourceObjectAttributes:
    """
    Attributes:
        name (str): Name of the event. Must be less than 128 characters. Example: Viewed Product.
        service (Union[Unset, str]): This is for advanced usage. For api requests, this should use the default, which is
            set to api.
    """

    name: str
    service: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        service = self.service

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if service is not UNSET:
            field_dict["service"] = service

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        service = d.pop("service", UNSET)

        metric_create_query_resource_object_attributes = cls(
            name=name,
            service=service,
        )

        metric_create_query_resource_object_attributes.additional_properties = d
        return metric_create_query_resource_object_attributes

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
