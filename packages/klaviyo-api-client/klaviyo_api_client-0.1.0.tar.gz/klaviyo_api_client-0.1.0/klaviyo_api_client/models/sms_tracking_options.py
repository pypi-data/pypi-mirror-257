from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.utm_param_info import UtmParamInfo


T = TypeVar("T", bound="SMSTrackingOptions")


@_attrs_define
class SMSTrackingOptions:
    """
    Attributes:
        add_utm (bool):
        utm_params (List['UtmParamInfo']):
    """

    add_utm: bool
    utm_params: List["UtmParamInfo"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        add_utm = self.add_utm

        utm_params = []
        for utm_params_item_data in self.utm_params:
            utm_params_item = utm_params_item_data.to_dict()
            utm_params.append(utm_params_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "add_utm": add_utm,
                "utm_params": utm_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.utm_param_info import UtmParamInfo

        d = src_dict.copy()
        add_utm = d.pop("add_utm")

        utm_params = []
        _utm_params = d.pop("utm_params")
        for utm_params_item_data in _utm_params:
            utm_params_item = UtmParamInfo.from_dict(utm_params_item_data)

            utm_params.append(utm_params_item)

        sms_tracking_options = cls(
            add_utm=add_utm,
            utm_params=utm_params,
        )

        sms_tracking_options.additional_properties = d
        return sms_tracking_options

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
