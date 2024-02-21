from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.profile_import_job_create_query_resource_object_attributes_profiles import (
        ProfileImportJobCreateQueryResourceObjectAttributesProfiles,
    )


T = TypeVar("T", bound="ProfileImportJobCreateQueryResourceObjectAttributes")


@_attrs_define
class ProfileImportJobCreateQueryResourceObjectAttributes:
    """
    Attributes:
        profiles (ProfileImportJobCreateQueryResourceObjectAttributesProfiles): Array of profiles to create or update
    """

    profiles: "ProfileImportJobCreateQueryResourceObjectAttributesProfiles"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profiles = self.profiles.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profiles": profiles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_import_job_create_query_resource_object_attributes_profiles import (
            ProfileImportJobCreateQueryResourceObjectAttributesProfiles,
        )

        d = src_dict.copy()
        profiles = ProfileImportJobCreateQueryResourceObjectAttributesProfiles.from_dict(d.pop("profiles"))

        profile_import_job_create_query_resource_object_attributes = cls(
            profiles=profiles,
        )

        profile_import_job_create_query_resource_object_attributes.additional_properties = d
        return profile_import_job_create_query_resource_object_attributes

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
