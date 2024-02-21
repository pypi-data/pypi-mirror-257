from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.series_data_groupings import SeriesDataGroupings
    from ..models.series_data_statistics import SeriesDataStatistics


T = TypeVar("T", bound="SeriesData")


@_attrs_define
class SeriesData:
    """
    Attributes:
        groupings (SeriesDataGroupings): Applied groupings and the values for this object
        statistics (SeriesDataStatistics): Requested statistics and their series result
    """

    groupings: "SeriesDataGroupings"
    statistics: "SeriesDataStatistics"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        groupings = self.groupings.to_dict()

        statistics = self.statistics.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupings": groupings,
                "statistics": statistics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.series_data_groupings import SeriesDataGroupings
        from ..models.series_data_statistics import SeriesDataStatistics

        d = src_dict.copy()
        groupings = SeriesDataGroupings.from_dict(d.pop("groupings"))

        statistics = SeriesDataStatistics.from_dict(d.pop("statistics"))

        series_data = cls(
            groupings=groupings,
            statistics=statistics,
        )

        series_data.additional_properties = d
        return series_data

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
