from enum import Enum


class GetCampaignsSort(str, Enum):
    CREATED_AT = "created_at"
    ID = "id"
    NAME = "name"
    SCHEDULED_AT = "scheduled_at"
    UPDATED_AT = "updated_at"
    VALUE_1 = "-created_at"
    VALUE_3 = "-id"
    VALUE_5 = "-name"
    VALUE_7 = "-scheduled_at"
    VALUE_9 = "-updated_at"

    def __str__(self) -> str:
        return str(self.value)
