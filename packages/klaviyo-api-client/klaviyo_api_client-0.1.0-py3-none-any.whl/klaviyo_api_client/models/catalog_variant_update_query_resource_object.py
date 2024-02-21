from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_variant_enum import CatalogVariantEnum

if TYPE_CHECKING:
    from ..models.catalog_variant_update_query_resource_object_attributes import (
        CatalogVariantUpdateQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="CatalogVariantUpdateQueryResourceObject")


@_attrs_define
class CatalogVariantUpdateQueryResourceObject:
    """
    Attributes:
        type (CatalogVariantEnum):
        id (str): The catalog variant ID is a compound ID (string), with format:
            `{integration}:::{catalog}:::{external_id}`. Currently, the only supported integration type is `$custom`, and
            the only supported catalog is `$default`. Example: $custom:::$default:::SAMPLE-DATA-ITEM-1-VARIANT-MEDIUM.
        attributes (CatalogVariantUpdateQueryResourceObjectAttributes):
    """

    type: CatalogVariantEnum
    id: str
    attributes: "CatalogVariantUpdateQueryResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_variant_update_query_resource_object_attributes import (
            CatalogVariantUpdateQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = CatalogVariantEnum(d.pop("type"))

        id = d.pop("id")

        attributes = CatalogVariantUpdateQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        catalog_variant_update_query_resource_object = cls(
            type=type,
            id=id,
            attributes=attributes,
        )

        catalog_variant_update_query_resource_object.additional_properties = d
        return catalog_variant_update_query_resource_object

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
