from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_content_sub_object import EmailContentSubObject
    from ..models.render_options_sub_object import RenderOptionsSubObject
    from ..models.sms_content_sub_object_create import SMSContentSubObjectCreate


T = TypeVar("T", bound="CampaignMessagePartialUpdateQueryResourceObjectAttributes")


@_attrs_define
class CampaignMessagePartialUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        label (Union[Unset, str]): The label or name on the message Example: My message name.
        content (Union['EmailContentSubObject', 'SMSContentSubObjectCreate', Unset]): Additional attributes relating to
            the content of the message
        render_options (Union[Unset, RenderOptionsSubObject]):
    """

    label: Union[Unset, str] = UNSET
    content: Union["EmailContentSubObject", "SMSContentSubObjectCreate", Unset] = UNSET
    render_options: Union[Unset, "RenderOptionsSubObject"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_content_sub_object import EmailContentSubObject

        label = self.label

        content: Union[Dict[str, Any], Unset]
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, EmailContentSubObject):
            content = self.content.to_dict()
        else:
            content = self.content.to_dict()

        render_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.render_options, Unset):
            render_options = self.render_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if content is not UNSET:
            field_dict["content"] = content
        if render_options is not UNSET:
            field_dict["render_options"] = render_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_content_sub_object import EmailContentSubObject
        from ..models.render_options_sub_object import RenderOptionsSubObject
        from ..models.sms_content_sub_object_create import SMSContentSubObjectCreate

        d = src_dict.copy()
        label = d.pop("label", UNSET)

        def _parse_content(data: object) -> Union["EmailContentSubObject", "SMSContentSubObjectCreate", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                content_type_0 = EmailContentSubObject.from_dict(data)

                return content_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            content_type_1 = SMSContentSubObjectCreate.from_dict(data)

            return content_type_1

        content = _parse_content(d.pop("content", UNSET))

        _render_options = d.pop("render_options", UNSET)
        render_options: Union[Unset, RenderOptionsSubObject]
        if isinstance(_render_options, Unset):
            render_options = UNSET
        else:
            render_options = RenderOptionsSubObject.from_dict(_render_options)

        campaign_message_partial_update_query_resource_object_attributes = cls(
            label=label,
            content=content,
            render_options=render_options,
        )

        campaign_message_partial_update_query_resource_object_attributes.additional_properties = d
        return campaign_message_partial_update_query_resource_object_attributes

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
