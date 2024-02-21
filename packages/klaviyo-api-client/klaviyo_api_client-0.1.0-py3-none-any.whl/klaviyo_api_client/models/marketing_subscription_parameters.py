import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.marketing_subscription_parameters_consent import MarketingSubscriptionParametersConsent
from ..types import UNSET, Unset

T = TypeVar("T", bound="MarketingSubscriptionParameters")


@_attrs_define
class MarketingSubscriptionParameters:
    """
    Attributes:
        consent (MarketingSubscriptionParametersConsent): The Consent status to subscribe to for the "Marketing" type.
            Currently supports "SUBSCRIBED". Example: SUBSCRIBED.
        consented_at (Union[Unset, datetime.datetime]): The timestamp of when the profile's consent was gathered
            Example: 2023-08-23T14:00:00-0400.
    """

    consent: MarketingSubscriptionParametersConsent
    consented_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        consent = self.consent.value

        consented_at: Union[Unset, str] = UNSET
        if not isinstance(self.consented_at, Unset):
            consented_at = self.consented_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "consent": consent,
            }
        )
        if consented_at is not UNSET:
            field_dict["consented_at"] = consented_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        consent = MarketingSubscriptionParametersConsent(d.pop("consent"))

        _consented_at = d.pop("consented_at", UNSET)
        consented_at: Union[Unset, datetime.datetime]
        if isinstance(_consented_at, Unset):
            consented_at = UNSET
        else:
            consented_at = isoparse(_consented_at)

        marketing_subscription_parameters = cls(
            consent=consent,
            consented_at=consented_at,
        )

        marketing_subscription_parameters.additional_properties = d
        return marketing_subscription_parameters

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
