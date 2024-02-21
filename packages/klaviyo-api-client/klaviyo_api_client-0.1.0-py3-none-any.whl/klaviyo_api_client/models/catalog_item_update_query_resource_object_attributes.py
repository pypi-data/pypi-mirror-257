from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_item_update_query_resource_object_attributes_custom_metadata import (
        CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata,
    )


T = TypeVar("T", bound="CatalogItemUpdateQueryResourceObjectAttributes")


@_attrs_define
class CatalogItemUpdateQueryResourceObjectAttributes:
    """
    Attributes:
        title (Union[Unset, str]): The title of the catalog item. Example: Ocean Blue Shirt (Sample).
        price (Union[Unset, float]): This field can be used to set the price on the catalog item, which is what gets
            displayed for the item when included in emails. For most price-update use cases, you will also want to update
            the `price` on any child variants, using the [Update Catalog Variant
            Endpoint](https://developers.klaviyo.com/en/reference/update_catalog_variant). Example: 42.
        description (Union[Unset, str]): A description of the catalog item. Example: A description of the catalog item..
        url (Union[Unset, str]): URL pointing to the location of the catalog item on your website. Example:
            https://via.placeholder.com/150.
        image_full_url (Union[Unset, str]): URL pointing to the location of a full image of the catalog item. Example:
            https://via.placeholder.com/300.
        image_thumbnail_url (Union[Unset, str]): URL pointing to the location of an image thumbnail of the catalog item
            Example: https://via.placeholder.com/150.
        images (Union[Unset, List[str]]): List of URLs pointing to the locations of images of the catalog item. Example:
            ['https://via.placeholder.com/150'].
        custom_metadata (Union[Unset, CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata]): Flat JSON blob to
            provide custom metadata about the catalog item. May not exceed 100kb. Example: {'Top Pick': True}.
        published (Union[Unset, bool]): Boolean value indicating whether the catalog item is published. Example: True.
    """

    title: Union[Unset, str] = UNSET
    price: Union[Unset, float] = UNSET
    description: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    image_full_url: Union[Unset, str] = UNSET
    image_thumbnail_url: Union[Unset, str] = UNSET
    images: Union[Unset, List[str]] = UNSET
    custom_metadata: Union[Unset, "CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata"] = UNSET
    published: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title

        price = self.price

        description = self.description

        url = self.url

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
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if price is not UNSET:
            field_dict["price"] = price
        if description is not UNSET:
            field_dict["description"] = description
        if url is not UNSET:
            field_dict["url"] = url
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
        from ..models.catalog_item_update_query_resource_object_attributes_custom_metadata import (
            CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata,
        )

        d = src_dict.copy()
        title = d.pop("title", UNSET)

        price = d.pop("price", UNSET)

        description = d.pop("description", UNSET)

        url = d.pop("url", UNSET)

        image_full_url = d.pop("image_full_url", UNSET)

        image_thumbnail_url = d.pop("image_thumbnail_url", UNSET)

        images = cast(List[str], d.pop("images", UNSET))

        _custom_metadata = d.pop("custom_metadata", UNSET)
        custom_metadata: Union[Unset, CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata]
        if isinstance(_custom_metadata, Unset):
            custom_metadata = UNSET
        else:
            custom_metadata = CatalogItemUpdateQueryResourceObjectAttributesCustomMetadata.from_dict(_custom_metadata)

        published = d.pop("published", UNSET)

        catalog_item_update_query_resource_object_attributes = cls(
            title=title,
            price=price,
            description=description,
            url=url,
            image_full_url=image_full_url,
            image_thumbnail_url=image_thumbnail_url,
            images=images,
            custom_metadata=custom_metadata,
            published=published,
        )

        catalog_item_update_query_resource_object_attributes.additional_properties = d
        return catalog_item_update_query_resource_object_attributes

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
