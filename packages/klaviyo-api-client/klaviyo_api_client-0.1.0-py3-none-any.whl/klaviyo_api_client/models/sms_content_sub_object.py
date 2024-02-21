from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SMSContentSubObject")


@_attrs_define
class SMSContentSubObject:
    """
    Attributes:
        body (Union[Unset, str]): The message body Example: My preview sms.
        media_url (Union[Unset, str]): URL for included media
    """

    body: Union[Unset, str] = UNSET
    media_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        body = self.body

        media_url = self.media_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if media_url is not UNSET:
            field_dict["media_url"] = media_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("body", UNSET)

        media_url = d.pop("media_url", UNSET)

        sms_content_sub_object = cls(
            body=body,
            media_url=media_url,
        )

        sms_content_sub_object.additional_properties = d
        return sms_content_sub_object

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
