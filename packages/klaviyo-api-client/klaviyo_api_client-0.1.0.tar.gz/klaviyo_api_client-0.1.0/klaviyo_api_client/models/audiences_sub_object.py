from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AudiencesSubObject")


@_attrs_define
class AudiencesSubObject:
    """
    Attributes:
        included (Union[Unset, List[str]]): A list of included audiences Example: ['Y6nRLr'].
        excluded (Union[Unset, List[str]]): An optional list of excluded audiences Example: ['UTd5ui'].
    """

    included: Union[Unset, List[str]] = UNSET
    excluded: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        included: Union[Unset, List[str]] = UNSET
        if not isinstance(self.included, Unset):
            included = self.included

        excluded: Union[Unset, List[str]] = UNSET
        if not isinstance(self.excluded, Unset):
            excluded = self.excluded

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if included is not UNSET:
            field_dict["included"] = included
        if excluded is not UNSET:
            field_dict["excluded"] = excluded

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        included = cast(List[str], d.pop("included", UNSET))

        excluded = cast(List[str], d.pop("excluded", UNSET))

        audiences_sub_object = cls(
            included=included,
            excluded=excluded,
        )

        audiences_sub_object.additional_properties = d
        return audiences_sub_object

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
