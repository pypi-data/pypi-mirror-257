from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_series_request_dto_resource_object_attributes_interval import (
    FlowSeriesRequestDTOResourceObjectAttributesInterval,
)
from ..models.flow_series_request_dto_resource_object_attributes_statistics_item import (
    FlowSeriesRequestDTOResourceObjectAttributesStatisticsItem,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_timeframe import CustomTimeframe
    from ..models.timeframe import Timeframe


T = TypeVar("T", bound="FlowSeriesRequestDTOResourceObjectAttributes")


@_attrs_define
class FlowSeriesRequestDTOResourceObjectAttributes:
    """
    Attributes:
        statistics (List[FlowSeriesRequestDTOResourceObjectAttributesStatisticsItem]): List of statistics to query for.
            All rate statistics will be returned in fractional form [0.0, 1.0] Example: ['opens', 'open_rate'].
        timeframe (Union['CustomTimeframe', 'Timeframe']): The timeframe to query for data within. The max length a
            timeframe can be is 1 year
        interval (FlowSeriesRequestDTOResourceObjectAttributesInterval): The interval used to aggregate data within the
            series request.
            If hourly is used, the timeframe cannot be longer than 7 days.
            If daily is used, the timeframe cannot be longer than 60 days.
            If monthly is used, the timeframe cannot be longer than 52 weeks. Example: weekly.
        conversion_metric_id (str): ID of the metric to be used for conversion statistics Example: RESQ6t.
        filter_ (Union[Unset, str]): API filter string used to filter the query.
            Allowed filters are flow_id, send_channel, flow_message_id.
            Allowed operators are equals, contains-any.
            Only one filter can be used per attribute, only AND can be used as a combination operator.
            Max of 100 messages per ANY filter. Example: and(equals(flow_id,"abc123"),contains-
            any(send_channel,["email","sms"])).
    """

    statistics: List[FlowSeriesRequestDTOResourceObjectAttributesStatisticsItem]
    timeframe: Union["CustomTimeframe", "Timeframe"]
    interval: FlowSeriesRequestDTOResourceObjectAttributesInterval
    conversion_metric_id: str
    filter_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.timeframe import Timeframe

        statistics = []
        for statistics_item_data in self.statistics:
            statistics_item = statistics_item_data.value
            statistics.append(statistics_item)

        timeframe: Dict[str, Any]
        if isinstance(self.timeframe, Timeframe):
            timeframe = self.timeframe.to_dict()
        else:
            timeframe = self.timeframe.to_dict()

        interval = self.interval.value

        conversion_metric_id = self.conversion_metric_id

        filter_ = self.filter_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "statistics": statistics,
                "timeframe": timeframe,
                "interval": interval,
                "conversion_metric_id": conversion_metric_id,
            }
        )
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.custom_timeframe import CustomTimeframe
        from ..models.timeframe import Timeframe

        d = src_dict.copy()
        statistics = []
        _statistics = d.pop("statistics")
        for statistics_item_data in _statistics:
            statistics_item = FlowSeriesRequestDTOResourceObjectAttributesStatisticsItem(statistics_item_data)

            statistics.append(statistics_item)

        def _parse_timeframe(data: object) -> Union["CustomTimeframe", "Timeframe"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                timeframe_type_0 = Timeframe.from_dict(data)

                return timeframe_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            timeframe_type_1 = CustomTimeframe.from_dict(data)

            return timeframe_type_1

        timeframe = _parse_timeframe(d.pop("timeframe"))

        interval = FlowSeriesRequestDTOResourceObjectAttributesInterval(d.pop("interval"))

        conversion_metric_id = d.pop("conversion_metric_id")

        filter_ = d.pop("filter", UNSET)

        flow_series_request_dto_resource_object_attributes = cls(
            statistics=statistics,
            timeframe=timeframe,
            interval=interval,
            conversion_metric_id=conversion_metric_id,
            filter_=filter_,
        )

        flow_series_request_dto_resource_object_attributes.additional_properties = d
        return flow_series_request_dto_resource_object_attributes

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
