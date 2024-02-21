from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.coupon_code_create_query_resource_object_relationships_coupon import (
        CouponCodeCreateQueryResourceObjectRelationshipsCoupon,
    )


T = TypeVar("T", bound="CouponCodeCreateQueryResourceObjectRelationships")


@_attrs_define
class CouponCodeCreateQueryResourceObjectRelationships:
    """
    Attributes:
        coupon (CouponCodeCreateQueryResourceObjectRelationshipsCoupon):
    """

    coupon: "CouponCodeCreateQueryResourceObjectRelationshipsCoupon"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coupon = self.coupon.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coupon": coupon,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coupon_code_create_query_resource_object_relationships_coupon import (
            CouponCodeCreateQueryResourceObjectRelationshipsCoupon,
        )

        d = src_dict.copy()
        coupon = CouponCodeCreateQueryResourceObjectRelationshipsCoupon.from_dict(d.pop("coupon"))

        coupon_code_create_query_resource_object_relationships = cls(
            coupon=coupon,
        )

        coupon_code_create_query_resource_object_relationships.additional_properties = d
        return coupon_code_create_query_resource_object_relationships

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
