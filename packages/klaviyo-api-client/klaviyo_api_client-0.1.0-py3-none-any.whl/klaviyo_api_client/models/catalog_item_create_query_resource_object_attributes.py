from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_item_create_query_resource_object_attributes_integration_type import (
    CatalogItemCreateQueryResourceObjectAttributesIntegrationType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_item_create_query_resource_object_attributes_custom_metadata import (
        CatalogItemCreateQueryResourceObjectAttributesCustomMetadata,
    )


T = TypeVar("T", bound="CatalogItemCreateQueryResourceObjectAttributes")


@_attrs_define
class CatalogItemCreateQueryResourceObjectAttributes:
    """
    Attributes:
        external_id (str): The ID of the catalog item in an external system. Example: SAMPLE-DATA-ITEM-1.
        title (str): The title of the catalog item. Example: Ocean Blue Shirt (Sample).
        description (str): A description of the catalog item. Example: Ocean blue cotton shirt with a narrow collar and
            buttons down the front and long sleeves. Comfortable fit and titled kaleidoscope patterns..
        url (str): URL pointing to the location of the catalog item on your website. Example:
            https://via.placeholder.com/150.
        integration_type (Union[Unset, CatalogItemCreateQueryResourceObjectAttributesIntegrationType]): The integration
            type. Currently only "$custom" is supported. Default:
            CatalogItemCreateQueryResourceObjectAttributesIntegrationType.VALUE_0. Example: $custom.
        price (Union[Unset, float]): This field can be used to set the price on the catalog item, which is what gets
            displayed for the item when included in emails. For most price-update use cases, you will also want to update
            the `price` on any child variants, using the [Update Catalog Variant
            Endpoint](https://developers.klaviyo.com/en/reference/update_catalog_variant). Example: 42.
        catalog_type (Union[Unset, str]): The type of catalog. Currently only "$default" is supported. Default:
            '$default'. Example: $default.
        image_full_url (Union[Unset, str]): URL pointing to the location of a full image of the catalog item. Example:
            https://via.placeholder.com/300.
        image_thumbnail_url (Union[Unset, str]): URL pointing to the location of an image thumbnail of the catalog item
            Example: https://via.placeholder.com/150.
        images (Union[Unset, List[str]]): List of URLs pointing to the locations of images of the catalog item. Example:
            ['https://via.placeholder.com/150'].
        custom_metadata (Union[Unset, CatalogItemCreateQueryResourceObjectAttributesCustomMetadata]): Flat JSON blob to
            provide custom metadata about the catalog item. May not exceed 100kb. Example: {'Top Pick': True}.
        published (Union[Unset, bool]): Boolean value indicating whether the catalog item is published. Default: True.
            Example: True.
    """

    external_id: str
    title: str
    description: str
    url: str
    integration_type: Union[
        Unset, CatalogItemCreateQueryResourceObjectAttributesIntegrationType
    ] = CatalogItemCreateQueryResourceObjectAttributesIntegrationType.VALUE_0
    price: Union[Unset, float] = UNSET
    catalog_type: Union[Unset, str] = "$default"
    image_full_url: Union[Unset, str] = UNSET
    image_thumbnail_url: Union[Unset, str] = UNSET
    images: Union[Unset, List[str]] = UNSET
    custom_metadata: Union[Unset, "CatalogItemCreateQueryResourceObjectAttributesCustomMetadata"] = UNSET
    published: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id

        title = self.title

        description = self.description

        url = self.url

        integration_type: Union[Unset, str] = UNSET
        if not isinstance(self.integration_type, Unset):
            integration_type = self.integration_type.value

        price = self.price

        catalog_type = self.catalog_type

        image_full_url = self.image_full_url

        image_thumbnail_url = self.image_thumbnail_url

        images: Union[Unset, List[str]] = UNSET
        if not isinstance(self.images, Unset):
            images = self.images

        custom_metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_metadata, Unset):
            custom_metadata = self.custom_metadata.to_dict()

        published = self.published

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "external_id": external_id,
                "title": title,
                "description": description,
                "url": url,
            }
        )
        if integration_type is not UNSET:
            field_dict["integration_type"] = integration_type
        if price is not UNSET:
            field_dict["price"] = price
        if catalog_type is not UNSET:
            field_dict["catalog_type"] = catalog_type
        if image_full_url is not UNSET:
            field_dict["image_full_url"] = image_full_url
        if image_thumbnail_url is not UNSET:
            field_dict["image_thumbnail_url"] = image_thumbnail_url
        if images is not UNSET:
            field_dict["images"] = images
        if custom_metadata is not UNSET:
            field_dict["custom_metadata"] = custom_metadata
        if published is not UNSET:
            field_dict["published"] = published

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_item_create_query_resource_object_attributes_custom_metadata import (
            CatalogItemCreateQueryResourceObjectAttributesCustomMetadata,
        )

        d = src_dict.copy()
        external_id = d.pop("external_id")

        title = d.pop("title")

        description = d.pop("description")

        url = d.pop("url")

        _integration_type = d.pop("integration_type", UNSET)
        integration_type: Union[Unset, CatalogItemCreateQueryResourceObjectAttributesIntegrationType]
        if isinstance(_integration_type, Unset):
            integration_type = UNSET
        else:
            integration_type = CatalogItemCreateQueryResourceObjectAttributesIntegrationType(_integration_type)

        price = d.pop("price", UNSET)

        catalog_type = d.pop("catalog_type", UNSET)

        image_full_url = d.pop("image_full_url", UNSET)

        image_thumbnail_url = d.pop("image_thumbnail_url", UNSET)

        images = cast(List[str], d.pop("images", UNSET))

        _custom_metadata = d.pop("custom_metadata", UNSET)
        custom_metadata: Union[Unset, CatalogItemCreateQueryResourceObjectAttributesCustomMetadata]
        if isinstance(_custom_metadata, Unset):
            custom_metadata = UNSET
        else:
            custom_metadata = CatalogItemCreateQueryResourceObjectAttributesCustomMetadata.from_dict(_custom_metadata)

        published = d.pop("published", UNSET)

        catalog_item_create_query_resource_object_attributes = cls(
            external_id=external_id,
            title=title,
            description=description,
            url=url,
            integration_type=integration_type,
            price=price,
            catalog_type=catalog_type,
            image_full_url=image_full_url,
            image_thumbnail_url=image_thumbnail_url,
            images=images,
            custom_metadata=custom_metadata,
            published=published,
        )

        catalog_item_create_query_resource_object_attributes.additional_properties = d
        return catalog_item_create_query_resource_object_attributes

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
