from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_catalog_variant_response_data_relationships_item import (
        PatchCatalogVariantResponseDataRelationshipsItem,
    )


T = TypeVar("T", bound="PatchCatalogVariantResponseDataRelationships")


@_attrs_define
class PatchCatalogVariantResponseDataRelationships:
    """
    Attributes:
        item (Union[Unset, PatchCatalogVariantResponseDataRelationshipsItem]):
    """

    item: Union[Unset, "PatchCatalogVariantResponseDataRelationshipsItem"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if item is not UNSET:
            field_dict["item"] = item

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patch_catalog_variant_response_data_relationships_item import (
            PatchCatalogVariantResponseDataRelationshipsItem,
        )

        d = src_dict.copy()
        _item = d.pop("item", UNSET)
        item: Union[Unset, PatchCatalogVariantResponseDataRelationshipsItem]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = PatchCatalogVariantResponseDataRelationshipsItem.from_dict(_item)

        patch_catalog_variant_response_data_relationships = cls(
            item=item,
        )

        patch_catalog_variant_response_data_relationships.additional_properties = d
        return patch_catalog_variant_response_data_relationships

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
