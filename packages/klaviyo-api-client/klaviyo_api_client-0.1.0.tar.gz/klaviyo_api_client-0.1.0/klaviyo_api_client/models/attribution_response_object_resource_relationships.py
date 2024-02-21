from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attribution_response_object_resource_relationships_attributed_event import (
        AttributionResponseObjectResourceRelationshipsAttributedEvent,
    )
    from ..models.attribution_response_object_resource_relationships_campaign import (
        AttributionResponseObjectResourceRelationshipsCampaign,
    )
    from ..models.attribution_response_object_resource_relationships_campaign_message import (
        AttributionResponseObjectResourceRelationshipsCampaignMessage,
    )
    from ..models.attribution_response_object_resource_relationships_event import (
        AttributionResponseObjectResourceRelationshipsEvent,
    )
    from ..models.attribution_response_object_resource_relationships_flow import (
        AttributionResponseObjectResourceRelationshipsFlow,
    )
    from ..models.attribution_response_object_resource_relationships_flow_message import (
        AttributionResponseObjectResourceRelationshipsFlowMessage,
    )
    from ..models.attribution_response_object_resource_relationships_flow_message_variation import (
        AttributionResponseObjectResourceRelationshipsFlowMessageVariation,
    )


T = TypeVar("T", bound="AttributionResponseObjectResourceRelationships")


