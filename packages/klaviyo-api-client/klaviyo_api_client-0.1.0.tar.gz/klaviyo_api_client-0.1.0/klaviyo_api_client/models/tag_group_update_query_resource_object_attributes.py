from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagGroupUpdateQueryResourceObjectAttributes")


@_attrs_define
class TagGroupUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        name (str): The Tag Group name Example: My Tag Group.
        return_fields (Union[Unset, List[str]]):
    """

    name: str
    return_fields: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        return_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.return_fields, Unset):
            return_fields = self.return_fields

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if return_fields is not UNSET:
            field_dict["return_fields"] = return_fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        return_fields = cast(List[str], d.pop("return_fields", UNSET))

        tag_group_update_query_resource_object_attributes = cls(
            name=name,
            return_fields=return_fields,
        )

        tag_group_update_query_resource_object_attributes.additional_properties = d
        return tag_group_update_query_resource_object_attributes

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
