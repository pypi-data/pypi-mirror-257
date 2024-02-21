from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CampaignRecipientEstimationResponseObjectResourceAttributes")


@_attrs_define
class CampaignRecipientEstimationResponseObjectResourceAttributes:
    """
    Attributes:
        estimated_recipient_count (int): The estimated number of unique recipients the campaign will send to
    """

    estimated_recipient_count: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        estimated_recipient_count = self.estimated_recipient_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "estimated_recipient_count": estimated_recipient_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        estimated_recipient_count = d.pop("estimated_recipient_count")

        campaign_recipient_estimation_response_object_resource_attributes = cls(
            estimated_recipient_count=estimated_recipient_count,
        )

        campaign_recipient_estimation_response_object_resource_attributes.additional_properties = d
        return campaign_recipient_estimation_response_object_resource_attributes

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
