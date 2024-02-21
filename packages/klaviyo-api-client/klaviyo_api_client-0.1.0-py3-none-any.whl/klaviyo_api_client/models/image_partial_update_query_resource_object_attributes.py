from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImagePartialUpdateQueryResourceObjectAttributes")


@_attrs_define
class ImagePartialUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        name (Union[Unset, str]): A name for the image.
        hidden (Union[Unset, bool]): If true, this image is not shown in the asset library.
    """

    name: Union[Unset, str] = UNSET
    hidden: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        hidden = self.hidden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if hidden is not UNSET:
            field_dict["hidden"] = hidden

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        hidden = d.pop("hidden", UNSET)

        image_partial_update_query_resource_object_attributes = cls(
            name=name,
            hidden=hidden,
        )

        image_partial_update_query_resource_object_attributes.additional_properties = d
        return image_partial_update_query_resource_object_attributes

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
