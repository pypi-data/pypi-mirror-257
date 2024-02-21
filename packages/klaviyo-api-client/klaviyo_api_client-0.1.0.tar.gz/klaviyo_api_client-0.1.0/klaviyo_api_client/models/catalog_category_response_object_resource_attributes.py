import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CatalogCategoryResponseObjectResourceAttributes")


@_attrs_define
class CatalogCategoryResponseObjectResourceAttributes:
    """
    Attributes:
        external_id (Union[Unset, str]): The ID of the catalog category in an external system. Example: SAMPLE-DATA-
            CATEGORY-APPAREL.
        name (Union[Unset, str]): The name of the catalog category. Example: Sample Data Category Apparel.
        updated (Union[Unset, datetime.datetime]): Date and time when the catalog category was last updated, in ISO 8601
            format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
    """

    external_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id

        name = self.name

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if name is not UNSET:
            field_dict["name"] = name
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        external_id = d.pop("external_id", UNSET)

        name = d.pop("name", UNSET)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        catalog_category_response_object_resource_attributes = cls(
            external_id=external_id,
            name=name,
            updated=updated,
        )

        catalog_category_response_object_resource_attributes.additional_properties = d
        return catalog_category_response_object_resource_attributes

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
