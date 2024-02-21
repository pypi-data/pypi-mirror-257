from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CatalogItemResponseObjectResourceAttributesCustomMetadata")


@_attrs_define
class CatalogItemResponseObjectResourceAttributesCustomMetadata:
    """Flat JSON blob to provide custom metadata about the catalog item. May not exceed 100kb.

    Example:
        {'Top Pick': True}

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        catalog_item_response_object_resource_attributes_custom_metadata = cls()

        catalog_item_response_object_resource_attributes_custom_metadata.additional_properties = d
        return catalog_item_response_object_resource_attributes_custom_metadata

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
