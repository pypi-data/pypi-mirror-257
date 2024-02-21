from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.collection_links import CollectionLinks
    from ..models.get_catalog_category_response_collection_data_item import GetCatalogCategoryResponseCollectionDataItem


T = TypeVar("T", bound="GetCatalogCategoryResponseCollection")


@_attrs_define
class GetCatalogCategoryResponseCollection:
    """
    Attributes:
        data (List['GetCatalogCategoryResponseCollectionDataItem']):
        links (CollectionLinks):
    """

    data: List["GetCatalogCategoryResponseCollectionDataItem"]
    links: "CollectionLinks"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        links = self.links.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.collection_links import CollectionLinks
        from ..models.get_catalog_category_response_collection_data_item import (
            GetCatalogCategoryResponseCollectionDataItem,
        )

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = GetCatalogCategoryResponseCollectionDataItem.from_dict(data_item_data)

            data.append(data_item)

        links = CollectionLinks.from_dict(d.pop("links"))

        get_catalog_category_response_collection = cls(
            data=data,
            links=links,
        )

        get_catalog_category_response_collection.additional_properties = d
        return get_catalog_category_response_collection

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
