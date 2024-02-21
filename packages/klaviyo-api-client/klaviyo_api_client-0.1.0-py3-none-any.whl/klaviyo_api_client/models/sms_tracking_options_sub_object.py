from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.utm_params_sub_object import UTMParamsSubObject


T = TypeVar("T", bound="SMSTrackingOptionsSubObject")


@_attrs_define
class SMSTrackingOptionsSubObject:
    """
    Attributes:
        is_add_utm (Union[Unset, bool]): Whether the campaign needs UTM parameters. If set to False, UTM params will not
            be used.
        utm_params (Union[Unset, List['UTMParamsSubObject']]): A list of UTM parameters. If an empty list is given and
            is_add_utm is True, uses company defaults.
    """

    is_add_utm: Union[Unset, bool] = UNSET
    utm_params: Union[Unset, List["UTMParamsSubObject"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_add_utm = self.is_add_utm

        utm_params: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.utm_params, Unset):
            utm_params = []
            for utm_params_item_data in self.utm_params:
                utm_params_item = utm_params_item_data.to_dict()
                utm_params.append(utm_params_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_add_utm is not UNSET:
            field_dict["is_add_utm"] = is_add_utm
        if utm_params is not UNSET:
            field_dict["utm_params"] = utm_params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.utm_params_sub_object import UTMParamsSubObject

        d = src_dict.copy()
        is_add_utm = d.pop("is_add_utm", UNSET)

        utm_params = []
        _utm_params = d.pop("utm_params", UNSET)
        for utm_params_item_data in _utm_params or []:
            utm_params_item = UTMParamsSubObject.from_dict(utm_params_item_data)

            utm_params.append(utm_params_item)

        sms_tracking_options_sub_object = cls(
            is_add_utm=is_add_utm,
            utm_params=utm_params,
        )

        sms_tracking_options_sub_object.additional_properties = d
        return sms_tracking_options_sub_object

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
