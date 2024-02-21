from enum import Enum


class GetFlowFieldsflowActionItem(str, Enum):
    ACTION_TYPE = "action_type"
    CREATED = "created"
    RENDER_OPTIONS = "render_options"
    RENDER_OPTIONS_ADD_INFO_LINK = "render_options.add_info_link"
    RENDER_OPTIONS_ADD_OPT_OUT_LANGUAGE = "render_options.add_opt_out_language"
    RENDER_OPTIONS_ADD_ORG_PREFIX = "render_options.add_org_prefix"
    RENDER_OPTIONS_SHORTEN_LINKS = "render_options.shorten_links"
    SEND_OPTIONS = "send_options"
    SEND_OPTIONS_IS_TRANSACTIONAL = "send_options.is_transactional"
    SEND_OPTIONS_USE_SMART_SENDING = "send_options.use_smart_sending"
    SETTINGS = "settings"
    STATUS = "status"
    TRACKING_OPTIONS = "tracking_options"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
