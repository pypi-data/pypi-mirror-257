from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_aggregate_row_dto_measurements import MetricAggregateRowDTOMeasurements


T = TypeVar("T", bound="MetricAggregateRowDTO")


@_attrs_define
class MetricAggregateRowDTO:
    """
    Attributes:
        dimensions (List[str]): List of dimensions associated with this set of measurements
        measurements (MetricAggregateRowDTOMeasurements): Dictionary of measurement_key, values
    """

    dimensions: List[str]
    measurements: "MetricAggregateRowDTOMeasurements"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dimensions = self.dimensions

        measurements = self.measurements.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dimensions": dimensions,
                "measurements": measurements,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_aggregate_row_dto_measurements import MetricAggregateRowDTOMeasurements

        d = src_dict.copy()
        dimensions = cast(List[str], d.pop("dimensions"))

        measurements = MetricAggregateRowDTOMeasurements.from_dict(d.pop("measurements"))

        metric_aggregate_row_dto = cls(
            dimensions=dimensions,
            measurements=measurements,
        )

        metric_aggregate_row_dto.additional_properties = d
        return metric_aggregate_row_dto

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
