from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_privacy_deletion_job_enum import DataPrivacyDeletionJobEnum

if TYPE_CHECKING:
    from ..models.data_privacy_create_deletion_job_query_resource_object_attributes import (
        DataPrivacyCreateDeletionJobQueryResourceObjectAttributes,
    )


T = TypeVar("T", bound="DataPrivacyCreateDeletionJobQueryResourceObject")


@_attrs_define
class DataPrivacyCreateDeletionJobQueryResourceObject:
    """
    Attributes:
        type (DataPrivacyDeletionJobEnum):
        attributes (DataPrivacyCreateDeletionJobQueryResourceObjectAttributes):
    """

    type: DataPrivacyDeletionJobEnum
    attributes: "DataPrivacyCreateDeletionJobQueryResourceObjectAttributes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        attributes = self.attributes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_privacy_create_deletion_job_query_resource_object_attributes import (
            DataPrivacyCreateDeletionJobQueryResourceObjectAttributes,
        )

        d = src_dict.copy()
        type = DataPrivacyDeletionJobEnum(d.pop("type"))

        attributes = DataPrivacyCreateDeletionJobQueryResourceObjectAttributes.from_dict(d.pop("attributes"))

        data_privacy_create_deletion_job_query_resource_object = cls(
            type=type,
            attributes=attributes,
        )

        data_privacy_create_deletion_job_query_resource_object.additional_properties = d
        return data_privacy_create_deletion_job_query_resource_object

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
