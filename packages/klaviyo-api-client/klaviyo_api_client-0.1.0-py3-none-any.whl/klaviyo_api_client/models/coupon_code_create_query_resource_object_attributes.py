import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CouponCodeCreateQueryResourceObjectAttributes")


@_attrs_define
class CouponCodeCreateQueryResourceObjectAttributes:
    """
    Attributes:
        unique_code (str): This is a unique string that will be or is assigned to each customer/profile and is
            associated with a coupon. Example: ASD325FHK324UJDOI2M3JNES99.
        expires_at (Union[Unset, datetime.datetime]): The datetime when this coupon code will expire. If not specified
            or set to null, it will be automatically set to 1 year. Example: 2023-01-01T00:00:00Z.
    """

    unique_code: str
    expires_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unique_code = self.unique_code

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unique_code": unique_code,
            }
        )
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unique_code = d.pop("unique_code")

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        coupon_code_create_query_resource_object_attributes = cls(
            unique_code=unique_code,
            expires_at=expires_at,
        )

        coupon_code_create_query_resource_object_attributes.additional_properties = d
        return coupon_code_create_query_resource_object_attributes

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
