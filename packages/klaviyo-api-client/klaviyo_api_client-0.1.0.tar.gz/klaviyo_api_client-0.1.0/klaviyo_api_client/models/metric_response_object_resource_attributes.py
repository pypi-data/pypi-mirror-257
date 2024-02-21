from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_response_object_resource_attributes_integration import (
        MetricResponseObjectResourceAttributesIntegration,
    )


T = TypeVar("T", bound="MetricResponseObjectResourceAttributes")


@_attrs_define
class MetricResponseObjectResourceAttributes:
    """
    Attributes:
        name (Union[Unset, str]): The name of the metric
        created (Union[Unset, str]): Creation time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm)
        updated (Union[Unset, str]): Last updated time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm)
        integration (Union[Unset, MetricResponseObjectResourceAttributesIntegration]): The integration associated with
            the event
    """

    name: Union[Unset, str] = UNSET
    created: Union[Unset, str] = UNSET
    updated: Union[Unset, str] = UNSET
    integration: Union[Unset, "MetricResponseObjectResourceAttributesIntegration"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        created = self.created

        updated = self.updated

        integration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if integration is not UNSET:
            field_dict["integration"] = integration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_response_object_resource_attributes_integration import (
            MetricResponseObjectResourceAttributesIntegration,
        )

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        created = d.pop("created", UNSET)

        updated = d.pop("updated", UNSET)

        _integration = d.pop("integration", UNSET)
        integration: Union[Unset, MetricResponseObjectResourceAttributesIntegration]
        if isinstance(_integration, Unset):
            integration = UNSET
        else:
            integration = MetricResponseObjectResourceAttributesIntegration.from_dict(_integration)

        metric_response_object_resource_attributes = cls(
            name=name,
            created=created,
            updated=updated,
            integration=integration,
        )

        metric_response_object_resource_attributes.additional_properties = d
        return metric_response_object_resource_attributes

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
