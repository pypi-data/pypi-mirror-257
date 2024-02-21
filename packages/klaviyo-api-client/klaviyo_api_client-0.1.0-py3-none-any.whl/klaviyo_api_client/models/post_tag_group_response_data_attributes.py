from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PostTagGroupResponseDataAttributes")


@_attrs_define
class PostTagGroupResponseDataAttributes:
    """
    Attributes:
        name (str): The Tag Group name Example: My Tag Group.
        exclusive (bool): If a tag group is non-exclusive, any given related resource (campaign, flow, etc.) can be
            linked to multiple tags from that tag group. If a tag group is exclusive, any given related resource can only be
            linked to one tag from that tag group.
        default (bool): Every company automatically has one Default Tag Group. The Default Tag Group cannot be deleted,
            and no other Default Tag Groups can be created. This value is true for the Default Tag Group and false for all
            other Tag Groups.
    """

    name: str
    exclusive: bool
    default: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        exclusive = self.exclusive

        default = self.default

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "exclusive": exclusive,
                "default": default,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        exclusive = d.pop("exclusive")

        default = d.pop("default")

        post_tag_group_response_data_attributes = cls(
            name=name,
            exclusive=exclusive,
            default=default,
        )

        post_tag_group_response_data_attributes.additional_properties = d
        return post_tag_group_response_data_attributes

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
