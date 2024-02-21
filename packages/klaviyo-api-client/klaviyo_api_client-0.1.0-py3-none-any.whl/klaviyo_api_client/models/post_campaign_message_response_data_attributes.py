import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_content_sub_object import EmailContentSubObject
    from ..models.render_options_sub_object import RenderOptionsSubObject
    from ..models.send_time_sub_object import SendTimeSubObject
    from ..models.sms_content_sub_object import SMSContentSubObject


T = TypeVar("T", bound="PostCampaignMessageResponseDataAttributes")


@_attrs_define
class PostCampaignMessageResponseDataAttributes:
    """
    Attributes:
        label (str): The label or name on the message
        channel (str): The channel the message is to be sent on
        content (Union['EmailContentSubObject', 'SMSContentSubObject']): Additional attributes relating to the content
            of the message
        send_times (Union[Unset, List['SendTimeSubObject']]): The list of appropriate Send Time Sub-objects associated
            with the message
        render_options (Union[Unset, RenderOptionsSubObject]):
        created_at (Union[Unset, datetime.datetime]): The datetime when the message was created Example:
            2022-11-08T00:00:00.
        updated_at (Union[Unset, datetime.datetime]): The datetime when the message was last updated Example:
            2022-11-08T00:00:00.
    """

    label: str
    channel: str
    content: Union["EmailContentSubObject", "SMSContentSubObject"]
    send_times: Union[Unset, List["SendTimeSubObject"]] = UNSET
    render_options: Union[Unset, "RenderOptionsSubObject"] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_content_sub_object import EmailContentSubObject

        label = self.label

        channel = self.channel

        content: Dict[str, Any]
        if isinstance(self.content, EmailContentSubObject):
            content = self.content.to_dict()
        else:
            content = self.content.to_dict()

        send_times: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.send_times, Unset):
            send_times = []
            for send_times_item_data in self.send_times:
                send_times_item = send_times_item_data.to_dict()
                send_times.append(send_times_item)

        render_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.render_options, Unset):
            render_options = self.render_options.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "channel": channel,
                "content": content,
            }
        )
        if send_times is not UNSET:
            field_dict["send_times"] = send_times
        if render_options is not UNSET:
            field_dict["render_options"] = render_options
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_content_sub_object import EmailContentSubObject
        from ..models.render_options_sub_object import RenderOptionsSubObject
        from ..models.send_time_sub_object import SendTimeSubObject
        from ..models.sms_content_sub_object import SMSContentSubObject

        d = src_dict.copy()
        label = d.pop("label")

        channel = d.pop("channel")

        def _parse_content(data: object) -> Union["EmailContentSubObject", "SMSContentSubObject"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_0 = EmailContentSubObject.from_dict(data)

                return content_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            content_type_1 = SMSContentSubObject.from_dict(data)

            return content_type_1

        content = _parse_content(d.pop("content"))

        send_times = []
        _send_times = d.pop("send_times", UNSET)
        for send_times_item_data in _send_times or []:
            send_times_item = SendTimeSubObject.from_dict(send_times_item_data)

            send_times.append(send_times_item)

        _render_options = d.pop("render_options", UNSET)
        render_options: Union[Unset, RenderOptionsSubObject]
        if isinstance(_render_options, Unset):
            render_options = UNSET
        else:
            render_options = RenderOptionsSubObject.from_dict(_render_options)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        post_campaign_message_response_data_attributes = cls(
            label=label,
            channel=channel,
            content=content,
            send_times=send_times,
            render_options=render_options,
            created_at=created_at,
            updated_at=updated_at,
        )

        post_campaign_message_response_data_attributes.additional_properties = d
        return post_campaign_message_response_data_attributes

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
