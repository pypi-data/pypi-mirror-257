from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.catalog_category_update_query_resource_object import CatalogCategoryUpdateQueryResourceObject


T = TypeVar("T", bound="CatalogCategoryUpdateQuery")


@_attrs_define
class CatalogCategoryUpdateQuery:
    """
    Attributes:
        data (CatalogCategoryUpdateQueryResourceObject):
    """

    data: "CatalogCategoryUpdateQueryResourceObject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_category_update_query_resource_object import CatalogCategoryUpdateQueryResourceObject

        d = src_dict.copy()
        data = CatalogCategoryUpdateQueryResourceObject.from_dict(d.pop("data"))

        catalog_category_update_query = cls(
            data=data,
        )

        catalog_category_update_query.additional_properties = d
        return catalog_category_update_query

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
