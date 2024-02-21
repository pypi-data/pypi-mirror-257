from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tag_create_query_resource_object_relationships_tag_group import (
        TagCreateQueryResourceObjectRelationshipsTagGroup,
    )


T = TypeVar("T", bound="TagCreateQueryResourceObjectRelationships")


@_attrs_define
class TagCreateQueryResourceObjectRelationships:
    """
    Attributes:
        tag_group (Union[Unset, TagCreateQueryResourceObjectRelationshipsTagGroup]):
    """

    tag_group: Union[Unset, "TagCreateQueryResourceObjectRelationshipsTagGroup"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tag_group, Unset):
            tag_group = self.tag_group.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tag_group is not UNSET:
            field_dict["tag-group"] = tag_group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tag_create_query_resource_object_relationships_tag_group import (
            TagCreateQueryResourceObjectRelationshipsTagGroup,
        )

        d = src_dict.copy()
        _tag_group = d.pop("tag-group", UNSET)
        tag_group: Union[Unset, TagCreateQueryResourceObjectRelationshipsTagGroup]
        if isinstance(_tag_group, Unset):
            tag_group = UNSET
        else:
            tag_group = TagCreateQueryResourceObjectRelationshipsTagGroup.from_dict(_tag_group)

        tag_create_query_resource_object_relationships = cls(
            tag_group=tag_group,
        )

        tag_create_query_resource_object_relationships.additional_properties = d
        return tag_create_query_resource_object_relationships

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
