from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileIdentifierDTOResourceObjectAttributes")


@_attrs_define
class ProfileIdentifierDTOResourceObjectAttributes:
    """
    Attributes:
        email (Union[Unset, str]): Individual's email address Example: sarah.mason@klaviyo-demo.com.
        phone_number (Union[Unset, str]): Individual's phone number in E.164 format Example: +15005550006.
        external_id (Union[Unset, str]): A unique identifier used by customers to associate Klaviyo profiles with
            profiles in an external system, such as a point-of-sale system. Format varies based on the external system.
            Example: 63f64a2b-c6bf-40c7-b81f-bed08162edbe.
        anonymous_id (Union[Unset, str]):
    """

    email: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET
    anonymous_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        phone_number = self.phone_number

        external_id = self.external_id

        anonymous_id = self.anonymous_id

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        external_id = d.pop("external_id", UNSET)

        anonymous_id = d.pop("anonymous_id", UNSET)

        profile_identifier_dto_resource_object_attributes = cls(
            email=email,
            phone_number=phone_number,
            external_id=external_id,
            anonymous_id=anonymous_id,
        )

        profile_identifier_dto_resource_object_attributes.additional_properties = d
        return profile_identifier_dto_resource_object_attributes

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
