import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.audiences_sub_object import AudiencesSubObject
    from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
    from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject
    from ..models.send_strategy_sub_object import SendStrategySubObject
    from ..models.sms_send_options_sub_object import SMSSendOptionsSubObject
    from ..models.sms_tracking_options_sub_object import SMSTrackingOptionsSubObject


T = TypeVar("T", bound="PatchCampaignResponseDataAttributes")


@_attrs_define
class PatchCampaignResponseDataAttributes:
    """
    Attributes:
        name (str): The campaign name
        status (str): The current status of the campaign
        archived (bool): Whether the campaign has been archived or not
        audiences (AudiencesSubObject):
        send_options (Union['EmailSendOptionsSubObject', 'SMSSendOptionsSubObject']): Options to use when sending a
            campaign
        tracking_options (Union['EmailTrackingOptionsSubObject', 'SMSTrackingOptionsSubObject']): The tracking options
            associated with the campaign
        send_strategy (SendStrategySubObject):
        created_at (datetime.datetime): The datetime when the campaign was created Example: 2022-11-08T00:00:00.
        scheduled_at (datetime.datetime): The datetime when the campaign was scheduled for future sending Example:
            2022-11-08T00:00:00.
        updated_at (datetime.datetime): The datetime when the campaign was last updated by a user or the system Example:
            2022-11-08T00:00:00.
        send_time (datetime.datetime): The datetime when the campaign will be / was sent or None if not yet scheduled by
            a send_job. Example: 2022-11-08T00:00:00.
    """

    name: str
    status: str
    archived: bool
    audiences: "AudiencesSubObject"
    send_options: Union["EmailSendOptionsSubObject", "SMSSendOptionsSubObject"]
    tracking_options: Union["EmailTrackingOptionsSubObject", "SMSTrackingOptionsSubObject"]
    send_strategy: "SendStrategySubObject"
    created_at: datetime.datetime
    scheduled_at: datetime.datetime
    updated_at: datetime.datetime
    send_time: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
        from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject

        name = self.name

        status = self.status

        archived = self.archived

        audiences = self.audiences.to_dict()

        send_options: Dict[str, Any]
        if isinstance(self.send_options, EmailSendOptionsSubObject):
            send_options = self.send_options.to_dict()
        else:
            send_options = self.send_options.to_dict()

        tracking_options: Dict[str, Any]
        if isinstance(self.tracking_options, EmailTrackingOptionsSubObject):
            tracking_options = self.tracking_options.to_dict()
        else:
            tracking_options = self.tracking_options.to_dict()

        send_strategy = self.send_strategy.to_dict()

        created_at = self.created_at.isoformat()

        scheduled_at = self.scheduled_at.isoformat()

        updated_at = self.updated_at.isoformat()

        send_time = self.send_time.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
                "archived": archived,
                "audiences": audiences,
                "send_options": send_options,
                "tracking_options": tracking_options,
                "send_strategy": send_strategy,
                "created_at": created_at,
                "scheduled_at": scheduled_at,
                "updated_at": updated_at,
                "send_time": send_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.audiences_sub_object import AudiencesSubObject
        from ..models.email_send_options_sub_object import EmailSendOptionsSubObject
        from ..models.email_tracking_options_sub_object import EmailTrackingOptionsSubObject
        from ..models.send_strategy_sub_object import SendStrategySubObject
        from ..models.sms_send_options_sub_object import SMSSendOptionsSubObject
        from ..models.sms_tracking_options_sub_object import SMSTrackingOptionsSubObject

        d = src_dict.copy()
        name = d.pop("name")

        status = d.pop("status")

        archived = d.pop("archived")

        audiences = AudiencesSubObject.from_dict(d.pop("audiences"))

        def _parse_send_options(data: object) -> Union["EmailSendOptionsSubObject", "SMSSendOptionsSubObject"]:
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

        send_options = _parse_send_options(d.pop("send_options"))

        def _parse_tracking_options(
            data: object,
        ) -> Union["EmailTrackingOptionsSubObject", "SMSTrackingOptionsSubObject"]:
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

        tracking_options = _parse_tracking_options(d.pop("tracking_options"))

        send_strategy = SendStrategySubObject.from_dict(d.pop("send_strategy"))

        created_at = isoparse(d.pop("created_at"))

        scheduled_at = isoparse(d.pop("scheduled_at"))

        updated_at = isoparse(d.pop("updated_at"))

        send_time = isoparse(d.pop("send_time"))

        patch_campaign_response_data_attributes = cls(
            name=name,
            status=status,
            archived=archived,
            audiences=audiences,
            send_options=send_options,
            tracking_options=tracking_options,
            send_strategy=send_strategy,
            created_at=created_at,
            scheduled_at=scheduled_at,
            updated_at=updated_at,
            send_time=send_time,
        )

        patch_campaign_response_data_attributes.additional_properties = d
        return patch_campaign_response_data_attributes

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
