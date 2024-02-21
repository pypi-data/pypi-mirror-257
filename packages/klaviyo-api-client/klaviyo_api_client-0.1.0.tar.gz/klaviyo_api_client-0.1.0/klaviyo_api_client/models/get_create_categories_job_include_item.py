from enum import Enum


class GetCreateCategoriesJobIncludeItem(str, Enum):
    CATEGORIES = "categories"

    def __str__(self) -> str:
        return str(self.value)
