from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.campaign_enum import CampaignEnum

T = TypeVar("T", bound="PostCampaignMessageResponseDataRelationshipsCampaignData")


@_attrs_define
class PostCampaignMessageResponseDataRelationshipsCampaignData:
    """
    Attributes:
        type (CampaignEnum):
        id (str): The parent campaign id
    """

    type: CampaignEnum
    id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = CampaignEnum(d.pop("type"))

        id = d.pop("id")

        post_campaign_message_response_data_relationships_campaign_data = cls(
            type=type,
            id=id,
        )

        post_campaign_message_response_data_relationships_campaign_data.additional_properties = d
        return post_campaign_message_response_data_relationships_campaign_data

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
