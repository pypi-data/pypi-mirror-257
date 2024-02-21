from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_group_enum import TagGroupEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delete_tag_group_response_data_attributes import DeleteTagGroupResponseDataAttributes
    from ..models.delete_tag_group_response_data_relationships import DeleteTagGroupResponseDataRelationships
    from ..models.object_links import ObjectLinks


T = TypeVar("T", bound="DeleteTagGroupResponseData")


@_attrs_define
class DeleteTagGroupResponseData:
    """
    Attributes:
        type (TagGroupEnum):
        id (str): The Tag Group ID Example: zyxw9876-vu54-ts32-rq10-zyxwvu654321.
        attributes (DeleteTagGroupResponseDataAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, DeleteTagGroupResponseDataRelationships]):
    """

    type: TagGroupEnum
    id: str
    attributes: "DeleteTagGroupResponseDataAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "DeleteTagGroupResponseDataRelationships"] = UNSET
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
        from ..models.delete_tag_group_response_data_attributes import DeleteTagGroupResponseDataAttributes
        from ..models.delete_tag_group_response_data_relationships import DeleteTagGroupResponseDataRelationships
        from ..models.object_links import ObjectLinks

        d = src_dict.copy()
        type = TagGroupEnum(d.pop("type"))

        id = d.pop("id")

        attributes = DeleteTagGroupResponseDataAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, DeleteTagGroupResponseDataRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = DeleteTagGroupResponseDataRelationships.from_dict(_relationships)

        delete_tag_group_response_data = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        delete_tag_group_response_data.additional_properties = d
        return delete_tag_group_response_data

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
