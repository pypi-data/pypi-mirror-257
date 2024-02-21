from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_variant_enum import CatalogVariantEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.object_links import ObjectLinks
    from ..models.patch_catalog_variant_response_data_attributes import PatchCatalogVariantResponseDataAttributes
    from ..models.patch_catalog_variant_response_data_relationships import PatchCatalogVariantResponseDataRelationships


T = TypeVar("T", bound="PatchCatalogVariantResponseData")


@_attrs_define
class PatchCatalogVariantResponseData:
    """
    Attributes:
        type (CatalogVariantEnum):
        id (str): The catalog variant ID is a compound ID (string), with format:
            `{integration}:::{catalog}:::{external_id}`. Currently, the only supported integration type is `$custom`, and
            the only supported catalog is `$default`. Example: $custom:::$default:::SAMPLE-DATA-ITEM-1-VARIANT-MEDIUM.
        attributes (PatchCatalogVariantResponseDataAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, PatchCatalogVariantResponseDataRelationships]):
    """

    type: CatalogVariantEnum
    id: str
    attributes: "PatchCatalogVariantResponseDataAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "PatchCatalogVariantResponseDataRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        links = self.links.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
                "links": links,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.object_links import ObjectLinks
        from ..models.patch_catalog_variant_response_data_attributes import PatchCatalogVariantResponseDataAttributes
        from ..models.patch_catalog_variant_response_data_relationships import (
            PatchCatalogVariantResponseDataRelationships,
        )

        d = src_dict.copy()
        type = CatalogVariantEnum(d.pop("type"))

        id = d.pop("id")

        attributes = PatchCatalogVariantResponseDataAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, PatchCatalogVariantResponseDataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = PatchCatalogVariantResponseDataRelationships.from_dict(_relationships)

        patch_catalog_variant_response_data = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        patch_catalog_variant_response_data.additional_properties = d
        return patch_catalog_variant_response_data

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
