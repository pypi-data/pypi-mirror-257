from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.suppression_delete_job_create_query_resource_object_attributes_profiles import (
        SuppressionDeleteJobCreateQueryResourceObjectAttributesProfiles,
    )


T = TypeVar("T", bound="SuppressionDeleteJobCreateQueryResourceObjectAttributes")


@_attrs_define
class SuppressionDeleteJobCreateQueryResourceObjectAttributes:
    """
    Attributes:
        profiles (SuppressionDeleteJobCreateQueryResourceObjectAttributesProfiles): The profile(s) to remove
            suppressions for.
    """

    profiles: "SuppressionDeleteJobCreateQueryResourceObjectAttributesProfiles"
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
        from ..models.suppression_delete_job_create_query_resource_object_attributes_profiles import (
            SuppressionDeleteJobCreateQueryResourceObjectAttributesProfiles,
        )

        d = src_dict.copy()
        profiles = SuppressionDeleteJobCreateQueryResourceObjectAttributesProfiles.from_dict(d.pop("profiles"))

        suppression_delete_job_create_query_resource_object_attributes = cls(
            profiles=profiles,
        )

        suppression_delete_job_create_query_resource_object_attributes.additional_properties = d
        return suppression_delete_job_create_query_resource_object_attributes

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
