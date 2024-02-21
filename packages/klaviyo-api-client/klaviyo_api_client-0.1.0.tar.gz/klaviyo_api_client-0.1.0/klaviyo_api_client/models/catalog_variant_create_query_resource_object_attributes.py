from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.catalog_variant_create_query_resource_object_attributes_integration_type import (
    CatalogVariantCreateQueryResourceObjectAttributesIntegrationType,
)
from ..models.catalog_variant_create_query_resource_object_attributes_inventory_policy import (
    CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.catalog_variant_create_query_resource_object_attributes_custom_metadata import (
        CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata,
    )


T = TypeVar("T", bound="CatalogVariantCreateQueryResourceObjectAttributes")


@_attrs_define
class CatalogVariantCreateQueryResourceObjectAttributes:
    """
    Attributes:
        external_id (str): The ID of the catalog item variant in an external system. Example: SAMPLE-DATA-
            ITEM-1-VARIANT-MEDIUM.
        title (str): The title of the catalog item variant. Example: Ocean Blue Shirt (Sample) Variant Medium.
        description (str): A description of the catalog item variant. Example: Ocean blue cotton shirt with a narrow
            collar and buttons down the front and long sleeves. Comfortable fit and titled kaleidoscope patterns..
        sku (str): The SKU of the catalog item variant. Example: OBS-MD.
        inventory_quantity (float): The quantity of the catalog item variant currently in stock. Example: 25.
        price (float): This field can be used to set the price on the catalog item variant, which is what gets displayed
            for the item variant when included in emails. For most price-update use cases, you will also want to update the
            `price` on any parent items using the [Update Catalog Item
            Endpoint](https://developers.klaviyo.com/en/reference/update_catalog_item). Example: 42.
        url (str): URL pointing to the location of the catalog item variant on your website. Example:
            https://via.placeholder.com/150.
        catalog_type (Union[Unset, str]): The type of catalog. Currently only "$default" is supported. Default:
            '$default'. Example: $default.
        integration_type (Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesIntegrationType]): The
            integration type. Currently only "$custom" is supported. Default:
            CatalogVariantCreateQueryResourceObjectAttributesIntegrationType.VALUE_0. Example: $custom.
        inventory_policy (Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy]): This field
            controls the visibility of this catalog item variant in product feeds/blocks. This field supports the following
            values:
            `1`: a product will not appear in dynamic product recommendation feeds and blocks if it is out of stock.
            `0` or `2`: a product can appear in dynamic product recommendation feeds and blocks regardless of inventory
            quantity. Default: CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy.VALUE_0. Example: 2.
        image_full_url (Union[Unset, str]): URL pointing to the location of a full image of the catalog item variant.
            Example: https://via.placeholder.com/300.
        image_thumbnail_url (Union[Unset, str]): URL pointing to the location of an image thumbnail of the catalog item
            variant. Example: https://via.placeholder.com/150.
        images (Union[Unset, List[str]]): List of URLs pointing to the locations of images of the catalog item variant.
            Example: ['https://via.placeholder.com/150'].
        custom_metadata (Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata]): Flat JSON blob
            to provide custom metadata about the catalog item variant. May not exceed 100kb. Example: {'Top Pick': True}.
        published (Union[Unset, bool]): Boolean value indicating whether the catalog item variant is published. Default:
            True. Example: True.
    """

    external_id: str
    title: str
    description: str
    sku: str
    inventory_quantity: float
    price: float
    url: str
    catalog_type: Union[Unset, str] = "$default"
    integration_type: Union[
        Unset, CatalogVariantCreateQueryResourceObjectAttributesIntegrationType
    ] = CatalogVariantCreateQueryResourceObjectAttributesIntegrationType.VALUE_0
    inventory_policy: Union[
        Unset, CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy
    ] = CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy.VALUE_0
    image_full_url: Union[Unset, str] = UNSET
    image_thumbnail_url: Union[Unset, str] = UNSET
    images: Union[Unset, List[str]] = UNSET
    custom_metadata: Union[Unset, "CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata"] = UNSET
    published: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id

        title = self.title

        description = self.description

        sku = self.sku

        inventory_quantity = self.inventory_quantity

        price = self.price

        url = self.url

        catalog_type = self.catalog_type

        integration_type: Union[Unset, str] = UNSET
        if not isinstance(self.integration_type, Unset):
            integration_type = self.integration_type.value

        inventory_policy: Union[Unset, int] = UNSET
        if not isinstance(self.inventory_policy, Unset):
            inventory_policy = self.inventory_policy.value

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
                "sku": sku,
                "inventory_quantity": inventory_quantity,
                "price": price,
                "url": url,
            }
        )
        if catalog_type is not UNSET:
            field_dict["catalog_type"] = catalog_type
        if integration_type is not UNSET:
            field_dict["integration_type"] = integration_type
        if inventory_policy is not UNSET:
            field_dict["inventory_policy"] = inventory_policy
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
        from ..models.catalog_variant_create_query_resource_object_attributes_custom_metadata import (
            CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata,
        )

        d = src_dict.copy()
        external_id = d.pop("external_id")

        title = d.pop("title")

        description = d.pop("description")

        sku = d.pop("sku")

        inventory_quantity = d.pop("inventory_quantity")

        price = d.pop("price")

        url = d.pop("url")

        catalog_type = d.pop("catalog_type", UNSET)

        _integration_type = d.pop("integration_type", UNSET)
        integration_type: Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesIntegrationType]
        if isinstance(_integration_type, Unset):
            integration_type = UNSET
        else:
            integration_type = CatalogVariantCreateQueryResourceObjectAttributesIntegrationType(_integration_type)

        _inventory_policy = d.pop("inventory_policy", UNSET)
        inventory_policy: Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy]
        if isinstance(_inventory_policy, Unset):
            inventory_policy = UNSET
        else:
            inventory_policy = CatalogVariantCreateQueryResourceObjectAttributesInventoryPolicy(_inventory_policy)

        image_full_url = d.pop("image_full_url", UNSET)

        image_thumbnail_url = d.pop("image_thumbnail_url", UNSET)

        images = cast(List[str], d.pop("images", UNSET))

        _custom_metadata = d.pop("custom_metadata", UNSET)
        custom_metadata: Union[Unset, CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata]
        if isinstance(_custom_metadata, Unset):
            custom_metadata = UNSET
        else:
            custom_metadata = CatalogVariantCreateQueryResourceObjectAttributesCustomMetadata.from_dict(
                _custom_metadata
            )

        published = d.pop("published", UNSET)

        catalog_variant_create_query_resource_object_attributes = cls(
            external_id=external_id,
            title=title,
            description=description,
            sku=sku,
            inventory_quantity=inventory_quantity,
            price=price,
            url=url,
            catalog_type=catalog_type,
            integration_type=integration_type,
            inventory_policy=inventory_policy,
            image_full_url=image_full_url,
            image_thumbnail_url=image_thumbnail_url,
            images=images,
            custom_metadata=custom_metadata,
            published=published,
        )

        catalog_variant_create_query_resource_object_attributes.additional_properties = d
        return catalog_variant_create_query_resource_object_attributes

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
