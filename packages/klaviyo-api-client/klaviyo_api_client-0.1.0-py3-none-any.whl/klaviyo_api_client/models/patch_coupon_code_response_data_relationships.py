from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patch_coupon_code_response_data_relationships_coupon import (
        PatchCouponCodeResponseDataRelationshipsCoupon,
    )
    from ..models.patch_coupon_code_response_data_relationships_profile import (
        PatchCouponCodeResponseDataRelationshipsProfile,
    )


T = TypeVar("T", bound="PatchCouponCodeResponseDataRelationships")


@_attrs_define
class PatchCouponCodeResponseDataRelationships:
    """
    Attributes:
        coupon (Union[Unset, PatchCouponCodeResponseDataRelationshipsCoupon]):
        profile (Union[Unset, PatchCouponCodeResponseDataRelationshipsProfile]):
    """

    coupon: Union[Unset, "PatchCouponCodeResponseDataRelationshipsCoupon"] = UNSET
    profile: Union[Unset, "PatchCouponCodeResponseDataRelationshipsProfile"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coupon: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coupon, Unset):
            coupon = self.coupon.to_dict()

        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if coupon is not UNSET:
            field_dict["coupon"] = coupon
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.patch_coupon_code_response_data_relationships_coupon import (
            PatchCouponCodeResponseDataRelationshipsCoupon,
        )
        from ..models.patch_coupon_code_response_data_relationships_profile import (
            PatchCouponCodeResponseDataRelationshipsProfile,
        )

        d = src_dict.copy()
        _coupon = d.pop("coupon", UNSET)
        coupon: Union[Unset, PatchCouponCodeResponseDataRelationshipsCoupon]
        if isinstance(_coupon, Unset):
            coupon = UNSET
        else:
            coupon = PatchCouponCodeResponseDataRelationshipsCoupon.from_dict(_coupon)

        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, PatchCouponCodeResponseDataRelationshipsProfile]
        if isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = PatchCouponCodeResponseDataRelationshipsProfile.from_dict(_profile)

        patch_coupon_code_response_data_relationships = cls(
            coupon=coupon,
            profile=profile,
        )

        patch_coupon_code_response_data_relationships.additional_properties = d
        return patch_coupon_code_response_data_relationships

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
