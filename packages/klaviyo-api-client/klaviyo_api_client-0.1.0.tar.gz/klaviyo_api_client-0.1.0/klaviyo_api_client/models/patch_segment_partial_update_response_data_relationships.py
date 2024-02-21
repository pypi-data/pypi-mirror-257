from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_segment_partial_update_response_data_relationships_profiles import (
        PatchSegmentPartialUpdateResponseDataRelationshipsProfiles,
    )
    from ..models.patch_segment_partial_update_response_data_relationships_tags import (
        PatchSegmentPartialUpdateResponseDataRelationshipsTags,
    )


T = TypeVar("T", bound="PatchSegmentPartialUpdateResponseDataRelationships")


@_attrs_define
class PatchSegmentPartialUpdateResponseDataRelationships:
    """
    Attributes:
        profiles (Union[Unset, PatchSegmentPartialUpdateResponseDataRelationshipsProfiles]):
        tags (Union[Unset, PatchSegmentPartialUpdateResponseDataRelationshipsTags]):
    """

    profiles: Union[Unset, "PatchSegmentPartialUpdateResponseDataRelationshipsProfiles"] = UNSET
    tags: Union[Unset, "PatchSegmentPartialUpdateResponseDataRelationshipsTags"] = UNSET
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
        from ..models.patch_segment_partial_update_response_data_relationships_profiles import (
            PatchSegmentPartialUpdateResponseDataRelationshipsProfiles,
        )
        from ..models.patch_segment_partial_update_response_data_relationships_tags import (
            PatchSegmentPartialUpdateResponseDataRelationshipsTags,
        )

        d = src_dict.copy()
        _profiles = d.pop("profiles", UNSET)
        profiles: Union[Unset, PatchSegmentPartialUpdateResponseDataRelationshipsProfiles]
        if isinstance(_profiles, Unset):
            profiles = UNSET
        else:
            profiles = PatchSegmentPartialUpdateResponseDataRelationshipsProfiles.from_dict(_profiles)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PatchSegmentPartialUpdateResponseDataRelationshipsTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PatchSegmentPartialUpdateResponseDataRelationshipsTags.from_dict(_tags)

        patch_segment_partial_update_response_data_relationships = cls(
            profiles=profiles,
            tags=tags,
        )

        patch_segment_partial_update_response_data_relationships.additional_properties = d
        return patch_segment_partial_update_response_data_relationships

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
