import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SMSMarketing")


@_attrs_define
class SMSMarketing:
    """
    Attributes:
        can_receive_sms_marketing (bool): Whether or not this profile is subscribed to receive SMS marketing.
        consent (str): The consent status for SMS marketing. Example: SUBSCRIBED.
        consent_timestamp (datetime.datetime): The timestamp when consent was recorded or updated for SMS marketing, in
            ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2023-02-21T20:07:38+00:00.
        method (str): The method by which the profile was subscribed to SMS marketing. Example: TEXT.
        last_updated (datetime.datetime): The timestamp when the SMS consent record was last modified, in ISO 8601
            format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2023-02-21T20:07:38+00:00.
        method_detail (Union[Unset, str]): Additional details about the method which the profile was subscribed to SMS
            marketing. This may be empty if no details were provided. Default: ''. Example: JOIN.
    """

    can_receive_sms_marketing: bool
    consent: str
    consent_timestamp: datetime.datetime
    method: str
    last_updated: datetime.datetime
    method_detail: Union[Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        can_receive_sms_marketing = self.can_receive_sms_marketing

        consent = self.consent

        consent_timestamp = self.consent_timestamp.isoformat()

        method = self.method

        last_updated = self.last_updated.isoformat()

        method_detail = self.method_detail

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "can_receive_sms_marketing": can_receive_sms_marketing,
                "consent": consent,
                "consent_timestamp": consent_timestamp,
                "method": method,
                "last_updated": last_updated,
            }
        )
        if method_detail is not UNSET:
            field_dict["method_detail"] = method_detail

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        can_receive_sms_marketing = d.pop("can_receive_sms_marketing")

        consent = d.pop("consent")

        consent_timestamp = isoparse(d.pop("consent_timestamp"))

        method = d.pop("method")

        last_updated = isoparse(d.pop("last_updated"))

        method_detail = d.pop("method_detail", UNSET)

        sms_marketing = cls(
            can_receive_sms_marketing=can_receive_sms_marketing,
            consent=consent,
            consent_timestamp=consent_timestamp,
            method=method,
            last_updated=last_updated,
            method_detail=method_detail,
        )

        sms_marketing.additional_properties = d
        return sms_marketing

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
