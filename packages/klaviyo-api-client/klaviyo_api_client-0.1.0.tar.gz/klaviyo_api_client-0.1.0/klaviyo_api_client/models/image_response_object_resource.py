from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.image_enum import ImageEnum

if TYPE_CHECKING:
    from ..models.image_response_object_resource_attributes import ImageResponseObjectResourceAttributes
    from ..models.object_links import ObjectLinks


T = TypeVar("T", bound="ImageResponseObjectResource")


@_attrs_define
class ImageResponseObjectResource:
    """
    Attributes:
        type (ImageEnum):
        id (str): The ID of the image Example: 7.
        attributes (ImageResponseObjectResourceAttributes):
        links (ObjectLinks):
    """

    type: ImageEnum
    id: str
    attributes: "ImageResponseObjectResourceAttributes"
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
        from ..models.image_response_object_resource_attributes import ImageResponseObjectResourceAttributes
        from ..models.object_links import ObjectLinks

        d = src_dict.copy()
        type = ImageEnum(d.pop("type"))

        id = d.pop("id")

        attributes = ImageResponseObjectResourceAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        image_response_object_resource = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
        )

        image_response_object_resource.additional_properties = d
        return image_response_object_resource

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
