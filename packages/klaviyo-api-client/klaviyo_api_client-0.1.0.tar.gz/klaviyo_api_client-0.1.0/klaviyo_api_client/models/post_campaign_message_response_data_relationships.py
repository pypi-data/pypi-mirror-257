from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_campaign_message_response_data_relationships_campaign import (
        PostCampaignMessageResponseDataRelationshipsCampaign,
    )
    from ..models.post_campaign_message_response_data_relationships_template import (
        PostCampaignMessageResponseDataRelationshipsTemplate,
    )


T = TypeVar("T", bound="PostCampaignMessageResponseDataRelationships")


@_attrs_define
class PostCampaignMessageResponseDataRelationships:
    """
    Attributes:
        campaign (Union[Unset, PostCampaignMessageResponseDataRelationshipsCampaign]):
        template (Union[Unset, PostCampaignMessageResponseDataRelationshipsTemplate]):
    """

    campaign: Union[Unset, "PostCampaignMessageResponseDataRelationshipsCampaign"] = UNSET
    template: Union[Unset, "PostCampaignMessageResponseDataRelationshipsTemplate"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        campaign: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaign, Unset):
            campaign = self.campaign.to_dict()

        template: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if campaign is not UNSET:
            field_dict["campaign"] = campaign
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_campaign_message_response_data_relationships_campaign import (
            PostCampaignMessageResponseDataRelationshipsCampaign,
        )
        from ..models.post_campaign_message_response_data_relationships_template import (
            PostCampaignMessageResponseDataRelationshipsTemplate,
        )

        d = src_dict.copy()
        _campaign = d.pop("campaign", UNSET)
        campaign: Union[Unset, PostCampaignMessageResponseDataRelationshipsCampaign]
        if isinstance(_campaign, Unset):
            campaign = UNSET
        else:
            campaign = PostCampaignMessageResponseDataRelationshipsCampaign.from_dict(_campaign)

        _template = d.pop("template", UNSET)
        template: Union[Unset, PostCampaignMessageResponseDataRelationshipsTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = PostCampaignMessageResponseDataRelationshipsTemplate.from_dict(_template)

        post_campaign_message_response_data_relationships = cls(
            campaign=campaign,
            template=template,
        )

        post_campaign_message_response_data_relationships.additional_properties = d
        return post_campaign_message_response_data_relationships

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
