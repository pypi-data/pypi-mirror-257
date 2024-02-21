import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PredictiveAnalytics")


@_attrs_define
class PredictiveAnalytics:
    """
    Attributes:
        historic_clv (Union[Unset, float]): Total value of all historically placed orders Example: 93.87.
        predicted_clv (Union[Unset, float]): Predicted value of all placed orders in the next 365 days Example: 27.24.
        total_clv (Union[Unset, float]): Sum of historic and predicted CLV Example: 121.11.
        historic_number_of_orders (Union[Unset, int]): Number of already placed orders Example: 2.
        predicted_number_of_orders (Union[Unset, float]): Predicted number of placed orders in the next 365 days
            Example: 0.54.
        average_days_between_orders (Union[Unset, float]): Average number of days between orders (None if only one order
            has been placed) Example: 189.
        average_order_value (Union[Unset, float]): Average value of placed orders Example: 46.94.
        churn_probability (Union[Unset, float]): Probability the customer has churned Example: 0.89.
        expected_date_of_next_order (Union[Unset, datetime.datetime]): Expected date of next order, as calculated at the
            time of their most recent order Example: 2022-11-08T00:00:00.
    """

    historic_clv: Union[Unset, float] = UNSET
    predicted_clv: Union[Unset, float] = UNSET
    total_clv: Union[Unset, float] = UNSET
    historic_number_of_orders: Union[Unset, int] = UNSET
    predicted_number_of_orders: Union[Unset, float] = UNSET
    average_days_between_orders: Union[Unset, float] = UNSET
    average_order_value: Union[Unset, float] = UNSET
    churn_probability: Union[Unset, float] = UNSET
    expected_date_of_next_order: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        historic_clv = self.historic_clv

        predicted_clv = self.predicted_clv

        total_clv = self.total_clv

        historic_number_of_orders = self.historic_number_of_orders

        predicted_number_of_orders = self.predicted_number_of_orders

        average_days_between_orders = self.average_days_between_orders

        average_order_value = self.average_order_value

        churn_probability = self.churn_probability

        expected_date_of_next_order: Union[Unset, str] = UNSET
        if not isinstance(self.expected_date_of_next_order, Unset):
            expected_date_of_next_order = self.expected_date_of_next_order.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if historic_clv is not UNSET:
            field_dict["historic_clv"] = historic_clv
        if predicted_clv is not UNSET:
            field_dict["predicted_clv"] = predicted_clv
        if total_clv is not UNSET:
            field_dict["total_clv"] = total_clv
        if historic_number_of_orders is not UNSET:
            field_dict["historic_number_of_orders"] = historic_number_of_orders
        if predicted_number_of_orders is not UNSET:
            field_dict["predicted_number_of_orders"] = predicted_number_of_orders
        if average_days_between_orders is not UNSET:
            field_dict["average_days_between_orders"] = average_days_between_orders
        if average_order_value is not UNSET:
            field_dict["average_order_value"] = average_order_value
        if churn_probability is not UNSET:
            field_dict["churn_probability"] = churn_probability
        if expected_date_of_next_order is not UNSET:
            field_dict["expected_date_of_next_order"] = expected_date_of_next_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        historic_clv = d.pop("historic_clv", UNSET)

        predicted_clv = d.pop("predicted_clv", UNSET)

        total_clv = d.pop("total_clv", UNSET)

        historic_number_of_orders = d.pop("historic_number_of_orders", UNSET)

        predicted_number_of_orders = d.pop("predicted_number_of_orders", UNSET)

        average_days_between_orders = d.pop("average_days_between_orders", UNSET)

        average_order_value = d.pop("average_order_value", UNSET)

        churn_probability = d.pop("churn_probability", UNSET)

        _expected_date_of_next_order = d.pop("expected_date_of_next_order", UNSET)
        expected_date_of_next_order: Union[Unset, datetime.datetime]
        if isinstance(_expected_date_of_next_order, Unset):
            expected_date_of_next_order = UNSET
        else:
            expected_date_of_next_order = isoparse(_expected_date_of_next_order)

        predictive_analytics = cls(
            historic_clv=historic_clv,
            predicted_clv=predicted_clv,
            total_clv=total_clv,
            historic_number_of_orders=historic_number_of_orders,
            predicted_number_of_orders=predicted_number_of_orders,
            average_days_between_orders=average_days_between_orders,
            average_order_value=average_order_value,
            churn_probability=churn_probability,
            expected_date_of_next_order=expected_date_of_next_order,
        )

        predictive_analytics.additional_properties = d
        return predictive_analytics

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
