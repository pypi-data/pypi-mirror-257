from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_category_create_query_resource_object_attributes_integration_type import (
    CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CatalogCategoryCreateQueryResourceObjectAttributes")


@_attrs_define
class CatalogCategoryCreateQueryResourceObjectAttributes:
    """
    Attributes:
        external_id (str): The ID of the catalog category in an external system. Example: SAMPLE-DATA-CATEGORY-APPAREL.
        name (str): The name of the catalog category. Example: Sample Data Category Apparel.
        integration_type (Union[Unset, CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType]): The
            integration type. Currently only "$custom" is supported. Default:
            CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType.VALUE_0. Example: $custom.
        catalog_type (Union[Unset, str]): The type of catalog. Currently only "$default" is supported. Default:
            '$default'. Example: $default.
    """

    external_id: str
    name: str
    integration_type: Union[
        Unset, CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType
    ] = CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType.VALUE_0
    catalog_type: Union[Unset, str] = "$default"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id

        name = self.name

        integration_type: Union[Unset, str] = UNSET
        if not isinstance(self.integration_type, Unset):
            integration_type = self.integration_type.value

        catalog_type = self.catalog_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "external_id": external_id,
                "name": name,
            }
        )
        if integration_type is not UNSET:
            field_dict["integration_type"] = integration_type
        if catalog_type is not UNSET:
            field_dict["catalog_type"] = catalog_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_id = d.pop("external_id")

        name = d.pop("name")

        _integration_type = d.pop("integration_type", UNSET)
        integration_type: Union[Unset, CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType]
        if isinstance(_integration_type, Unset):
            integration_type = UNSET
        else:
            integration_type = CatalogCategoryCreateQueryResourceObjectAttributesIntegrationType(_integration_type)

        catalog_type = d.pop("catalog_type", UNSET)

        catalog_category_create_query_resource_object_attributes = cls(
            external_id=external_id,
            name=name,
            integration_type=integration_type,
            catalog_type=catalog_type,
        )

        catalog_category_create_query_resource_object_attributes.additional_properties = d
        return catalog_category_create_query_resource_object_attributes

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
