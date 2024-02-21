from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagGroupCreateQueryResourceObjectAttributes")


@_attrs_define
class TagGroupCreateQueryResourceObjectAttributes:
    """
    Attributes:
        name (str): The Tag Group name Example: My Tag Group.
        exclusive (Union[Unset, bool]):  Default: False.
    """

    name: str
    exclusive: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        exclusive = self.exclusive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        exclusive = d.pop("exclusive", UNSET)

        tag_group_create_query_resource_object_attributes = cls(
            name=name,
            exclusive=exclusive,
        )

        tag_group_create_query_resource_object_attributes.additional_properties = d
        return tag_group_create_query_resource_object_attributes

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
