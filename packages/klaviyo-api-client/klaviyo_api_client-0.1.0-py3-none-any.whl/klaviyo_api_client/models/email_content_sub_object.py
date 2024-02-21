from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailContentSubObject")


@_attrs_define
class EmailContentSubObject:
    """
    Attributes:
        subject (Union[Unset, str]): The subject of the message Example: Buy our product!.
        preview_text (Union[Unset, str]): Preview text associated with the message Example: My preview text.
        from_email (Union[Unset, str]): The email the message should be sent from Example: store@my-company.com.
        from_label (Union[Unset, str]): The label associated with the from_email Example: My Company.
        reply_to_email (Union[Unset, str]): Optional Reply-To email address Example: reply-to@my-company.com.
        cc_email (Union[Unset, str]): Optional CC email address Example: cc@my-company.com.
        bcc_email (Union[Unset, str]): Optional BCC email address Example: bcc@my-company.com.
    """

    subject: Union[Unset, str] = UNSET
    preview_text: Union[Unset, str] = UNSET
    from_email: Union[Unset, str] = UNSET
    from_label: Union[Unset, str] = UNSET
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
        field_dict.update({})
        if subject is not UNSET:
            field_dict["subject"] = subject
        if preview_text is not UNSET:
            field_dict["preview_text"] = preview_text
        if from_email is not UNSET:
            field_dict["from_email"] = from_email
        if from_label is not UNSET:
            field_dict["from_label"] = from_label
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
        subject = d.pop("subject", UNSET)

        preview_text = d.pop("preview_text", UNSET)

        from_email = d.pop("from_email", UNSET)

        from_label = d.pop("from_label", UNSET)

        reply_to_email = d.pop("reply_to_email", UNSET)

        cc_email = d.pop("cc_email", UNSET)

        bcc_email = d.pop("bcc_email", UNSET)

        email_content_sub_object = cls(
            subject=subject,
            preview_text=preview_text,
            from_email=from_email,
            from_label=from_label,
            reply_to_email=reply_to_email,
            cc_email=cc_email,
            bcc_email=bcc_email,
        )

        email_content_sub_object.additional_properties = d
        return email_content_sub_object

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
