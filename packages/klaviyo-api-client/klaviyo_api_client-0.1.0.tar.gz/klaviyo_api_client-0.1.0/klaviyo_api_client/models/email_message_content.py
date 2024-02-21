from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailMessageContent")


@_attrs_define
class EmailMessageContent:
    """
    Attributes:
        subject (str):
        preview_text (str):
        from_email (str):
        from_label (str):
        reply_to_email (Union[Unset, str]):
        cc_email (Union[Unset, str]):
        bcc_email (Union[Unset, str]):
    """

    subject: str
    preview_text: str
    from_email: str
    from_label: str
    reply_to_email: Union[Unset, str] = UNSET
    cc_email: Union[Unset, str] = UNSET
    bcc_email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subject = self.subject

        preview_text = self.preview_text

        from_email = self.from_email

        from_label = self.from_label

        reply_to_email = self.reply_to_email

        cc_email = self.cc_email

        bcc_email = self.bcc_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subject": subject,
                "preview_text": preview_text,
                "from_email": from_email,
                "from_label": from_label,
            }
        )
        if reply_to_email is not UNSET:
            field_dict["reply_to_email"] = reply_to_email
        if cc_email is not UNSET:
            field_dict["cc_email"] = cc_email
        if bcc_email is not UNSET:
            field_dict["bcc_email"] = bcc_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subject = d.pop("subject")

        preview_text = d.pop("preview_text")

        from_email = d.pop("from_email")

        from_label = d.pop("from_label")

        reply_to_email = d.pop("reply_to_email", UNSET)

        cc_email = d.pop("cc_email", UNSET)

        bcc_email = d.pop("bcc_email", UNSET)

        email_message_content = cls(
            subject=subject,
            preview_text=preview_text,
            from_email=from_email,
            from_label=from_label,
            reply_to_email=reply_to_email,
            cc_email=cc_email,
            bcc_email=bcc_email,
        )

        email_message_content.additional_properties = d
        return email_message_content

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
