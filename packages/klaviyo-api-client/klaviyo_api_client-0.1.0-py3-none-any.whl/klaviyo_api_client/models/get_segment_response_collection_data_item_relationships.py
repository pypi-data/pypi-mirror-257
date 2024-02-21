from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_segment_response_collection_data_item_relationships_profiles import (
        GetSegmentResponseCollectionDataItemRelationshipsProfiles,
    )
    from ..models.get_segment_response_collection_data_item_relationships_tags import (
        GetSegmentResponseCollectionDataItemRelationshipsTags,
    )


T = TypeVar("T", bound="GetSegmentResponseCollectionDataItemRelationships")


@_attrs_define
class GetSegmentResponseCollectionDataItemRelationships:
    """
    Attributes:
        profiles (Union[Unset, GetSegmentResponseCollectionDataItemRelationshipsProfiles]):
        tags (Union[Unset, GetSegmentResponseCollectionDataItemRelationshipsTags]):
    """

    profiles: Union[Unset, "GetSegmentResponseCollectionDataItemRelationshipsProfiles"] = UNSET
    tags: Union[Unset, "GetSegmentResponseCollectionDataItemRelationshipsTags"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profiles: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = self.profiles.to_dict()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profiles is not UNSET:
            field_dict["profiles"] = profiles
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_segment_response_collection_data_item_relationships_profiles import (
            GetSegmentResponseCollectionDataItemRelationshipsProfiles,
        )
        from ..models.get_segment_response_collection_data_item_relationships_tags import (
            GetSegmentResponseCollectionDataItemRelationshipsTags,
        )

        d = src_dict.copy()
        _profiles = d.pop("profiles", UNSET)
        profiles: Union[Unset, GetSegmentResponseCollectionDataItemRelationshipsProfiles]
        if isinstance(_profiles, Unset):
            profiles = UNSET
        else:
            profiles = GetSegmentResponseCollectionDataItemRelationshipsProfiles.from_dict(_profiles)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, GetSegmentResponseCollectionDataItemRelationshipsTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = GetSegmentResponseCollectionDataItemRelationshipsTags.from_dict(_tags)

        get_segment_response_collection_data_item_relationships = cls(
            profiles=profiles,
            tags=tags,
        )

        get_segment_response_collection_data_item_relationships.additional_properties = d
        return get_segment_response_collection_data_item_relationships

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
