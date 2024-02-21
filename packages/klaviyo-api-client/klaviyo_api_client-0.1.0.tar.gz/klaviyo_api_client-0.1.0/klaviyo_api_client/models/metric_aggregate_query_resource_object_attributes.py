from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_aggregate_query_resource_object_attributes_by_item import (
    MetricAggregateQueryResourceObjectAttributesByItem,
)
from ..models.metric_aggregate_query_resource_object_attributes_interval import (
    MetricAggregateQueryResourceObjectAttributesInterval,
)
from ..models.metric_aggregate_query_resource_object_attributes_measurements_item import (
    MetricAggregateQueryResourceObjectAttributesMeasurementsItem,
)
from ..models.metric_aggregate_query_resource_object_attributes_sort import (
    MetricAggregateQueryResourceObjectAttributesSort,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricAggregateQueryResourceObjectAttributes")


@_attrs_define
class MetricAggregateQueryResourceObjectAttributes:
    """
    Attributes:
        metric_id (str): The metric ID used in the aggregation. Example: 0rG4eQ.
        measurements (List[MetricAggregateQueryResourceObjectAttributesMeasurementsItem]): Measurement key, e.g.
            `unique`, `sum_value`, `count` Example: count.
        filter_ (List[str]): List of filters, must include time range using ISO 8601 format (YYYY-MM-
            DDTHH:MM:SS.mmmmmm).
                        These filters follow a similar format to those in `GET` requests, the primary difference is that
            this endpoint asks for a list.
                        The time range can be filtered by providing a `greater-or-equal` and a `less-than` filter on the
            `datetime` field. Example: ['greater-or-equal(datetime,2022-12-01T00:00:00)', 'less-
            than(datetime,2022-12-08T00:00:00'].
        page_cursor (Union[Unset, str]): Optional pagination cursor to iterate over large result sets
        interval (Union[Unset, MetricAggregateQueryResourceObjectAttributesInterval]): Aggregation interval, e.g.
            "hour", "day", "week", "month" Default: MetricAggregateQueryResourceObjectAttributesInterval.DAY. Example: day.
        page_size (Union[Unset, int]): Alter the maximum number of returned rows in a single page of aggregation results
            Default: 500. Example: 500.
        by (Union[Unset, List[MetricAggregateQueryResourceObjectAttributesByItem]]): Optional attribute(s) used for
            partitioning by the aggregation function Example: $message.
        return_fields (Union[Unset, List[str]]): Provide fields to limit the returned data
        timezone (Union[Unset, str]): The timezone used for processing the query, e.g. `'America/New_York'`.
                        This field is validated against a list of common timezones from the [IANA Time Zone
            Database](https://www.iana.org/time-zones).
                        While most are supported, a few notable exceptions are `Factory`, `Europe/Kyiv` and
            `Pacific/Kanton`. This field is case-sensitive. Default: 'UTC'. Example: America/New_York.
        sort (Union[Unset, MetricAggregateQueryResourceObjectAttributesSort]): Provide a sort key (e.g. -$message)
    """

    metric_id: str
    measurements: List[MetricAggregateQueryResourceObjectAttributesMeasurementsItem]
    filter_: List[str]
    page_cursor: Union[Unset, str] = UNSET
    interval: Union[
        Unset, MetricAggregateQueryResourceObjectAttributesInterval
    ] = MetricAggregateQueryResourceObjectAttributesInterval.DAY
    page_size: Union[Unset, int] = 500
    by: Union[Unset, List[MetricAggregateQueryResourceObjectAttributesByItem]] = UNSET
    return_fields: Union[Unset, List[str]] = UNSET
    timezone: Union[Unset, str] = "UTC"
    sort: Union[Unset, MetricAggregateQueryResourceObjectAttributesSort] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metric_id = self.metric_id

        measurements = []
        for measurements_item_data in self.measurements:
            measurements_item = measurements_item_data.value
            measurements.append(measurements_item)

        filter_ = self.filter_

        page_cursor = self.page_cursor

        interval: Union[Unset, str] = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.value

        page_size = self.page_size

        by: Union[Unset, List[str]] = UNSET
        if not isinstance(self.by, Unset):
            by = []
            for by_item_data in self.by:
                by_item = by_item_data.value
                by.append(by_item)

        return_fields: Union[Unset, List[str]] = UNSET
        if not isinstance(self.return_fields, Unset):
            return_fields = self.return_fields

        timezone = self.timezone

        sort: Union[Unset, str] = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric_id": metric_id,
                "measurements": measurements,
                "filter": filter_,
            }
        )
        if page_cursor is not UNSET:
            field_dict["page_cursor"] = page_cursor
        if interval is not UNSET:
            field_dict["interval"] = interval
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if by is not UNSET:
            field_dict["by"] = by
        if return_fields is not UNSET:
            field_dict["return_fields"] = return_fields
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metric_id = d.pop("metric_id")

        measurements = []
        _measurements = d.pop("measurements")
        for measurements_item_data in _measurements:
            measurements_item = MetricAggregateQueryResourceObjectAttributesMeasurementsItem(measurements_item_data)

            measurements.append(measurements_item)

        filter_ = cast(List[str], d.pop("filter"))

        page_cursor = d.pop("page_cursor", UNSET)

        _interval = d.pop("interval", UNSET)
        interval: Union[Unset, MetricAggregateQueryResourceObjectAttributesInterval]
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = MetricAggregateQueryResourceObjectAttributesInterval(_interval)

        page_size = d.pop("page_size", UNSET)

        by = []
        _by = d.pop("by", UNSET)
        for by_item_data in _by or []:
            by_item = MetricAggregateQueryResourceObjectAttributesByItem(by_item_data)

            by.append(by_item)

        return_fields = cast(List[str], d.pop("return_fields", UNSET))

        timezone = d.pop("timezone", UNSET)

        _sort = d.pop("sort", UNSET)
        sort: Union[Unset, MetricAggregateQueryResourceObjectAttributesSort]
        if isinstance(_sort, Unset):
            sort = UNSET
        else:
            sort = MetricAggregateQueryResourceObjectAttributesSort(_sort)

        metric_aggregate_query_resource_object_attributes = cls(
            metric_id=metric_id,
            measurements=measurements,
            filter_=filter_,
            page_cursor=page_cursor,
            interval=interval,
            page_size=page_size,
            by=by,
            return_fields=return_fields,
            timezone=timezone,
            sort=sort,
        )

        metric_aggregate_query_resource_object_attributes.additional_properties = d
        return metric_aggregate_query_resource_object_attributes

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
