from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileLocation")


@_attrs_define
class ProfileLocation:
    """
    Attributes:
        address1 (Union[Unset, str]): First line of street address Example: 89 E 42nd St.
        address2 (Union[Unset, str]): Second line of street address Example: 1st floor.
        city (Union[Unset, str]): City name Example: New York.
        country (Union[Unset, str]): Country name Example: United States.
        latitude (Union[Unset, float, str]): Latitude coordinate. We recommend providing a precision of four decimal
            places. Example: 40.7128.
        longitude (Union[Unset, float, str]): Longitude coordinate. We recommend providing a precision of four decimal
            places. Example: 74.0060.
        region (Union[Unset, str]): Region within a country, such as state or province Example: NY.
        zip_ (Union[Unset, str]): Zip code Example: 10017.
        timezone (Union[Unset, str]): Time zone name. We recommend using time zones from the IANA Time Zone Database.
            Example: America/New_York.
        ip (Union[Unset, str]): IP Address Example: 127.0.0.1.
    """

    address1: Union[Unset, str] = UNSET
    address2: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    latitude: Union[Unset, float, str] = UNSET
    longitude: Union[Unset, float, str] = UNSET
    region: Union[Unset, str] = UNSET
    zip_: Union[Unset, str] = UNSET
    timezone: Union[Unset, str] = UNSET
    ip: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address1 = self.address1

        address2 = self.address2

        city = self.city

        country = self.country

        latitude: Union[Unset, float, str]
        if isinstance(self.latitude, Unset):
            latitude = UNSET
        else:
            latitude = self.latitude

        longitude: Union[Unset, float, str]
        if isinstance(self.longitude, Unset):
            longitude = UNSET
        else:
            longitude = self.longitude

        region = self.region

        zip_ = self.zip_

        timezone = self.timezone

        ip = self.ip

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address1 is not UNSET:
            field_dict["address1"] = address1
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if city is not UNSET:
            field_dict["city"] = city
        if country is not UNSET:
            field_dict["country"] = country
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if region is not UNSET:
            field_dict["region"] = region
        if zip_ is not UNSET:
            field_dict["zip"] = zip_
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if ip is not UNSET:
            field_dict["ip"] = ip

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address1 = d.pop("address1", UNSET)

        address2 = d.pop("address2", UNSET)

        city = d.pop("city", UNSET)

        country = d.pop("country", UNSET)

        def _parse_latitude(data: object) -> Union[Unset, float, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, str], data)

        latitude = _parse_latitude(d.pop("latitude", UNSET))

        def _parse_longitude(data: object) -> Union[Unset, float, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, str], data)

        longitude = _parse_longitude(d.pop("longitude", UNSET))

        region = d.pop("region", UNSET)

        zip_ = d.pop("zip", UNSET)

        timezone = d.pop("timezone", UNSET)

        ip = d.pop("ip", UNSET)

        profile_location = cls(
            address1=address1,
            address2=address2,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            region=region,
            zip_=zip_,
            timezone=timezone,
            ip=ip,
        )

        profile_location.additional_properties = d
        return profile_location

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
