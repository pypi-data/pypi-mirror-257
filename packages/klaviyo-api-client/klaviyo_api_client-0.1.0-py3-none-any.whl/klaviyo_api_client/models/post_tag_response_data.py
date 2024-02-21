from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_enum import TagEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.object_links import ObjectLinks
    from ..models.post_tag_response_data_attributes import PostTagResponseDataAttributes
    from ..models.post_tag_response_data_relationships import PostTagResponseDataRelationships


T = TypeVar("T", bound="PostTagResponseData")


@_attrs_define
class PostTagResponseData:
    """
    Attributes:
        type (TagEnum):
        id (str): The Tag ID Example: abcd1234-ef56-gh78-ij90-abcdef123456.
        attributes (PostTagResponseDataAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, PostTagResponseDataRelationships]):
    """

    type: TagEnum
    id: str
    attributes: "PostTagResponseDataAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "PostTagResponseDataRelationships"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        links = self.links.to_dict()

        relationships: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
                "attributes": attributes,
                "links": links,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.object_links import ObjectLinks
        from ..models.post_tag_response_data_attributes import PostTagResponseDataAttributes
        from ..models.post_tag_response_data_relationships import PostTagResponseDataRelationships

        d = src_dict.copy()
        type = TagEnum(d.pop("type"))

        id = d.pop("id")

        attributes = PostTagResponseDataAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, PostTagResponseDataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = PostTagResponseDataRelationships.from_dict(_relationships)

        post_tag_response_data = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        post_tag_response_data.additional_properties = d
        return post_tag_response_data

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
