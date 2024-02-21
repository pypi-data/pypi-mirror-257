from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_privacy_profile_query_resource_object import DataPrivacyProfileQueryResourceObject


T = TypeVar("T", bound="DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile")


@_attrs_define
class DataPrivacyCreateDeletionJobQueryResourceObjectAttributesProfile:
    """
    Attributes:
        data (DataPrivacyProfileQueryResourceObject):
    """

    data: "DataPrivacyProfileQueryResourceObject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_privacy_profile_query_resource_object import DataPrivacyProfileQueryResourceObject

        d = src_dict.copy()
        data = DataPrivacyProfileQueryResourceObject.from_dict(d.pop("data"))

        data_privacy_create_deletion_job_query_resource_object_attributes_profile = cls(
            data=data,
        )

        data_privacy_create_deletion_job_query_resource_object_attributes_profile.additional_properties = d
        return data_privacy_create_deletion_job_query_resource_object_attributes_profile

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
