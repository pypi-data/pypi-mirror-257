from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RenderOptionsSubObject")


@_attrs_define
class RenderOptionsSubObject:
    """
    Attributes:
        shorten_links (Union[Unset, bool]):  Default: True. Example: True.
        add_org_prefix (Union[Unset, bool]):  Default: True. Example: True.
        add_info_link (Union[Unset, bool]):  Default: True. Example: True.
        add_opt_out_language (Union[Unset, bool]):  Default: False.
    """

    shorten_links: Union[Unset, bool] = True
    add_org_prefix: Union[Unset, bool] = True
    add_info_link: Union[Unset, bool] = True
    add_opt_out_language: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        shorten_links = self.shorten_links

        add_org_prefix = self.add_org_prefix

        add_info_link = self.add_info_link

        add_opt_out_language = self.add_opt_out_language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if shorten_links is not UNSET:
            field_dict["shorten_links"] = shorten_links
        if add_org_prefix is not UNSET:
            field_dict["add_org_prefix"] = add_org_prefix
        if add_info_link is not UNSET:
            field_dict["add_info_link"] = add_info_link
        if add_opt_out_language is not UNSET:
            field_dict["add_opt_out_language"] = add_opt_out_language

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        shorten_links = d.pop("shorten_links", UNSET)

        add_org_prefix = d.pop("add_org_prefix", UNSET)

        add_info_link = d.pop("add_info_link", UNSET)

        add_opt_out_language = d.pop("add_opt_out_language", UNSET)

        render_options_sub_object = cls(
            shorten_links=shorten_links,
            add_org_prefix=add_org_prefix,
            add_info_link=add_info_link,
            add_opt_out_language=add_opt_out_language,
        )

        render_options_sub_object.additional_properties = d
        return render_options_sub_object

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
