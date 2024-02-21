from enum import Enum


class GetCreateVariantsJobFieldscatalogVariantItem(str, Enum):
    CREATED = "created"
    CUSTOM_METADATA = "custom_metadata"
    DESCRIPTION = "description"
    EXTERNAL_ID = "external_id"
    IMAGES = "images"
    IMAGE_FULL_URL = "image_full_url"
    IMAGE_THUMBNAIL_URL = "image_thumbnail_url"
    INVENTORY_POLICY = "inventory_policy"
    INVENTORY_QUANTITY = "inventory_quantity"
    PRICE = "price"
    PUBLISHED = "published"
    SKU = "sku"
    TITLE = "title"
    UPDATED = "updated"
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)
