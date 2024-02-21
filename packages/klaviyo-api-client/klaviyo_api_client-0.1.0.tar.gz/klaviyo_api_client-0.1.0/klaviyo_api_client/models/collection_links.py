from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionLinks")


@_attrs_define
class CollectionLinks:
    """
    Attributes:
        self_ (str):
        first (Union[Unset, str]):
        last (Union[Unset, str]):
        prev (Union[Unset, str]):
        next_ (Union[Unset, str]):
    """

    self_: str
    first: Union[Unset, str] = UNSET
    last: Union[Unset, str] = UNSET
    prev: Union[Unset, str] = UNSET
    next_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_

        first = self.first

        last = self.last

        prev = self.prev

        next_ = self.next_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "self": self_,
            }
        )
        if first is not UNSET:
            field_dict["first"] = first
        if last is not UNSET:
            field_dict["last"] = last
        if prev is not UNSET:
            field_dict["prev"] = prev
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self")

        first = d.pop("first", UNSET)

        last = d.pop("last", UNSET)

        prev = d.pop("prev", UNSET)

        next_ = d.pop("next", UNSET)

        collection_links = cls(
            self_=self_,
            first=first,
            last=last,
            prev=prev,
            next_=next_,
        )

        collection_links.additional_properties = d
        return collection_links

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
