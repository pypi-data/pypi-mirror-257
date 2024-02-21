from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_enum import TagEnum

if TYPE_CHECKING:
    from ..models.object_links import ObjectLinks
    from ..models.tag_response_object_resource_attributes import TagResponseObjectResourceAttributes


T = TypeVar("T", bound="TagResponseObjectResource")


@_attrs_define
class TagResponseObjectResource:
    """
    Attributes:
        type (TagEnum):
        id (str): The Tag ID Example: abcd1234-ef56-gh78-ij90-abcdef123456.
        attributes (TagResponseObjectResourceAttributes):
        links (ObjectLinks):
    """

    type: TagEnum
    id: str
    attributes: "TagResponseObjectResourceAttributes"
    links: "ObjectLinks"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        attributes = self.attributes.to_dict()

        links = self.links.to_dict()

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.object_links import ObjectLinks
        from ..models.tag_response_object_resource_attributes import TagResponseObjectResourceAttributes

        d = src_dict.copy()
        type = TagEnum(d.pop("type"))

        id = d.pop("id")

        attributes = TagResponseObjectResourceAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        tag_response_object_resource = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
        )

        tag_response_object_resource.additional_properties = d
        return tag_response_object_resource

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
