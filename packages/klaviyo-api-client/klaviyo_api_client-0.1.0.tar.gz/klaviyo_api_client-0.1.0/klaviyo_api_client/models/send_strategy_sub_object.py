from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.static_schedule_options import StaticScheduleOptions
    from ..models.sto_schedule_options import STOScheduleOptions
    from ..models.throttled_schedule_options import ThrottledScheduleOptions


T = TypeVar("T", bound="SendStrategySubObject")


@_attrs_define
class SendStrategySubObject:
    """
    Attributes:
        method (str): Describes the shape of the options object. Allowed values: ['static', 'throttled', 'immediate',
            'smart_send_time'] Example: static.
        options_static (Union[Unset, StaticScheduleOptions]):
        options_throttled (Union[Unset, ThrottledScheduleOptions]):
        options_sto (Union[Unset, STOScheduleOptions]):
    """

    method: str
    options_static: Union[Unset, "StaticScheduleOptions"] = UNSET
    options_throttled: Union[Unset, "ThrottledScheduleOptions"] = UNSET
    options_sto: Union[Unset, "STOScheduleOptions"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        method = self.method

        options_static: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options_static, Unset):
            options_static = self.options_static.to_dict()

        options_throttled: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options_throttled, Unset):
            options_throttled = self.options_throttled.to_dict()

        options_sto: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.options_sto, Unset):
            options_sto = self.options_sto.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "method": method,
            }
        )
        if options_static is not UNSET:
            field_dict["options_static"] = options_static
        if options_throttled is not UNSET:
            field_dict["options_throttled"] = options_throttled
        if options_sto is not UNSET:
            field_dict["options_sto"] = options_sto

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.static_schedule_options import StaticScheduleOptions
        from ..models.sto_schedule_options import STOScheduleOptions
        from ..models.throttled_schedule_options import ThrottledScheduleOptions

        d = src_dict.copy()
        method = d.pop("method")

        _options_static = d.pop("options_static", UNSET)
        options_static: Union[Unset, StaticScheduleOptions]
        if isinstance(_options_static, Unset):
            options_static = UNSET
        else:
            options_static = StaticScheduleOptions.from_dict(_options_static)

        _options_throttled = d.pop("options_throttled", UNSET)
        options_throttled: Union[Unset, ThrottledScheduleOptions]
        if isinstance(_options_throttled, Unset):
            options_throttled = UNSET
        else:
            options_throttled = ThrottledScheduleOptions.from_dict(_options_throttled)

        _options_sto = d.pop("options_sto", UNSET)
        options_sto: Union[Unset, STOScheduleOptions]
        if isinstance(_options_sto, Unset):
            options_sto = UNSET
        else:
            options_sto = STOScheduleOptions.from_dict(_options_sto)

        send_strategy_sub_object = cls(
            method=method,
            options_static=options_static,
            options_throttled=options_throttled,
            options_sto=options_sto,
        )

        send_strategy_sub_object.additional_properties = d
        return send_strategy_sub_object

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
