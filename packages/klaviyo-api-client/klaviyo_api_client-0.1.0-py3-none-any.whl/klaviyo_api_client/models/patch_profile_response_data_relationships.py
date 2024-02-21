from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_profile_response_data_relationships_lists import PatchProfileResponseDataRelationshipsLists
    from ..models.patch_profile_response_data_relationships_segments import (
        PatchProfileResponseDataRelationshipsSegments,
    )


T = TypeVar("T", bound="PatchProfileResponseDataRelationships")


@_attrs_define
class PatchProfileResponseDataRelationships:
    """
    Attributes:
        lists (Union[Unset, PatchProfileResponseDataRelationshipsLists]):
        segments (Union[Unset, PatchProfileResponseDataRelationshipsSegments]):
    """

    lists: Union[Unset, "PatchProfileResponseDataRelationshipsLists"] = UNSET
    segments: Union[Unset, "PatchProfileResponseDataRelationshipsSegments"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lists: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lists, Unset):
            lists = self.lists.to_dict()

        segments: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.segments, Unset):
            segments = self.segments.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lists is not UNSET:
            field_dict["lists"] = lists
        if segments is not UNSET:
            field_dict["segments"] = segments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patch_profile_response_data_relationships_lists import PatchProfileResponseDataRelationshipsLists
        from ..models.patch_profile_response_data_relationships_segments import (
            PatchProfileResponseDataRelationshipsSegments,
        )

        d = src_dict.copy()
        _lists = d.pop("lists", UNSET)
        lists: Union[Unset, PatchProfileResponseDataRelationshipsLists]
        if isinstance(_lists, Unset):
            lists = UNSET
        else:
            lists = PatchProfileResponseDataRelationshipsLists.from_dict(_lists)

        _segments = d.pop("segments", UNSET)
        segments: Union[Unset, PatchProfileResponseDataRelationshipsSegments]
        if isinstance(_segments, Unset):
            segments = UNSET
        else:
            segments = PatchProfileResponseDataRelationshipsSegments.from_dict(_segments)

        patch_profile_response_data_relationships = cls(
            lists=lists,
            segments=segments,
        )

        patch_profile_response_data_relationships.additional_properties = d
        return patch_profile_response_data_relationships

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
