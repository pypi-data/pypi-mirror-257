from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_group_enum import TagGroupEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_tag_group_response_collection_data_item_relationships import (
        GetTagGroupResponseCollectionDataItemRelationships,
    )
    from ..models.object_links import ObjectLinks
    from ..models.tag_group_response_object_resource_attributes import TagGroupResponseObjectResourceAttributes


T = TypeVar("T", bound="GetTagGroupResponseCollectionDataItem")


@_attrs_define
class GetTagGroupResponseCollectionDataItem:
    """
    Attributes:
        type (TagGroupEnum):
        id (str): The Tag Group ID Example: zyxw9876-vu54-ts32-rq10-zyxwvu654321.
        attributes (TagGroupResponseObjectResourceAttributes):
        links (ObjectLinks):
        relationships (Union[Unset, GetTagGroupResponseCollectionDataItemRelationships]):
    """

    type: TagGroupEnum
    id: str
    attributes: "TagGroupResponseObjectResourceAttributes"
    links: "ObjectLinks"
    relationships: Union[Unset, "GetTagGroupResponseCollectionDataItemRelationships"] = UNSET
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
        from ..models.get_tag_group_response_collection_data_item_relationships import (
            GetTagGroupResponseCollectionDataItemRelationships,
        )
        from ..models.object_links import ObjectLinks
        from ..models.tag_group_response_object_resource_attributes import TagGroupResponseObjectResourceAttributes

        d = src_dict.copy()
        type = TagGroupEnum(d.pop("type"))

        id = d.pop("id")

        attributes = TagGroupResponseObjectResourceAttributes.from_dict(d.pop("attributes"))

        links = ObjectLinks.from_dict(d.pop("links"))

        _relationships = d.pop("relationships", UNSET)
        relationships: Union[Unset, GetTagGroupResponseCollectionDataItemRelationships]
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = GetTagGroupResponseCollectionDataItemRelationships.from_dict(_relationships)

        get_tag_group_response_collection_data_item = cls(
            type=type,
            id=id,
            attributes=attributes,
            links=links,
            relationships=relationships,
        )

        get_tag_group_response_collection_data_item.additional_properties = d
        return get_tag_group_response_collection_data_item

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
