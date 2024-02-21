from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_tag_group_response_data_relationships_tags import PostTagGroupResponseDataRelationshipsTags


T = TypeVar("T", bound="PostTagGroupResponseDataRelationships")


@_attrs_define
class PostTagGroupResponseDataRelationships:
    """
    Attributes:
        tags (Union[Unset, PostTagGroupResponseDataRelationshipsTags]):
    """

    tags: Union[Unset, "PostTagGroupResponseDataRelationshipsTags"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_tag_group_response_data_relationships_tags import PostTagGroupResponseDataRelationshipsTags

        d = src_dict.copy()
        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PostTagGroupResponseDataRelationshipsTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PostTagGroupResponseDataRelationshipsTags.from_dict(_tags)

        post_tag_group_response_data_relationships = cls(
            tags=tags,
        )

        post_tag_group_response_data_relationships.additional_properties = d
        return post_tag_group_response_data_relationships

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