@_attrs_define
class AttributionResponseObjectResourceRelationships:
    """
    Attributes:
        event (Union[Unset, AttributionResponseObjectResourceRelationshipsEvent]):
        attributed_event (Union[Unset, AttributionResponseObjectResourceRelationshipsAttributedEvent]):
        campaign (Union[Unset, AttributionResponseObjectResourceRelationshipsCampaign]):
        campaign_message (Union[Unset, AttributionResponseObjectResourceRelationshipsCampaignMessage]):
        flow (Union[Unset, AttributionResponseObjectResourceRelationshipsFlow]):
        flow_message (Union[Unset, AttributionResponseObjectResourceRelationshipsFlowMessage]):
        flow_message_variation (Union[Unset, AttributionResponseObjectResourceRelationshipsFlowMessageVariation]):
    """

    event: Union[Unset, "AttributionResponseObjectResourceRelationshipsEvent"] = UNSET
    attributed_event: Union[Unset, "AttributionResponseObjectResourceRelationshipsAttributedEvent"] = UNSET
    campaign: Union[Unset, "AttributionResponseObjectResourceRelationshipsCampaign"] = UNSET
    campaign_message: Union[Unset, "AttributionResponseObjectResourceRelationshipsCampaignMessage"] = UNSET
    flow: Union[Unset, "AttributionResponseObjectResourceRelationshipsFlow"] = UNSET
    flow_message: Union[Unset, "AttributionResponseObjectResourceRelationshipsFlowMessage"] = UNSET
    flow_message_variation: Union[Unset, "AttributionResponseObjectResourceRelationshipsFlowMessageVariation"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.event, Unset):
            event = self.event.to_dict()

        attributed_event: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.attributed_event, Unset):
            attributed_event = self.attributed_event.to_dict()

        campaign: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaign, Unset):
            campaign = self.campaign.to_dict()

        campaign_message: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.campaign_message, Unset):
            campaign_message = self.campaign_message.to_dict()

        flow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow, Unset):
            flow = self.flow.to_dict()

        flow_message: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_message, Unset):
            flow_message = self.flow_message.to_dict()

        flow_message_variation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_message_variation, Unset):
            flow_message_variation = self.flow_message_variation.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if event is not UNSET:
            field_dict["event"] = event
        if attributed_event is not UNSET:
            field_dict["attributed-event"] = attributed_event
        if campaign is not UNSET:
            field_dict["campaign"] = campaign
        if campaign_message is not UNSET:
            field_dict["campaign-message"] = campaign_message
        if flow is not UNSET:
            field_dict["flow"] = flow
        if flow_message is not UNSET:
            field_dict["flow-message"] = flow_message
        if flow_message_variation is not UNSET:
            field_dict["flow-message-variation"] = flow_message_variation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.attribution_response_object_resource_relationships_attributed_event import (
            AttributionResponseObjectResourceRelationshipsAttributedEvent,
        )
        from ..models.attribution_response_object_resource_relationships_campaign import (
            AttributionResponseObjectResourceRelationshipsCampaign,
        )
        from ..models.attribution_response_object_resource_relationships_campaign_message import (
            AttributionResponseObjectResourceRelationshipsCampaignMessage,
        )
        from ..models.attribution_response_object_resource_relationships_event import (
            AttributionResponseObjectResourceRelationshipsEvent,
        )
        from ..models.attribution_response_object_resource_relationships_flow import (
            AttributionResponseObjectResourceRelationshipsFlow,
        )
        from ..models.attribution_response_object_resource_relationships_flow_message import (
            AttributionResponseObjectResourceRelationshipsFlowMessage,
        )
        from ..models.attribution_response_object_resource_relationships_flow_message_variation import (
            AttributionResponseObjectResourceRelationshipsFlowMessageVariation,
        )

        d = src_dict.copy()
        _event = d.pop("event", UNSET)
        event: Union[Unset, AttributionResponseObjectResourceRelationshipsEvent]
        if isinstance(_event, Unset):
            event = UNSET
        else:
            event = AttributionResponseObjectResourceRelationshipsEvent.from_dict(_event)

        _attributed_event = d.pop("attributed-event", UNSET)
        attributed_event: Union[Unset, AttributionResponseObjectResourceRelationshipsAttributedEvent]
        if isinstance(_attributed_event, Unset):
            attributed_event = UNSET
        else:
            attributed_event = AttributionResponseObjectResourceRelationshipsAttributedEvent.from_dict(
                _attributed_event
            )

        _campaign = d.pop("campaign", UNSET)
        campaign: Union[Unset, AttributionResponseObjectResourceRelationshipsCampaign]
        if isinstance(_campaign, Unset):
            campaign = UNSET
        else:
            campaign = AttributionResponseObjectResourceRelationshipsCampaign.from_dict(_campaign)

        _campaign_message = d.pop("campaign-message", UNSET)
        campaign_message: Union[Unset, AttributionResponseObjectResourceRelationshipsCampaignMessage]
        if isinstance(_campaign_message, Unset):
            campaign_message = UNSET
        else:
            campaign_message = AttributionResponseObjectResourceRelationshipsCampaignMessage.from_dict(
                _campaign_message
            )

        _flow = d.pop("flow", UNSET)
        flow: Union[Unset, AttributionResponseObjectResourceRelationshipsFlow]
        if isinstance(_flow, Unset):
            flow = UNSET
        else:
            flow = AttributionResponseObjectResourceRelationshipsFlow.from_dict(_flow)

        _flow_message = d.pop("flow-message", UNSET)
        flow_message: Union[Unset, AttributionResponseObjectResourceRelationshipsFlowMessage]
        if isinstance(_flow_message, Unset):
            flow_message = UNSET
        else:
            flow_message = AttributionResponseObjectResourceRelationshipsFlowMessage.from_dict(_flow_message)

        _flow_message_variation = d.pop("flow-message-variation", UNSET)
        flow_message_variation: Union[Unset, AttributionResponseObjectResourceRelationshipsFlowMessageVariation]
        if isinstance(_flow_message_variation, Unset):
            flow_message_variation = UNSET
        else:
            flow_message_variation = AttributionResponseObjectResourceRelationshipsFlowMessageVariation.from_dict(
                _flow_message_variation
            )

        attribution_response_object_resource_relationships = cls(
            event=event,
            attributed_event=attributed_event,
            campaign=campaign,
            campaign_message=campaign_message,
            flow=flow,
            flow_message=flow_message,
            flow_message_variation=flow_message_variation,
        )

        attribution_response_object_resource_relationships.additional_properties = d
        return attribution_response_object_resource_relationships

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
