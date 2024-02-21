from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.marketing_subscription_parameters import MarketingSubscriptionParameters


T = TypeVar("T", bound="EmailSubscriptionParameters")


@_attrs_define
class EmailSubscriptionParameters:
    """
    Attributes:
        marketing (MarketingSubscriptionParameters):
    """

    marketing: "MarketingSubscriptionParameters"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        marketing = self.marketing.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "marketing": marketing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.marketing_subscription_parameters import MarketingSubscriptionParameters

        d = src_dict.copy()
        marketing = MarketingSubscriptionParameters.from_dict(d.pop("marketing"))

        email_subscription_parameters = cls(
            marketing=marketing,
        )

        email_subscription_parameters.additional_properties = d
        return email_subscription_parameters

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
