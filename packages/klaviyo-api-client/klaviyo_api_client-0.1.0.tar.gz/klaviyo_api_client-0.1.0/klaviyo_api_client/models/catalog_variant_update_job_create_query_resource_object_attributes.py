from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.catalog_variant_update_job_create_query_resource_object_attributes_variants import (
        CatalogVariantUpdateJobCreateQueryResourceObjectAttributesVariants,
    )


T = TypeVar("T", bound="CatalogVariantUpdateJobCreateQueryResourceObjectAttributes")


@_attrs_define
class CatalogVariantUpdateJobCreateQueryResourceObjectAttributes:
    """
    Attributes:
        variants (CatalogVariantUpdateJobCreateQueryResourceObjectAttributesVariants): Array of catalog variants to
            update.
    """

    variants: "CatalogVariantUpdateJobCreateQueryResourceObjectAttributesVariants"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        variants = self.variants.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "variants": variants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_variant_update_job_create_query_resource_object_attributes_variants import (
            CatalogVariantUpdateJobCreateQueryResourceObjectAttributesVariants,
        )

        d = src_dict.copy()
        variants = CatalogVariantUpdateJobCreateQueryResourceObjectAttributesVariants.from_dict(d.pop("variants"))

        catalog_variant_update_job_create_query_resource_object_attributes = cls(
            variants=variants,
        )

        catalog_variant_update_job_create_query_resource_object_attributes.additional_properties = d
        return catalog_variant_update_job_create_query_resource_object_attributes

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
