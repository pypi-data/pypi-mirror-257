from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_category_enum import CatalogCategoryEnum

T = TypeVar("T", bound="GetCatalogCategoryUpdateJobResponseCompoundDocumentDataRelationshipsCategoriesDataItem")


@_attrs_define
class GetCatalogCategoryUpdateJobResponseCompoundDocumentDataRelationshipsCategoriesDataItem:
    """
    Attributes:
        type (CatalogCategoryEnum):
        id (str): IDs of the updated catalog categories. Example: $custom:::$default:::SAMPLE-DATA-CATEGORY-APPAREL.
    """

    type: CatalogCategoryEnum
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = CatalogCategoryEnum(d.pop("type"))

        id = d.pop("id")

        get_catalog_category_update_job_response_compound_document_data_relationships_categories_data_item = cls(
            type=type,
            id=id,
        )

        get_catalog_category_update_job_response_compound_document_data_relationships_categories_data_item.additional_properties = d
        return get_catalog_category_update_job_response_compound_document_data_relationships_categories_data_item

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
