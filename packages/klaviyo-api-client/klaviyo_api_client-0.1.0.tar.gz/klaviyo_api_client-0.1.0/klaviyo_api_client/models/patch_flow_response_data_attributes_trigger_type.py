from enum import Enum


class PatchFlowResponseDataAttributesTriggerType(str, Enum):
    ADDED_TO_LIST = "Added to List"
    DATE_BASED = "Date Based"
    LOW_INVENTORY = "Low Inventory"
    METRIC = "Metric"
    PRICE_DROP = "Price Drop"
    UNCONFIGURED = "Unconfigured"

    def __str__(self) -> str:
        return str(self.value)
