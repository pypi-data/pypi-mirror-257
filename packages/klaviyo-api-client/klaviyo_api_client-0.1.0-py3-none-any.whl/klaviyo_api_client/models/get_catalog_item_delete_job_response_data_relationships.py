from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_catalog_item_delete_job_response_data_relationships_items import (
        GetCatalogItemDeleteJobResponseDataRelationshipsItems,
    )


T = TypeVar("T", bound="GetCatalogItemDeleteJobResponseDataRelationships")


@_attrs_define
class GetCatalogItemDeleteJobResponseDataRelationships:
    """
    Attributes:
        items (Union[Unset, GetCatalogItemDeleteJobResponseDataRelationshipsItems]):
    """

    items: Union[Unset, "GetCatalogItemDeleteJobResponseDataRelationshipsItems"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.items, Unset):
            items = self.items.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_catalog_item_delete_job_response_data_relationships_items import (
            GetCatalogItemDeleteJobResponseDataRelationshipsItems,
        )

        d = src_dict.copy()
        _items = d.pop("items", UNSET)
        items: Union[Unset, GetCatalogItemDeleteJobResponseDataRelationshipsItems]
        if isinstance(_items, Unset):
            items = UNSET
        else:
            items = GetCatalogItemDeleteJobResponseDataRelationshipsItems.from_dict(_items)

        get_catalog_item_delete_job_response_data_relationships = cls(
            items=items,
        )

        get_catalog_item_delete_job_response_data_relationships.additional_properties = d
        return get_catalog_item_delete_job_response_data_relationships

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
