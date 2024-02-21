from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_catalog_variant_delete_job_response_data_relationships_variants import (
        PostCatalogVariantDeleteJobResponseDataRelationshipsVariants,
    )


T = TypeVar("T", bound="PostCatalogVariantDeleteJobResponseDataRelationships")


@_attrs_define
class PostCatalogVariantDeleteJobResponseDataRelationships:
    """
    Attributes:
        variants (Union[Unset, PostCatalogVariantDeleteJobResponseDataRelationshipsVariants]):
    """

    variants: Union[Unset, "PostCatalogVariantDeleteJobResponseDataRelationshipsVariants"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        variants: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.variants, Unset):
            variants = self.variants.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if variants is not UNSET:
            field_dict["variants"] = variants

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_catalog_variant_delete_job_response_data_relationships_variants import (
            PostCatalogVariantDeleteJobResponseDataRelationshipsVariants,
        )

        d = src_dict.copy()
        _variants = d.pop("variants", UNSET)
        variants: Union[Unset, PostCatalogVariantDeleteJobResponseDataRelationshipsVariants]
        if isinstance(_variants, Unset):
            variants = UNSET
        else:
            variants = PostCatalogVariantDeleteJobResponseDataRelationshipsVariants.from_dict(_variants)

        post_catalog_variant_delete_job_response_data_relationships = cls(
            variants=variants,
        )

        post_catalog_variant_delete_job_response_data_relationships.additional_properties = d
        return post_catalog_variant_delete_job_response_data_relationships

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
