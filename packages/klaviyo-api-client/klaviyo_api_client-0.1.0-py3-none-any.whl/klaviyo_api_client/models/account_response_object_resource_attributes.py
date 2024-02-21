from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.contact_information import ContactInformation


T = TypeVar("T", bound="AccountResponseObjectResourceAttributes")


@_attrs_define
class AccountResponseObjectResourceAttributes:
    """
    Attributes:
        contact_information (ContactInformation):
        industry (str): The kind of business and/or types of goods that the business sells. This is leveraged in Klaviyo
            analytics and guidance. Example: Software / SaaS.
        timezone (str): The account's timezone is used when displaying dates and times. This is an IANA timezone. See
            [the full list here ](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Example: US/Eastern.
        preferred_currency (str): The preferred currency for the account. This is the currency used for currency-based
            metrics in dashboards, analytics, coupons, and templates. Example: USD.
        public_api_key (str): The Public API Key can be used for client-side API calls. [More info
            here](https://developers.klaviyo.com/en/docs/retrieve_api_credentials). Example: AbC123.
    """

    contact_information: "ContactInformation"
    industry: str
    timezone: str
    preferred_currency: str
    public_api_key: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        contact_information = self.contact_information.to_dict()

        industry = self.industry

        timezone = self.timezone

        preferred_currency = self.preferred_currency

        public_api_key = self.public_api_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contact_information": contact_information,
                "industry": industry,
                "timezone": timezone,
                "preferred_currency": preferred_currency,
                "public_api_key": public_api_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contact_information import ContactInformation

        d = src_dict.copy()
        contact_information = ContactInformation.from_dict(d.pop("contact_information"))

        industry = d.pop("industry")

        timezone = d.pop("timezone")

        preferred_currency = d.pop("preferred_currency")

        public_api_key = d.pop("public_api_key")

        account_response_object_resource_attributes = cls(
            contact_information=contact_information,
            industry=industry,
            timezone=timezone,
            preferred_currency=preferred_currency,
            public_api_key=public_api_key,
        )

        account_response_object_resource_attributes.additional_properties = d
        return account_response_object_resource_attributes

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
