from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.post_coupon_code_create_job_response_data_relationships_coupon_codes import (
        PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes,
    )


T = TypeVar("T", bound="PostCouponCodeCreateJobResponseDataRelationships")


@_attrs_define
class PostCouponCodeCreateJobResponseDataRelationships:
    """
    Attributes:
        coupon_codes (Union[Unset, PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes]):
    """

    coupon_codes: Union[Unset, "PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coupon_codes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coupon_codes, Unset):
            coupon_codes = self.coupon_codes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if coupon_codes is not UNSET:
            field_dict["coupon-codes"] = coupon_codes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.post_coupon_code_create_job_response_data_relationships_coupon_codes import (
            PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes,
        )

        d = src_dict.copy()
        _coupon_codes = d.pop("coupon-codes", UNSET)
        coupon_codes: Union[Unset, PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes]
        if isinstance(_coupon_codes, Unset):
            coupon_codes = UNSET
        else:
            coupon_codes = PostCouponCodeCreateJobResponseDataRelationshipsCouponCodes.from_dict(_coupon_codes)

        post_coupon_code_create_job_response_data_relationships = cls(
            coupon_codes=coupon_codes,
        )

        post_coupon_code_create_job_response_data_relationships.additional_properties = d
        return post_coupon_code_create_job_response_data_relationships

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
