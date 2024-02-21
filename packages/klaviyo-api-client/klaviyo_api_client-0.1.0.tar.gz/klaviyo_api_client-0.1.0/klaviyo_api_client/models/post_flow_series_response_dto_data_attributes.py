import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.series_data import SeriesData


T = TypeVar("T", bound="PostFlowSeriesResponseDTODataAttributes")


@_attrs_define
class PostFlowSeriesResponseDTODataAttributes:
    """
    Attributes:
        results (List['SeriesData']): An array of all the returned values data.
            Each object in the array represents one unique grouping and the results for that grouping.
            Each value in the results array corresponds to the date time at the same index. Example: [{'groupings':
            {'flow_id': 'XVTP5Q', 'send_channel': 'email', 'flow_message_id': '01GMRWDSA0ARTAKE1SFX8JGXAY'}, 'statistics':
            {'opens': [123, 156, 144], 'open_rate': [0.8253, 0.8722, 0.8398]}}, {'groupings': {'flow_id': 'XVTP5Q',
            'send_channel': 'email', 'flow_message_id': '01GJTHNWVG93F3KNX71SJ4FDBB'}, 'statistics': {'opens': [97, 98, 65],
            'open_rate': [0.7562, 0.761, 0.688]}}].
        date_times (List[datetime.datetime]): An array of date times which correspond to the equivalent index in the
            results data. Example: ['2024-01-05T00:00:00+00:00', '2024-01-06T00:00:00+00:00', '2024-01-07T00:00:00+00:00'].
    """

    results: List["SeriesData"]
    date_times: List[datetime.datetime]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        date_times = []
        for date_times_item_data in self.date_times:
            date_times_item = date_times_item_data.isoformat()
            date_times.append(date_times_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
                "date_times": date_times,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.series_data import SeriesData

        d = src_dict.copy()
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = SeriesData.from_dict(results_item_data)

            results.append(results_item)

        date_times = []
        _date_times = d.pop("date_times")
        for date_times_item_data in _date_times:
            date_times_item = isoparse(date_times_item_data)

            date_times.append(date_times_item)

        post_flow_series_response_dto_data_attributes = cls(
            results=results,
            date_times=date_times,
        )

        post_flow_series_response_dto_data_attributes.additional_properties = d
        return post_flow_series_response_dto_data_attributes

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
