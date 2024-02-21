from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_enum import TagEnum

T = TypeVar("T", bound="GetTagGroupTagRelationshipsResponseCollectionDataItem")


@_attrs_define
class GetTagGroupTagRelationshipsResponseCollectionDataItem:
    """
    Attributes:
        type (TagEnum):
        id (str): The IDs of the Tags that are associated with the Tag Group Example:
            ['abcd1234-ef56-gh78-ij90-abcdef123456', 'klmn1234-op56-qr78-st90-klmnop123456'].
    """

    type: TagEnum
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = TagEnum(d.pop("type"))

        id = d.pop("id")

        get_tag_group_tag_relationships_response_collection_data_item = cls(
            type=type,
            id=id,
        )

        get_tag_group_tag_relationships_response_collection_data_item.additional_properties = d
        return get_tag_group_tag_relationships_response_collection_data_item

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
