from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audiences_sub_object import AudiencesSubObject
    from ..models.campaign_create_query_resource_object_attributes_campaign_messages import (
        CampaignCreateQueryResourceObjectAttributesCampaignMessages,
    )
    from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
    from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject
    from ..models.send_strategy_sub_object import SendStrategySubObject
    from ..models.sms_send_options_sub_object import SMSSendOptionsSubObject
    from ..models.sms_tracking_options_sub_object import SMSTrackingOptionsSubObject


T = TypeVar("T", bound="CampaignCreateQueryResourceObjectAttributes")


@_attrs_define
class CampaignCreateQueryResourceObjectAttributes:
    """
    Attributes:
        name (str): The campaign name Example: My new campaign.
        audiences (AudiencesSubObject):
        campaign_messages (CampaignCreateQueryResourceObjectAttributesCampaignMessages): The message(s) associated with
            the campaign
        send_strategy (Union[Unset, SendStrategySubObject]):
        send_options (Union['EmailSendOptionsSubObject', 'SMSSendOptionsSubObject', Unset]): Options to use when sending
            a campaign
        tracking_options (Union['EmailTrackingOptionsSubObject', 'SMSTrackingOptionsSubObject', Unset]): The tracking
            options associated with the campaign
    """

    name: str
    audiences: "AudiencesSubObject"
    campaign_messages: "CampaignCreateQueryResourceObjectAttributesCampaignMessages"
    send_strategy: Union[Unset, "SendStrategySubObject"] = UNSET
    send_options: Union["EmailSendOptionsSubObject", "SMSSendOptionsSubObject", Unset] = UNSET
    tracking_options: Union["EmailTrackingOptionsSubObject", "SMSTrackingOptionsSubObject", Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
        from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject

        name = self.name

        audiences = self.audiences.to_dict()

        campaign_messages = self.campaign_messages.to_dict()

        send_strategy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.send_strategy, Unset):
            send_strategy = self.send_strategy.to_dict()

        send_options: Union[Dict[str, Any], Unset]
        if isinstance(self.send_options, Unset):
            send_options = UNSET
        elif isinstance(self.send_options, EmailSendOptionsSubObject):
            send_options = self.send_options.to_dict()
        else:
            send_options = self.send_options.to_dict()

        tracking_options: Union[Dict[str, Any], Unset]
        if isinstance(self.tracking_options, Unset):
            tracking_options = UNSET
        elif isinstance(self.tracking_options, EmailTrackingOptionsSubObject):
            tracking_options = self.tracking_options.to_dict()
        else:
            tracking_options = self.tracking_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "audiences": audiences,
                "campaign-messages": campaign_messages,
            }
        )
        if send_strategy is not UNSET:
            field_dict["send_strategy"] = send_strategy
        if send_options is not UNSET:
            field_dict["send_options"] = send_options
        if tracking_options is not UNSET:
            field_dict["tracking_options"] = tracking_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.audiences_sub_object import AudiencesSubObject
        from ..models.campaign_create_query_resource_object_attributes_campaign_messages import (
            CampaignCreateQueryResourceObjectAttributesCampaignMessages,
        )
        from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
        from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject
        from ..models.send_strategy_sub_object import SendStrategySubObject
        from ..models.sms_send_options_sub_object import SMSSendOptionsSubObject
        from ..models.sms_tracking_options_sub_object import SMSTrackingOptionsSubObject

        d = src_dict.copy()
        name = d.pop("name")

        audiences = AudiencesSubObject.from_dict(d.pop("audiences"))

        campaign_messages = CampaignCreateQueryResourceObjectAttributesCampaignMessages.from_dict(
            d.pop("campaign-messages")
        )

        _send_strategy = d.pop("send_strategy", UNSET)
        send_strategy: Union[Unset, SendStrategySubObject]
        if isinstance(_send_strategy, Unset):
            send_strategy = UNSET
        else:
            send_strategy = SendStrategySubObject.from_dict(_send_strategy)

        def _parse_send_options(data: object) -> Union["EmailSendOptionsSubObject", "SMSSendOptionsSubObject", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                send_options_type_0 = EmailSendOptionsSubObject.from_dict(data)

                return send_options_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            send_options_type_1 = SMSSendOptionsSubObject.from_dict(data)

            return send_options_type_1

        send_options = _parse_send_options(d.pop("send_options", UNSET))

        def _parse_tracking_options(
            data: object,
        ) -> Union["EmailTrackingOptionsSubObject", "SMSTrackingOptionsSubObject", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tracking_options_type_0 = EmailTrackingOptionsSubObject.from_dict(data)

                return tracking_options_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            tracking_options_type_1 = SMSTrackingOptionsSubObject.from_dict(data)

            return tracking_options_type_1

        tracking_options = _parse_tracking_options(d.pop("tracking_options", UNSET))

        campaign_create_query_resource_object_attributes = cls(
            name=name,
            audiences=audiences,
            campaign_messages=campaign_messages,
            send_strategy=send_strategy,
            send_options=send_options,
            tracking_options=tracking_options,
        )

        campaign_create_query_resource_object_attributes.additional_properties = d
        return campaign_create_query_resource_object_attributes

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
