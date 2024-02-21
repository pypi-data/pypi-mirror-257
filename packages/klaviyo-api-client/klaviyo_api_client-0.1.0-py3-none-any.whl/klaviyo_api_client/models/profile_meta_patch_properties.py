from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profile_meta_patch_properties_append import ProfileMetaPatchPropertiesAppend
    from ..models.profile_meta_patch_properties_unappend import ProfileMetaPatchPropertiesUnappend


T = TypeVar("T", bound="ProfileMetaPatchProperties")


@_attrs_define
class ProfileMetaPatchProperties:
    """
    Attributes:
        append (Union[Unset, ProfileMetaPatchPropertiesAppend]): Append a simple value or values to this property array
            Example: {'skus': '92538'}.
        unappend (Union[Unset, ProfileMetaPatchPropertiesUnappend]): Remove a simple value or values from this property
            array Example: {'skus': '40571'}.
        unset (Union[List[str], Unset, str]): Remove a key or keys (and their values) completely from properties
            Example: skus.
    """

    append: Union[Unset, "ProfileMetaPatchPropertiesAppend"] = UNSET
    unappend: Union[Unset, "ProfileMetaPatchPropertiesUnappend"] = UNSET
    unset: Union[List[str], Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        append: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.append, Unset):
            append = self.append.to_dict()

        unappend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.unappend, Unset):
            unappend = self.unappend.to_dict()

        unset: Union[List[str], Unset, str]
        if isinstance(self.unset, Unset):
            unset = UNSET
        elif isinstance(self.unset, list):
            unset = self.unset

        else:
            unset = self.unset

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if append is not UNSET:
            field_dict["append"] = append
        if unappend is not UNSET:
            field_dict["unappend"] = unappend
        if unset is not UNSET:
            field_dict["unset"] = unset

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.profile_meta_patch_properties_append import ProfileMetaPatchPropertiesAppend
        from ..models.profile_meta_patch_properties_unappend import ProfileMetaPatchPropertiesUnappend

        d = src_dict.copy()
        _append = d.pop("append", UNSET)
        append: Union[Unset, ProfileMetaPatchPropertiesAppend]
        if isinstance(_append, Unset):
            append = UNSET
        else:
            append = ProfileMetaPatchPropertiesAppend.from_dict(_append)

        _unappend = d.pop("unappend", UNSET)
        unappend: Union[Unset, ProfileMetaPatchPropertiesUnappend]
        if isinstance(_unappend, Unset):
            unappend = UNSET
        else:
            unappend = ProfileMetaPatchPropertiesUnappend.from_dict(_unappend)

        def _parse_unset(data: object) -> Union[List[str], Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                unset_type_1 = cast(List[str], data)

                return unset_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[str], Unset, str], data)

        unset = _parse_unset(d.pop("unset", UNSET))

        profile_meta_patch_properties = cls(
            append=append,
            unappend=unappend,
            unset=unset,
        )

        profile_meta_patch_properties.additional_properties = d
        return profile_meta_patch_properties

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
