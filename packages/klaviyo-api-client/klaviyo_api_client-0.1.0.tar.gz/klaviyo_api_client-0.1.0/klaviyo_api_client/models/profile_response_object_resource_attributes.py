import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_location import ProfileLocation
    from ..models.profile_response_object_resource_attributes_properties import (
        ProfileResponseObjectResourceAttributesProperties,
    )


T = TypeVar("T", bound="ProfileResponseObjectResourceAttributes")


@_attrs_define
class ProfileResponseObjectResourceAttributes:
    """
    Attributes:
        email (Union[Unset, str]): Individual's email address Example: sarah.mason@klaviyo-demo.com.
        phone_number (Union[Unset, str]): Individual's phone number in E.164 format Example: +15005550006.
        external_id (Union[Unset, str]): A unique identifier used by customers to associate Klaviyo profiles with
            profiles in an external system, such as a point-of-sale system. Format varies based on the external system.
            Example: 63f64a2b-c6bf-40c7-b81f-bed08162edbe.
        first_name (Union[Unset, str]): Individual's first name Example: Sarah.
        last_name (Union[Unset, str]): Individual's last name Example: Mason.
        organization (Union[Unset, str]): Name of the company or organization within the company for whom the individual
            works Example: Klaviyo.
        title (Union[Unset, str]): Individual's job title Example: Engineer.
        image (Union[Unset, str]): URL pointing to the location of a profile image Example:
            https://images.pexels.com/photos/3760854/pexels-photo-3760854.jpeg.
        created (Union[Unset, datetime.datetime]): Date and time when the profile was created, in ISO 8601 format (YYYY-
            MM-DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]): Date and time when the profile was last updated, in ISO 8601 format
            (YYYY-MM-DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        last_event_date (Union[Unset, datetime.datetime]): Date and time of the most recent event the triggered an
            update to the profile, in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm) Example: 2022-11-08T00:00:00.
        location (Union[Unset, ProfileLocation]):
        properties (Union[Unset, ProfileResponseObjectResourceAttributesProperties]): An object containing key/value
            pairs for any custom properties assigned to this profile Example: {'pseudonym': 'Dr. Octopus'}.
    """

    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    last_event_date: Union[Unset, datetime.datetime] = UNSET
    location: Union[Unset, "ProfileLocation"] = UNSET
    properties: Union[Unset, "ProfileResponseObjectResourceAttributesProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        phone_number = self.phone_number

        external_id = self.external_id

        first_name = self.first_name

        last_name = self.last_name

        organization = self.organization

        title = self.title

        image = self.image

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        last_event_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_event_date, Unset):
            last_event_date = self.last_event_date.isoformat()

        location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.location, Unset):
            location = self.location.to_dict()

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if organization is not UNSET:
            field_dict["organization"] = organization
        if title is not UNSET:
            field_dict["title"] = title
        if image is not UNSET:
            field_dict["image"] = image
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if last_event_date is not UNSET:
            field_dict["last_event_date"] = last_event_date
        if location is not UNSET:
            field_dict["location"] = location
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_location import ProfileLocation
        from ..models.profile_response_object_resource_attributes_properties import (
            ProfileResponseObjectResourceAttributesProperties,
        )

        d = src_dict.copy()
        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        external_id = d.pop("external_id", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        organization = d.pop("organization", UNSET)

        title = d.pop("title", UNSET)

        image = d.pop("image", UNSET)

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

        _last_event_date = d.pop("last_event_date", UNSET)
        last_event_date: Union[Unset, datetime.datetime]
        if isinstance(_last_event_date, Unset):
            last_event_date = UNSET
        else:
            last_event_date = isoparse(_last_event_date)

        _location = d.pop("location", UNSET)
        location: Union[Unset, ProfileLocation]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = ProfileLocation.from_dict(_location)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ProfileResponseObjectResourceAttributesProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProfileResponseObjectResourceAttributesProperties.from_dict(_properties)

        profile_response_object_resource_attributes = cls(
            email=email,
            phone_number=phone_number,
            external_id=external_id,
            first_name=first_name,
            last_name=last_name,
            organization=organization,
            title=title,
            image=image,
            created=created,
            updated=updated,
            last_event_date=last_event_date,
            location=location,
            properties=properties,
        )

        profile_response_object_resource_attributes.additional_properties = d
        return profile_response_object_resource_attributes

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
