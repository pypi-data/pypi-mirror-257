from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.values_data import ValuesData


T = TypeVar("T", bound="PostCampaignValuesResponseDTODataAttributes")


@_attrs_define
class PostCampaignValuesResponseDTODataAttributes:
    """
    Attributes:
        results (List['ValuesData']): An array of all the returned values data.
            Each object in the array represents one unique grouping and the results for that grouping. Example:
            [{'groupings': {'send_channel': 'email', 'campaign_id': '01GMRWDSA0ARTAKE1SFX8JGXAY'}, 'statistics': {'opens':
            123, 'open_rate': 0.8253}}, {'groupings': {'send_channel': 'email', 'campaign_id':
            '01GJTHNWVG93F3KNX71SJ4FDBB'}, 'statistics': {'opens': 97, 'open_rate': 0.7562}}].
    """

    results: List["ValuesData"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.values_data import ValuesData

        d = src_dict.copy()
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = ValuesData.from_dict(results_item_data)

            results.append(results_item)

        post_campaign_values_response_dto_data_attributes = cls(
            results=results,
        )

        post_campaign_values_response_dto_data_attributes.additional_properties = d
        return post_campaign_values_response_dto_data_attributes

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
