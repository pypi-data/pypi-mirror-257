from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StreetAddress")


@_attrs_define
class StreetAddress:
    """
    Attributes:
        address1 (str):  Example: 125 Summer Street.
        address2 (str):  Example: 5th Floor.
        city (str):  Example: Boston.
        region (str): State, province, or region. Example: MA.
        country (str): Two-letter [ISO country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
            Example: US.
        zip_ (str):  Example: 04323.
    """

    address1: str
    address2: str
    city: str
    region: str
    country: str
    zip_: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address1 = self.address1

        address2 = self.address2

        city = self.city

        region = self.region

        country = self.country

        zip_ = self.zip_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address1": address1,
                "address2": address2,
                "city": city,
                "region": region,
                "country": country,
                "zip": zip_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address1 = d.pop("address1")

        address2 = d.pop("address2")

        city = d.pop("city")

        region = d.pop("region")

        country = d.pop("country")

        zip_ = d.pop("zip")

        street_address = cls(
            address1=address1,
            address2=address2,
            city=city,
            region=region,
            country=country,
            zip_=zip_,
        )

        street_address.additional_properties = d
        return street_address

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
