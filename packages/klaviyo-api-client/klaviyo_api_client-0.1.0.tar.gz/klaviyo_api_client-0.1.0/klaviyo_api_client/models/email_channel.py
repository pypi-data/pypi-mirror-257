from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_marketing import EmailMarketing


T = TypeVar("T", bound="EmailChannel")


@_attrs_define
class EmailChannel:
    """
    Attributes:
        marketing (Union[Unset, EmailMarketing]):
    """

    marketing: Union[Unset, "EmailMarketing"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        marketing: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.marketing, Unset):
            marketing = self.marketing.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if marketing is not UNSET:
            field_dict["marketing"] = marketing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_marketing import EmailMarketing

        d = src_dict.copy()
        _marketing = d.pop("marketing", UNSET)
        marketing: Union[Unset, EmailMarketing]
        if isinstance(_marketing, Unset):
            marketing = UNSET
        else:
            marketing = EmailMarketing.from_dict(_marketing)

        email_channel = cls(
            marketing=marketing,
        )

        email_channel.additional_properties = d
        return email_channel

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
