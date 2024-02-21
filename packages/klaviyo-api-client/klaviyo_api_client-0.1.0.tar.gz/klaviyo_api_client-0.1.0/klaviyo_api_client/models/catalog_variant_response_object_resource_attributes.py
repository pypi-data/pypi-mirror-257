import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.catalog_variant_response_object_resource_attributes_inventory_policy import (
    CatalogVariantResponseObjectResourceAttributesInventoryPolicy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_variant_response_object_resource_attributes_custom_metadata import (
        CatalogVariantResponseObjectResourceAttributesCustomMetadata,
    )


T = TypeVar("T", bound="CatalogVariantResponseObjectResourceAttributes")


@_attrs_define
class CatalogVariantResponseObjectResourceAttributes:
    """
    Attributes:
        external_id (Union[Unset, str]): The ID of the catalog item variant in an external system. Example: SAMPLE-DATA-
            ITEM-1-VARIANT-MEDIUM.
        title (Union[Unset, str]): The title of the catalog item variant. Example: Ocean Blue Shirt (Sample) Variant
            Medium.
        description (Union[Unset, str]): A description of the catalog item variant. Example: Ocean blue cotton shirt
            with a narrow collar and buttons down the front and long sleeves. Comfortable fit and titled kaleidoscope
            patterns..
        sku (Union[Unset, str]): The SKU of the catalog item variant. Example: OBS-MD.
        inventory_policy (Union[Unset, CatalogVariantResponseObjectResourceAttributesInventoryPolicy]): This field
            controls the visibility of this catalog item variant in product feeds/blocks. This field supports the following
            values:
            `1`: a product will not appear in dynamic product recommendation feeds and blocks if it is out of stock.
            `0` or `2`: a product can appear in dynamic product recommendation feeds and blocks regardless of inventory
            quantity. Example: 2.
        inventory_quantity (Union[Unset, float]): The quantity of the catalog item variant currently in stock. Example:
            25.
        price (Union[Unset, float]): This field can be used to set the price on the catalog item variant, which is what
            gets displayed for the item variant when included in emails. For most price-update use cases, you will also want
            to update the `price` on any parent items using the [Update Catalog Item
            Endpoint](https://developers.klaviyo.com/en/reference/update_catalog_item). Example: 42.
        url (Union[Unset, str]): URL pointing to the location of the catalog item variant on your website. Example:
            https://via.placeholder.com/150.
        image_full_url (Union[Unset, str]): URL pointing to the location of a full image of the catalog item variant.
            Example: https://via.placeholder.com/300.
        image_thumbnail_url (Union[Unset, str]): URL pointing to the location of an image thumbnail of the catalog item
            variant. Example: https://via.placeholder.com/150.
        images (Union[Unset, List[str]]): List of URLs pointing to the locations of images of the catalog item variant.
            Example: ['https://via.placeholder.com/150'].
        custom_metadata (Union[Unset, CatalogVariantResponseObjectResourceAttributesCustomMetadata]): Flat JSON blob to
            provide custom metadata about the catalog item variant. May not exceed 100kb. Example: {'Top Pick': True}.
        published (Union[Unset, bool]): Boolean value indicating whether the catalog item variant is published. Example:
            True.
        created (Union[Unset, datetime.datetime]): Date and time when the catalog item  variant was created, in ISO 8601
            format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
        updated (Union[Unset, datetime.datetime]): Date and time when the catalog item variant was last updated, in ISO
            8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm). Example: 2022-11-08T00:00:00.
    """

    external_id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    sku: Union[Unset, str] = UNSET
    inventory_policy: Union[Unset, CatalogVariantResponseObjectResourceAttributesInventoryPolicy] = UNSET
    inventory_quantity: Union[Unset, float] = UNSET
    price: Union[Unset, float] = UNSET
    url: Union[Unset, str] = UNSET
    image_full_url: Union[Unset, str] = UNSET
    image_thumbnail_url: Union[Unset, str] = UNSET
    images: Union[Unset, List[str]] = UNSET
    custom_metadata: Union[Unset, "CatalogVariantResponseObjectResourceAttributesCustomMetadata"] = UNSET
    published: Union[Unset, bool] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id

        title = self.title

        description = self.description

        sku = self.sku

        inventory_policy: Union[Unset, int] = UNSET
        if not isinstance(self.inventory_policy, Unset):
            inventory_policy = self.inventory_policy.value

        inventory_quantity = self.inventory_quantity

        price = self.price

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

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if sku is not UNSET:
            field_dict["sku"] = sku
        if inventory_policy is not UNSET:
            field_dict["inventory_policy"] = inventory_policy
        if inventory_quantity is not UNSET:
            field_dict["inventory_quantity"] = inventory_quantity
        if price is not UNSET:
            field_dict["price"] = price
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
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.catalog_variant_response_object_resource_attributes_custom_metadata import (
            CatalogVariantResponseObjectResourceAttributesCustomMetadata,
        )

        d = src_dict.copy()
        external_id = d.pop("external_id", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        sku = d.pop("sku", UNSET)

        _inventory_policy = d.pop("inventory_policy", UNSET)
        inventory_policy: Union[Unset, CatalogVariantResponseObjectResourceAttributesInventoryPolicy]
        if isinstance(_inventory_policy, Unset):
            inventory_policy = UNSET
        else:
            inventory_policy = CatalogVariantResponseObjectResourceAttributesInventoryPolicy(_inventory_policy)

        inventory_quantity = d.pop("inventory_quantity", UNSET)

        price = d.pop("price", UNSET)

        url = d.pop("url", UNSET)

        image_full_url = d.pop("image_full_url", UNSET)

        image_thumbnail_url = d.pop("image_thumbnail_url", UNSET)

        images = cast(List[str], d.pop("images", UNSET))

        _custom_metadata = d.pop("custom_metadata", UNSET)
        custom_metadata: Union[Unset, CatalogVariantResponseObjectResourceAttributesCustomMetadata]
        if isinstance(_custom_metadata, Unset):
            custom_metadata = UNSET
        else:
            custom_metadata = CatalogVariantResponseObjectResourceAttributesCustomMetadata.from_dict(_custom_metadata)

        published = d.pop("published", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        catalog_variant_response_object_resource_attributes = cls(
            external_id=external_id,
            title=title,
            description=description,
            sku=sku,
            inventory_policy=inventory_policy,
            inventory_quantity=inventory_quantity,
            price=price,
            url=url,
            image_full_url=image_full_url,
            image_thumbnail_url=image_thumbnail_url,
            images=images,
            custom_metadata=custom_metadata,
            published=published,
            created=created,
            updated=updated,
        )

        catalog_variant_response_object_resource_attributes.additional_properties = d
        return catalog_variant_response_object_resource_attributes

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
