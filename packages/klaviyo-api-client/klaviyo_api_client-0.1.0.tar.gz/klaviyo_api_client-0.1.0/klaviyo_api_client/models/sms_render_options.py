from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SMSRenderOptions")


@_attrs_define
class SMSRenderOptions:
    """
    Attributes:
        shorten_links (bool):
        add_org_prefix (bool):
        add_info_link (bool):
        add_opt_out_language (bool):
    """

    shorten_links: bool
    add_org_prefix: bool
    add_info_link: bool
    add_opt_out_language: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        shorten_links = self.shorten_links

        add_org_prefix = self.add_org_prefix

        add_info_link = self.add_info_link

        add_opt_out_language = self.add_opt_out_language

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "shorten_links": shorten_links,
                "add_org_prefix": add_org_prefix,
                "add_info_link": add_info_link,
                "add_opt_out_language": add_opt_out_language,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        shorten_links = d.pop("shorten_links")

        add_org_prefix = d.pop("add_org_prefix")

        add_info_link = d.pop("add_info_link")

        add_opt_out_language = d.pop("add_opt_out_language")

        sms_render_options = cls(
            shorten_links=shorten_links,
            add_org_prefix=add_org_prefix,
            add_info_link=add_info_link,
            add_opt_out_language=add_opt_out_language,
        )

        sms_render_options.additional_properties = d
        return sms_render_options

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
