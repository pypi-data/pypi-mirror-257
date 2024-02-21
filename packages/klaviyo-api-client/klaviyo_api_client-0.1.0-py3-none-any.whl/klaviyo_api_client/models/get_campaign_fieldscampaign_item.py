from enum import Enum


class GetCampaignFieldscampaignItem(str, Enum):
    ARCHIVED = "archived"
    AUDIENCES = "audiences"
    AUDIENCES_EXCLUDED = "audiences.excluded"
    AUDIENCES_INCLUDED = "audiences.included"
    CREATED_AT = "created_at"
    NAME = "name"
    SCHEDULED_AT = "scheduled_at"
    SEND_OPTIONS = "send_options"
    SEND_STRATEGY = "send_strategy"
    SEND_STRATEGY_METHOD = "send_strategy.method"
    SEND_STRATEGY_OPTIONS_STATIC = "send_strategy.options_static"
    SEND_STRATEGY_OPTIONS_STATIC_DATETIME = "send_strategy.options_static.datetime"
    SEND_STRATEGY_OPTIONS_STATIC_IS_LOCAL = "send_strategy.options_static.is_local"
    SEND_STRATEGY_OPTIONS_STATIC_SEND_PAST_RECIPIENTS_IMMEDIATELY = (
        "send_strategy.options_static.send_past_recipients_immediately"
    )
    SEND_STRATEGY_OPTIONS_STO = "send_strategy.options_sto"
    SEND_STRATEGY_OPTIONS_STO_DATE = "send_strategy.options_sto.date"
    SEND_STRATEGY_OPTIONS_THROTTLED = "send_strategy.options_throttled"
    SEND_STRATEGY_OPTIONS_THROTTLED_DATETIME = "send_strategy.options_throttled.datetime"
    SEND_STRATEGY_OPTIONS_THROTTLED_THROTTLE_PERCENTAGE = "send_strategy.options_throttled.throttle_percentage"
    SEND_TIME = "send_time"
    STATUS = "status"
    TRACKING_OPTIONS = "tracking_options"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
