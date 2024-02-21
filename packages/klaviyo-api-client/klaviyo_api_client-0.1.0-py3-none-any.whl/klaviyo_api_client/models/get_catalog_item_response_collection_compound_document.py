from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_variant_response_object_resource import CatalogVariantResponseObjectResource
    from ..models.collection_links import CollectionLinks
    from ..models.get_catalog_item_response_collection_compound_document_data_item import (
        GetCatalogItemResponseCollectionCompoundDocumentDataItem,
    )


T = TypeVar("T", bound="GetCatalogItemResponseCollectionCompoundDocument")


@_attrs_define
class GetCatalogItemResponseCollectionCompoundDocument:
    """
    Attributes:
        data (List['GetCatalogItemResponseCollectionCompoundDocumentDataItem']):
        links (CollectionLinks):
        included (Union[Unset, List['CatalogVariantResponseObjectResource']]):
    """

    data: List["GetCatalogItemResponseCollectionCompoundDocumentDataItem"]
    links: "CollectionLinks"
    included: Union[Unset, List["CatalogVariantResponseObjectResource"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        links = self.links.to_dict()

        included: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.included, Unset):
            included = []
            for included_item_data in self.included:
                included_item = included_item_data.to_dict()
                included.append(included_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "links": links,
            }
        )
        if included is not UNSET:
            field_dict["included"] = included

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_variant_response_object_resource import CatalogVariantResponseObjectResource
        from ..models.collection_links import CollectionLinks
        from ..models.get_catalog_item_response_collection_compound_document_data_item import (
            GetCatalogItemResponseCollectionCompoundDocumentDataItem,
        )

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = GetCatalogItemResponseCollectionCompoundDocumentDataItem.from_dict(data_item_data)

            data.append(data_item)

        links = CollectionLinks.from_dict(d.pop("links"))

        included = []
        _included = d.pop("included", UNSET)
        for included_item_data in _included or []:
            included_item = CatalogVariantResponseObjectResource.from_dict(included_item_data)

            included.append(included_item)

        get_catalog_item_response_collection_compound_document = cls(
            data=data,
            links=links,
            included=included,
        )

        get_catalog_item_response_collection_compound_document.additional_properties = d
        return get_catalog_item_response_collection_compound_document

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
