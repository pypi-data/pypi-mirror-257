from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_location import ProfileLocation
    from ..models.profile_partial_update_query_resource_object_attributes_properties import (
        ProfilePartialUpdateQueryResourceObjectAttributesProperties,
    )


T = TypeVar("T", bound="ProfilePartialUpdateQueryResourceObjectAttributes")


@_attrs_define
class ProfilePartialUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        email (Union[Unset, str]): Individual's email address Example: sarah.mason@klaviyo-demo.com.
        phone_number (Union[Unset, str]): Individual's phone number in E.164 format Example: +15005550006.
        external_id (Union[Unset, str]): A unique identifier used by customers to associate Klaviyo profiles with
            profiles in an external system, such as a point-of-sale system. Format varies based on the external system.
            Example: 63f64a2b-c6bf-40c7-b81f-bed08162edbe.
        anonymous_id (Union[Unset, str]):
        first_name (Union[Unset, str]): Individual's first name Example: Sarah.
        last_name (Union[Unset, str]): Individual's last name Example: Mason.
        organization (Union[Unset, str]): Name of the company or organization within the company for whom the individual
            works Example: Klaviyo.
        title (Union[Unset, str]): Individual's job title Example: Engineer.
        image (Union[Unset, str]): URL pointing to the location of a profile image Example:
            https://images.pexels.com/photos/3760854/pexels-photo-3760854.jpeg.
        location (Union[Unset, ProfileLocation]):
        properties (Union[Unset, ProfilePartialUpdateQueryResourceObjectAttributesProperties]): An object containing
            key/value pairs for any custom properties assigned to this profile Example: {'pseudonym': 'Dr. Octopus'}.
    """

    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET
    anonymous_id: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    location: Union[Unset, "ProfileLocation"] = UNSET
    properties: Union[Unset, "ProfilePartialUpdateQueryResourceObjectAttributesProperties"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        phone_number = self.phone_number

        external_id = self.external_id

        anonymous_id = self.anonymous_id

        first_name = self.first_name

        last_name = self.last_name

        organization = self.organization

        title = self.title

        image = self.image

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
        if anonymous_id is not UNSET:
            field_dict["anonymous_id"] = anonymous_id
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
        if location is not UNSET:
            field_dict["location"] = location
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_location import ProfileLocation
        from ..models.profile_partial_update_query_resource_object_attributes_properties import (
            ProfilePartialUpdateQueryResourceObjectAttributesProperties,
        )

        d = src_dict.copy()
        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        external_id = d.pop("external_id", UNSET)

        anonymous_id = d.pop("anonymous_id", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        organization = d.pop("organization", UNSET)

        title = d.pop("title", UNSET)

        image = d.pop("image", UNSET)

        _location = d.pop("location", UNSET)
        location: Union[Unset, ProfileLocation]
        if isinstance(_location, Unset):
            location = UNSET
        else:
            location = ProfileLocation.from_dict(_location)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ProfilePartialUpdateQueryResourceObjectAttributesProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProfilePartialUpdateQueryResourceObjectAttributesProperties.from_dict(_properties)

        profile_partial_update_query_resource_object_attributes = cls(
            email=email,
            phone_number=phone_number,
            external_id=external_id,
            anonymous_id=anonymous_id,
            first_name=first_name,
            last_name=last_name,
            organization=organization,
            title=title,
            image=image,
            location=location,
            properties=properties,
        )

        profile_partial_update_query_resource_object_attributes.additional_properties = d
        return profile_partial_update_query_resource_object_attributes

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
