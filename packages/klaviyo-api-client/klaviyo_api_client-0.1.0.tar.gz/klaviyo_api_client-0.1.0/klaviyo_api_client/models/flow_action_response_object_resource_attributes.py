import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_tracking_options import EmailTrackingOptions
    from ..models.flow_action_response_object_resource_attributes_settings import (
        FlowActionResponseObjectResourceAttributesSettings,
    )
    from ..models.send_options import SendOptions
    from ..models.sms_render_options import SMSRenderOptions
    from ..models.sms_tracking_options import SMSTrackingOptions


T = TypeVar("T", bound="FlowActionResponseObjectResourceAttributes")


@_attrs_define
class FlowActionResponseObjectResourceAttributes:
    """
    Attributes:
        action_type (Union[Unset, str]):
        status (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]):  Example: 2022-11-08T00:00:00.
        settings (Union[Unset, FlowActionResponseObjectResourceAttributesSettings]):
        tracking_options (Union['EmailTrackingOptions', 'SMSTrackingOptions', Unset]):
        send_options (Union[Unset, SendOptions]):
        render_options (Union[Unset, SMSRenderOptions]):
    """

    action_type: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    settings: Union[Unset, "FlowActionResponseObjectResourceAttributesSettings"] = UNSET
    tracking_options: Union["EmailTrackingOptions", "SMSTrackingOptions", Unset] = UNSET
    send_options: Union[Unset, "SendOptions"] = UNSET
    render_options: Union[Unset, "SMSRenderOptions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.email_tracking_options import EmailTrackingOptions

        action_type = self.action_type

        status = self.status

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        tracking_options: Union[Dict[str, Any], Unset]
        if isinstance(self.tracking_options, Unset):
            tracking_options = UNSET
        elif isinstance(self.tracking_options, EmailTrackingOptions):
            tracking_options = self.tracking_options.to_dict()
        else:
            tracking_options = self.tracking_options.to_dict()

        send_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.send_options, Unset):
            send_options = self.send_options.to_dict()

        render_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.render_options, Unset):
            render_options = self.render_options.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if action_type is not UNSET:
            field_dict["action_type"] = action_type
        if status is not UNSET:
            field_dict["status"] = status
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated
        if settings is not UNSET:
            field_dict["settings"] = settings
        if tracking_options is not UNSET:
            field_dict["tracking_options"] = tracking_options
        if send_options is not UNSET:
            field_dict["send_options"] = send_options
        if render_options is not UNSET:
            field_dict["render_options"] = render_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.email_tracking_options import EmailTrackingOptions
        from ..models.flow_action_response_object_resource_attributes_settings import (
            FlowActionResponseObjectResourceAttributesSettings,
        )
        from ..models.send_options import SendOptions
        from ..models.sms_render_options import SMSRenderOptions
        from ..models.sms_tracking_options import SMSTrackingOptions

        d = src_dict.copy()
        action_type = d.pop("action_type", UNSET)

        status = d.pop("status", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, FlowActionResponseObjectResourceAttributesSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = FlowActionResponseObjectResourceAttributesSettings.from_dict(_settings)

        def _parse_tracking_options(data: object) -> Union["EmailTrackingOptions", "SMSTrackingOptions", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tracking_options_type_0 = EmailTrackingOptions.from_dict(data)

                return tracking_options_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            tracking_options_type_1 = SMSTrackingOptions.from_dict(data)

            return tracking_options_type_1

        tracking_options = _parse_tracking_options(d.pop("tracking_options", UNSET))

        _send_options = d.pop("send_options", UNSET)
        send_options: Union[Unset, SendOptions]
        if isinstance(_send_options, Unset):
            send_options = UNSET
        else:
            send_options = SendOptions.from_dict(_send_options)

        _render_options = d.pop("render_options", UNSET)
        render_options: Union[Unset, SMSRenderOptions]
        if isinstance(_render_options, Unset):
            render_options = UNSET
        else:
            render_options = SMSRenderOptions.from_dict(_render_options)

        flow_action_response_object_resource_attributes = cls(
            action_type=action_type,
            status=status,
            created=created,
            updated=updated,
            settings=settings,
            tracking_options=tracking_options,
            send_options=send_options,
            render_options=render_options,
        )

        flow_action_response_object_resource_attributes.additional_properties = d
        return flow_action_response_object_resource_attributes

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
