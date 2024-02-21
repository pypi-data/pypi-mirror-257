from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_campaign_response_data_relationships_campaign_messages import (
        PostCampaignResponseDataRelationshipsCampaignMessages,
    )
    from ..models.post_campaign_response_data_relationships_tags import PostCampaignResponseDataRelationshipsTags


T = TypeVar("T", bound="PostCampaignResponseDataRelationships")


@_attrs_define
class PostCampaignResponseDataRelationships:
    """
    Attributes:
        campaign_messages (Union[Unset, PostCampaignResponseDataRelationshipsCampaignMessages]):
        tags (Union[Unset, PostCampaignResponseDataRelationshipsTags]):
    """

    campaign_messages: Union[Unset, "PostCampaignResponseDataRelationshipsCampaignMessages"] = UNSET
    tags: Union[Unset, "PostCampaignResponseDataRelationshipsTags"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        campaign_messages: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaign_messages, Unset):
            campaign_messages = self.campaign_messages.to_dict()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if campaign_messages is not UNSET:
            field_dict["campaign-messages"] = campaign_messages
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_campaign_response_data_relationships_campaign_messages import (
            PostCampaignResponseDataRelationshipsCampaignMessages,
        )
        from ..models.post_campaign_response_data_relationships_tags import PostCampaignResponseDataRelationshipsTags

        d = src_dict.copy()
        _campaign_messages = d.pop("campaign-messages", UNSET)
        campaign_messages: Union[Unset, PostCampaignResponseDataRelationshipsCampaignMessages]
        if isinstance(_campaign_messages, Unset):
            campaign_messages = UNSET
        else:
            campaign_messages = PostCampaignResponseDataRelationshipsCampaignMessages.from_dict(_campaign_messages)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PostCampaignResponseDataRelationshipsTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PostCampaignResponseDataRelationshipsTags.from_dict(_tags)

        post_campaign_response_data_relationships = cls(
            campaign_messages=campaign_messages,
            tags=tags,
        )

        post_campaign_response_data_relationships.additional_properties = d
        return post_campaign_response_data_relationships

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
