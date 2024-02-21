from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.campaign_message_response_object_resource import CampaignMessageResponseObjectResource
    from ..models.collection_links import CollectionLinks
    from ..models.get_campaign_response_collection_compound_document_data_item import (
        GetCampaignResponseCollectionCompoundDocumentDataItem,
    )
    from ..models.tag_response_object_resource import TagResponseObjectResource


T = TypeVar("T", bound="GetCampaignResponseCollectionCompoundDocument")


@_attrs_define
class GetCampaignResponseCollectionCompoundDocument:
    """
    Attributes:
        data (List['GetCampaignResponseCollectionCompoundDocumentDataItem']):
        links (CollectionLinks):
        included (Union[Unset, List[Union['CampaignMessageResponseObjectResource', 'TagResponseObjectResource']]]):
    """

    data: List["GetCampaignResponseCollectionCompoundDocumentDataItem"]
    links: "CollectionLinks"
    included: Union[Unset, List[Union["CampaignMessageResponseObjectResource", "TagResponseObjectResource"]]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.campaign_message_response_object_resource import CampaignMessageResponseObjectResource

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        links = self.links.to_dict()

        included: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.included, Unset):
            included = []
            for included_item_data in self.included:
                included_item: Dict[str, Any]
                if isinstance(included_item_data, CampaignMessageResponseObjectResource):
                    included_item = included_item_data.to_dict()
                else:
                    included_item = included_item_data.to_dict()

                included.append(included_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "links": links,
            }
        )
        if included is not UNSET:
            field_dict["included"] = included

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.campaign_message_response_object_resource import CampaignMessageResponseObjectResource
        from ..models.collection_links import CollectionLinks
        from ..models.get_campaign_response_collection_compound_document_data_item import (
            GetCampaignResponseCollectionCompoundDocumentDataItem,
        )
        from ..models.tag_response_object_resource import TagResponseObjectResource

        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = GetCampaignResponseCollectionCompoundDocumentDataItem.from_dict(data_item_data)

            data.append(data_item)

        links = CollectionLinks.from_dict(d.pop("links"))

        included = []
        _included = d.pop("included", UNSET)
        for included_item_data in _included or []:

            def _parse_included_item(
                data: object,
            ) -> Union["CampaignMessageResponseObjectResource", "TagResponseObjectResource"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    included_item_type_0 = CampaignMessageResponseObjectResource.from_dict(data)

                    return included_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                included_item_type_1 = TagResponseObjectResource.from_dict(data)

                return included_item_type_1

            included_item = _parse_included_item(included_item_data)

            included.append(included_item)

        get_campaign_response_collection_compound_document = cls(
            data=data,
            links=links,
            included=included,
        )

        get_campaign_response_collection_compound_document.additional_properties = d
        return get_campaign_response_collection_compound_document

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
