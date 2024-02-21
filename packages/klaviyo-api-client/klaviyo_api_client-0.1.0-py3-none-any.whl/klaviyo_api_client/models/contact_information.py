from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.street_address import StreetAddress


T = TypeVar("T", bound="ContactInformation")


@_attrs_define
class ContactInformation:
    """
    Attributes:
        default_sender_name (str): This field is used to auto-populate the default sender name on flow and campaign
            emails. Example: Klaviyo Demo.
        default_sender_email (str): This field is used to auto-populate the default sender email address on flow and
            campaign emails. Example: contact@klaviyo-demo.com.
        website_url (str):  Example: https://www.klaviyo.com.
        organization_name (str):  Example: Klaviyo Demo.
        street_address (StreetAddress):
    """

    default_sender_name: str
    default_sender_email: str
    website_url: str
    organization_name: str
    street_address: "StreetAddress"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default_sender_name = self.default_sender_name

        default_sender_email = self.default_sender_email

        website_url = self.website_url

        organization_name = self.organization_name

        street_address = self.street_address.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default_sender_name": default_sender_name,
                "default_sender_email": default_sender_email,
                "website_url": website_url,
                "organization_name": organization_name,
                "street_address": street_address,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.street_address import StreetAddress

        d = src_dict.copy()
        default_sender_name = d.pop("default_sender_name")

        default_sender_email = d.pop("default_sender_email")

        website_url = d.pop("website_url")

        organization_name = d.pop("organization_name")

        street_address = StreetAddress.from_dict(d.pop("street_address"))

        contact_information = cls(
            default_sender_name=default_sender_name,
            default_sender_email=default_sender_email,
            website_url=website_url,
            organization_name=organization_name,
            street_address=street_address,
        )

        contact_information.additional_properties = d
        return contact_information

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
