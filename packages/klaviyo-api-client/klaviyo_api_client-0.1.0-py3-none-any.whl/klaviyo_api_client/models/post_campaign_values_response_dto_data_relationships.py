from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_campaign_values_response_dto_data_relationships_campaigns import (
        PostCampaignValuesResponseDTODataRelationshipsCampaigns,
    )


T = TypeVar("T", bound="PostCampaignValuesResponseDTODataRelationships")


@_attrs_define
class PostCampaignValuesResponseDTODataRelationships:
    """
    Attributes:
        campaigns (Union[Unset, PostCampaignValuesResponseDTODataRelationshipsCampaigns]):
    """

    campaigns: Union[Unset, "PostCampaignValuesResponseDTODataRelationshipsCampaigns"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        campaigns: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaigns, Unset):
            campaigns = self.campaigns.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if campaigns is not UNSET:
            field_dict["campaigns"] = campaigns

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_campaign_values_response_dto_data_relationships_campaigns import (
            PostCampaignValuesResponseDTODataRelationshipsCampaigns,
        )

        d = src_dict.copy()
        _campaigns = d.pop("campaigns", UNSET)
        campaigns: Union[Unset, PostCampaignValuesResponseDTODataRelationshipsCampaigns]
        if isinstance(_campaigns, Unset):
            campaigns = UNSET
        else:
            campaigns = PostCampaignValuesResponseDTODataRelationshipsCampaigns.from_dict(_campaigns)

        post_campaign_values_response_dto_data_relationships = cls(
            campaigns=campaigns,
        )

        post_campaign_values_response_dto_data_relationships.additional_properties = d
        return post_campaign_values_response_dto_data_relationships

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
