from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CampaignSendJobPartialUpdateQueryResourceObjectAttributes")


@_attrs_define
class CampaignSendJobPartialUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        action (str): The action you would like to take with this send job from among 'cancel' and 'revert' Example:
            cancel.
    """

    action: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = d.pop("action")

        campaign_send_job_partial_update_query_resource_object_attributes = cls(
            action=action,
        )

        campaign_send_job_partial_update_query_resource_object_attributes.additional_properties = d
        return campaign_send_job_partial_update_query_resource_object_attributes

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
