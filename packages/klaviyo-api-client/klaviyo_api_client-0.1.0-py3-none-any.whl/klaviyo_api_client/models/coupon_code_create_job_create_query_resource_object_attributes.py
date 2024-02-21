from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.coupon_code_create_job_create_query_resource_object_attributes_coupon_codes import (
        CouponCodeCreateJobCreateQueryResourceObjectAttributesCouponCodes,
    )


T = TypeVar("T", bound="CouponCodeCreateJobCreateQueryResourceObjectAttributes")


@_attrs_define
class CouponCodeCreateJobCreateQueryResourceObjectAttributes:
    """
    Attributes:
        coupon_codes (CouponCodeCreateJobCreateQueryResourceObjectAttributesCouponCodes): Array of coupon codes to
            create.
    """

    coupon_codes: "CouponCodeCreateJobCreateQueryResourceObjectAttributesCouponCodes"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        coupon_codes = self.coupon_codes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "coupon-codes": coupon_codes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.coupon_code_create_job_create_query_resource_object_attributes_coupon_codes import (
            CouponCodeCreateJobCreateQueryResourceObjectAttributesCouponCodes,
        )

        d = src_dict.copy()
        coupon_codes = CouponCodeCreateJobCreateQueryResourceObjectAttributesCouponCodes.from_dict(
            d.pop("coupon-codes")
        )

        coupon_code_create_job_create_query_resource_object_attributes = cls(
            coupon_codes=coupon_codes,
        )

        coupon_code_create_job_create_query_resource_object_attributes.additional_properties = d
        return coupon_code_create_job_create_query_resource_object_attributes

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
