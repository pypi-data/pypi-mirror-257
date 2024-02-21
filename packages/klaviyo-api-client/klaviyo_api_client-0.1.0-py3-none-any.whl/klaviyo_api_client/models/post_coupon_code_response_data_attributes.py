import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.post_coupon_code_response_data_attributes_status import PostCouponCodeResponseDataAttributesStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostCouponCodeResponseDataAttributes")


@_attrs_define
class PostCouponCodeResponseDataAttributes:
    """
    Attributes:
        unique_code (Union[Unset, str]): This is a unique string that will be or is assigned to each customer/profile
            and is associated with a coupon. Example: ASD325FHK324UJDOI2M3JNES99.
        expires_at (Union[Unset, datetime.datetime]): The datetime when this coupon code will expire. If not specified
            or set to null, it will be automatically set to 1 year. Example: 2023-01-01T00:00:00Z.
        status (Union[Unset, PostCouponCodeResponseDataAttributesStatus]): The current status of the coupon code.
            Example: UNASSIGNED.
    """

    unique_code: Union[Unset, str] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, PostCouponCodeResponseDataAttributesStatus] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unique_code = self.unique_code

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if unique_code is not UNSET:
            field_dict["unique_code"] = unique_code
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unique_code = d.pop("unique_code", UNSET)

        _expires_at = d.pop("expires_at", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        _status = d.pop("status", UNSET)
        status: Union[Unset, PostCouponCodeResponseDataAttributesStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PostCouponCodeResponseDataAttributesStatus(_status)

        post_coupon_code_response_data_attributes = cls(
            unique_code=unique_code,
            expires_at=expires_at,
            status=status,
        )

        post_coupon_code_response_data_attributes.additional_properties = d
        return post_coupon_code_response_data_attributes

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
