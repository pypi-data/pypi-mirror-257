from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_catalog_category_delete_job_response_data_relationships_categories import (
        GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories,
    )


T = TypeVar("T", bound="GetCatalogCategoryDeleteJobResponseDataRelationships")


@_attrs_define
class GetCatalogCategoryDeleteJobResponseDataRelationships:
    """
    Attributes:
        categories (Union[Unset, GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories]):
    """

    categories: Union[Unset, "GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        categories: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if categories is not UNSET:
            field_dict["categories"] = categories

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_catalog_category_delete_job_response_data_relationships_categories import (
            GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories,
        )

        d = src_dict.copy()
        _categories = d.pop("categories", UNSET)
        categories: Union[Unset, GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories]
        if isinstance(_categories, Unset):
            categories = UNSET
        else:
            categories = GetCatalogCategoryDeleteJobResponseDataRelationshipsCategories.from_dict(_categories)

        get_catalog_category_delete_job_response_data_relationships = cls(
            categories=categories,
        )

        get_catalog_category_delete_job_response_data_relationships.additional_properties = d
        return get_catalog_category_delete_job_response_data_relationships

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
