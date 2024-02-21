import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.metric_aggregate_row_dto import MetricAggregateRowDTO


T = TypeVar("T", bound="PostMetricAggregateResponseDataAttributes")


@_attrs_define
class PostMetricAggregateResponseDataAttributes:
    """
    Attributes:
        dates (List[datetime.datetime]): The dates of the query range
        data (List['MetricAggregateRowDTO']): Aggregation result data
    """

    dates: List[datetime.datetime]
    data: List["MetricAggregateRowDTO"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dates = []
        for dates_item_data in self.dates:
            dates_item = dates_item_data.isoformat()
            dates.append(dates_item)

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dates": dates,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_aggregate_row_dto import MetricAggregateRowDTO

        d = src_dict.copy()
        dates = []
        _dates = d.pop("dates")
        for dates_item_data in _dates:
            dates_item = isoparse(dates_item_data)

            dates.append(dates_item)

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = MetricAggregateRowDTO.from_dict(data_item_data)

            data.append(data_item)

        post_metric_aggregate_response_data_attributes = cls(
            dates=dates,
            data=data,
        )

        post_metric_aggregate_response_data_attributes.additional_properties = d
        return post_metric_aggregate_response_data_attributes

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
