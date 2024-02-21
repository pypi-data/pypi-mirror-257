from enum import Enum


class GetImagesFieldsimageItem(str, Enum):
    FORMAT = "format"
    HIDDEN = "hidden"
    IMAGE_URL = "image_url"
    NAME = "name"
    SIZE = "size"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
