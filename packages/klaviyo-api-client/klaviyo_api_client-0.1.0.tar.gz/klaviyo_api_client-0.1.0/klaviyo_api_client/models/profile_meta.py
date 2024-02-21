from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_meta_patch_properties import ProfileMetaPatchProperties


T = TypeVar("T", bound="ProfileMeta")


@_attrs_define
class ProfileMeta:
    """
    Attributes:
        patch_properties (Union[Unset, ProfileMetaPatchProperties]):
    """

    patch_properties: Union[Unset, "ProfileMetaPatchProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        patch_properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.patch_properties, Unset):
            patch_properties = self.patch_properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if patch_properties is not UNSET:
            field_dict["patch_properties"] = patch_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_meta_patch_properties import ProfileMetaPatchProperties

        d = src_dict.copy()
        _patch_properties = d.pop("patch_properties", UNSET)
        patch_properties: Union[Unset, ProfileMetaPatchProperties]
        if isinstance(_patch_properties, Unset):
            patch_properties = UNSET
        else:
            patch_properties = ProfileMetaPatchProperties.from_dict(_patch_properties)

        profile_meta = cls(
            patch_properties=patch_properties,
        )

        profile_meta.additional_properties = d
        return profile_meta

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
