import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_message_content import EmailMessageContent
    from ..models.sms_message_content import SMSMessageContent


T = TypeVar("T", bound="FlowMessageResponseObjectResourceAttributes")


@_attrs_define
class FlowMessageResponseObjectResourceAttributes:
    """
    Attributes:
        name (str):
        channel (str):
        content (Union['EmailMessageContent', 'SMSMessageContent']):
        created (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
    """

    name: str
    channel: str
    content: Union["EmailMessageContent", "SMSMessageContent"]
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_message_content import EmailMessageContent

        name = self.name

        channel = self.channel

        content: Dict[str, Any]
        if isinstance(self.content, EmailMessageContent):
            content = self.content.to_dict()
        else:
            content = self.content.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "channel": channel,
                "content": content,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_message_content import EmailMessageContent
        from ..models.sms_message_content import SMSMessageContent

        d = src_dict.copy()
        name = d.pop("name")

        channel = d.pop("channel")

        def _parse_content(data: object) -> Union["EmailMessageContent", "SMSMessageContent"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_0 = EmailMessageContent.from_dict(data)

                return content_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            content_type_1 = SMSMessageContent.from_dict(data)

            return content_type_1

        content = _parse_content(d.pop("content"))

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        flow_message_response_object_resource_attributes = cls(
            name=name,
            channel=channel,
            content=content,
            created=created,
            updated=updated,
        )

        flow_message_response_object_resource_attributes.additional_properties = d
        return flow_message_response_object_resource_attributes

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
