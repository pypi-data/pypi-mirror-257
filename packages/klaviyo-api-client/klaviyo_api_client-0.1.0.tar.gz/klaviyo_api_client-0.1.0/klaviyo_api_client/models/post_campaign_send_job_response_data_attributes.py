from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_campaign_send_job_response_data_attributes_status import (
    PostCampaignSendJobResponseDataAttributesStatus,
)

T = TypeVar("T", bound="PostCampaignSendJobResponseDataAttributes")


@_attrs_define
class PostCampaignSendJobResponseDataAttributes:
    """
    Attributes:
        status (PostCampaignSendJobResponseDataAttributesStatus): The status of the send job
    """

    status: PostCampaignSendJobResponseDataAttributesStatus
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = PostCampaignSendJobResponseDataAttributesStatus(d.pop("status"))

        post_campaign_send_job_response_data_attributes = cls(
            status=status,
        )

        post_campaign_send_job_response_data_attributes.additional_properties = d
        return post_campaign_send_job_response_data_attributes

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
