from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_privacy_create_deletion_job_query_resource_object_attributes_profile import (
        DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile,
    )


T = TypeVar("T", bound="DataPrivacyCreateDeletionJobQueryResourceObjectAttributes")


@_attrs_define
class DataPrivacyCreateDeletionJobQueryResourceObjectAttributes:
    """
    Attributes:
        profile (DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile):
    """

    profile: "DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile = self.profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_privacy_create_deletion_job_query_resource_object_attributes_profile import (
            DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile,
        )

        d = src_dict.copy()
        profile = DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile.from_dict(d.pop("profile"))

        data_privacy_create_deletion_job_query_resource_object_attributes = cls(
            profile=profile,
        )

        data_privacy_create_deletion_job_query_resource_object_attributes.additional_properties = d
        return data_privacy_create_deletion_job_query_resource_object_attributes

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
