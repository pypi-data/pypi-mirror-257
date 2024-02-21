from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_aggregate_query import MetricAggregateQuery
from ...models.post_metric_aggregate_response import PostMetricAggregateResponse
from ...types import Response


def _get_kwargs(
    *,
    body: MetricAggregateQuery,
    revision: str = "2024-02-15",
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["revision"] = revision

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/metric-aggregates/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PostMetricAggregateResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PostMetricAggregateResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = cast(Any, None)
        return response_402
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        response_405 = cast(Any, None)
        return response_405
    if response.status_code == HTTPStatus.NOT_ACCEPTABLE:
        response_406 = cast(Any, None)
        return response_406
    if response.status_code == HTTPStatus.PROXY_AUTHENTICATION_REQUIRED:
        response_407 = cast(Any, None)
        return response_407
    if response.status_code == HTTPStatus.REQUEST_TIMEOUT:
        response_408 = cast(Any, None)
        return response_408
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = cast(Any, None)
        return response_409
    if response.status_code == HTTPStatus.GONE:
        response_410 = cast(Any, None)
        return response_410
    if response.status_code == HTTPStatus.LENGTH_REQUIRED:
        response_411 = cast(Any, None)
        return response_411
    if response.status_code == HTTPStatus.PRECONDITION_FAILED:
        response_412 = cast(Any, None)
        return response_412
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = cast(Any, None)
        return response_413
    if response.status_code == HTTPStatus.REQUEST_URI_TOO_LONG:
        response_414 = cast(Any, None)
        return response_414
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        response_415 = cast(Any, None)
        return response_415
    if response.status_code == HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE:
        response_416 = cast(Any, None)
        return response_416
    if response.status_code == HTTPStatus.EXPECTATION_FAILED:
        response_417 = cast(Any, None)
        return response_417
    if response.status_code == HTTPStatus.IM_A_TEAPOT:
        response_418 = cast(Any, None)
        return response_418
    if response.status_code == HTTPStatus.MISDIRECTED_REQUEST:
        response_421 = cast(Any, None)
        return response_421
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = cast(Any, None)
        return response_422
    if response.status_code == HTTPStatus.LOCKED:
        response_423 = cast(Any, None)
        return response_423
    if response.status_code == HTTPStatus.FAILED_DEPENDENCY:
        response_424 = cast(Any, None)
        return response_424
    if response.status_code == HTTPStatus.TOO_EARLY:
        response_425 = cast(Any, None)
        return response_425
    if response.status_code == HTTPStatus.UPGRADE_REQUIRED:
        response_426 = cast(Any, None)
        return response_426
    if response.status_code == HTTPStatus.PRECONDITION_REQUIRED:
        response_428 = cast(Any, None)
        return response_428
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        response_429 = cast(Any, None)
        return response_429
    if response.status_code == HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE:
        response_431 = cast(Any, None)
        return response_431
    if response.status_code == HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS:
        response_451 = cast(Any, None)
        return response_451
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if response.status_code == HTTPStatus.BAD_GATEWAY:
        response_502 = cast(Any, None)
        return response_502
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = cast(Any, None)
        return response_503
    if response.status_code == HTTPStatus.GATEWAY_TIMEOUT:
        response_504 = cast(Any, None)
        return response_504
    if response.status_code == HTTPStatus.HTTP_VERSION_NOT_SUPPORTED:
        response_505 = cast(Any, None)
        return response_505
    if response.status_code == HTTPStatus.VARIANT_ALSO_NEGOTIATES:
        response_506 = cast(Any, None)
        return response_506
    if response.status_code == HTTPStatus.INSUFFICIENT_STORAGE:
        response_507 = cast(Any, None)
        return response_507
    if response.status_code == HTTPStatus.LOOP_DETECTED:
        response_508 = cast(Any, None)
        return response_508
    if response.status_code == HTTPStatus.NOT_EXTENDED:
        response_510 = cast(Any, None)
        return response_510
    if response.status_code == HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED:
        response_511 = cast(Any, None)
        return response_511
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PostMetricAggregateResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MetricAggregateQuery,
    revision: str = "2024-02-15",
) -> Response[Union[Any, PostMetricAggregateResponse]]:
    r"""Query Metric Aggregates

     Query and aggregate event data associated with a metric, including native Klaviyo metrics,
    integration-specific metrics, and custom events. Queries must be passed in the JSON body of your
    `POST` request.

    Results can be filtered and grouped by time, event, or profile dimensions.

    To learn more about how to use this endpoint, check out our new [Using the Query Metric Aggregates
    Endpoint guide](https://developers.klaviyo.com/en/docs/using-the-query-metric-aggregates-endpoint).

    **Request body parameters** (nested under `attributes`):

    * `return_fields`: request specific fields using [sparse
    fieldsets](https://developers.klaviyo.com/en/reference/api_overview#sparse-fieldsets)
    * `sort`: sort results by a specified field, such as `\"-timestamp\"`
    * `page_cursor`: results can be paginated with [cursor-based
    pagination](https://developers.klaviyo.com/en/reference/api_overview#pagination)
    * `page_size`: limit the number of returned results per page
    * `by`: optional attributes used to group by the aggregation function
        * When using `by` attributes, an empty `dimensions` response is expected when the counts for the
    events do not have the associated dimension requested by the set `by` attribute. For example, a
    query including `\"by\": [\"$flow\"]` will return an empty dimensions response for counts of metrics
    not associated with a `$flow`
    * `measurement`: the measurement key supports the following values:
        * `\"sum_value\"`: perform a summation of the `_Event Value_`, optionally partitioned over any
    dimension provided in the `by` field
        * `\"count\"`: counts the number of events associated to a metric, optionally partitioned over
    any dimension provided in the `by` field
        * `\"unique\"` counts the number of unique customers associated to a metric, optionally
    partitioned over any dimension provided in the `by` field
    * `interval`: aggregation interval, such as `\"hour\"`,`\"day\"`,`\"week\"`, and `\"month\"`
    * `metric_id`: the metric ID used in the aggregation
    * `filter`: list of filters for specific fields, must include time range using ISO 8601 format
    (`\"YYYY-MM-DDTHH:MM:SS.mmmmmm\"`)
        * The time range can be filtered by providing a `greater-or-equal` filter on the datetime field,
    such as `\"greater-or-equal(datetime,2021-07-01T00:00:00)\"` and a `less-than` filter on the same
    datetime field, such as `\"less-than(datetime,2022-07-01T00:00:00)\"`
        * The time range may span a maximum of one year. Time range dates may be set to a maximum of 5
    years prior to the current date
        * Filter the list of supported aggregate dimensions using the common filter syntax, such as
    `\"equals(URL,\\"https://www.klaviyo.com/\\")\"`
    * `timezone`: the timezone used when processing the query. Case sensitive. This field is validated
    against a list of common timezones from the [IANA Time Zone Database](https://www.iana.org/time-
    zones)
        * While the payload accepts a timezone, the response datetimes returned will be in UTC.

    For a comprehensive list of native Klaviyo metrics and their associated attributes for grouping and
    filtering, please refer to the [metrics attributes
    guide](https://developers.klaviyo.com/en/docs/supported_metrics_and_attributes).<br><br>*Rate
    limits*:<br>Burst: `3/s`<br>Steady: `60/m`

    **Scopes:**
    `metrics:read`

    Args:
        revision (str):  Default: '2024-02-15'.
        body (MetricAggregateQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostMetricAggregateResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        revision=revision,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MetricAggregateQuery,
    revision: str = "2024-02-15",
) -> Optional[Union[Any, PostMetricAggregateResponse]]:
    r"""Query Metric Aggregates

     Query and aggregate event data associated with a metric, including native Klaviyo metrics,
    integration-specific metrics, and custom events. Queries must be passed in the JSON body of your
    `POST` request.

    Results can be filtered and grouped by time, event, or profile dimensions.

    To learn more about how to use this endpoint, check out our new [Using the Query Metric Aggregates
    Endpoint guide](https://developers.klaviyo.com/en/docs/using-the-query-metric-aggregates-endpoint).

    **Request body parameters** (nested under `attributes`):

    * `return_fields`: request specific fields using [sparse
    fieldsets](https://developers.klaviyo.com/en/reference/api_overview#sparse-fieldsets)
    * `sort`: sort results by a specified field, such as `\"-timestamp\"`
    * `page_cursor`: results can be paginated with [cursor-based
    pagination](https://developers.klaviyo.com/en/reference/api_overview#pagination)
    * `page_size`: limit the number of returned results per page
    * `by`: optional attributes used to group by the aggregation function
        * When using `by` attributes, an empty `dimensions` response is expected when the counts for the
    events do not have the associated dimension requested by the set `by` attribute. For example, a
    query including `\"by\": [\"$flow\"]` will return an empty dimensions response for counts of metrics
    not associated with a `$flow`
    * `measurement`: the measurement key supports the following values:
        * `\"sum_value\"`: perform a summation of the `_Event Value_`, optionally partitioned over any
    dimension provided in the `by` field
        * `\"count\"`: counts the number of events associated to a metric, optionally partitioned over
    any dimension provided in the `by` field
        * `\"unique\"` counts the number of unique customers associated to a metric, optionally
    partitioned over any dimension provided in the `by` field
    * `interval`: aggregation interval, such as `\"hour\"`,`\"day\"`,`\"week\"`, and `\"month\"`
    * `metric_id`: the metric ID used in the aggregation
    * `filter`: list of filters for specific fields, must include time range using ISO 8601 format
    (`\"YYYY-MM-DDTHH:MM:SS.mmmmmm\"`)
        * The time range can be filtered by providing a `greater-or-equal` filter on the datetime field,
    such as `\"greater-or-equal(datetime,2021-07-01T00:00:00)\"` and a `less-than` filter on the same
    datetime field, such as `\"less-than(datetime,2022-07-01T00:00:00)\"`
        * The time range may span a maximum of one year. Time range dates may be set to a maximum of 5
    years prior to the current date
        * Filter the list of supported aggregate dimensions using the common filter syntax, such as
    `\"equals(URL,\\"https://www.klaviyo.com/\\")\"`
    * `timezone`: the timezone used when processing the query. Case sensitive. This field is validated
    against a list of common timezones from the [IANA Time Zone Database](https://www.iana.org/time-
    zones)
        * While the payload accepts a timezone, the response datetimes returned will be in UTC.

    For a comprehensive list of native Klaviyo metrics and their associated attributes for grouping and
    filtering, please refer to the [metrics attributes
    guide](https://developers.klaviyo.com/en/docs/supported_metrics_and_attributes).<br><br>*Rate
    limits*:<br>Burst: `3/s`<br>Steady: `60/m`

    **Scopes:**
    `metrics:read`

    Args:
        revision (str):  Default: '2024-02-15'.
        body (MetricAggregateQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostMetricAggregateResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        revision=revision,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MetricAggregateQuery,
    revision: str = "2024-02-15",
) -> Response[Union[Any, PostMetricAggregateResponse]]:
    r"""Query Metric Aggregates

     Query and aggregate event data associated with a metric, including native Klaviyo metrics,
    integration-specific metrics, and custom events. Queries must be passed in the JSON body of your
    `POST` request.

    Results can be filtered and grouped by time, event, or profile dimensions.

    To learn more about how to use this endpoint, check out our new [Using the Query Metric Aggregates
    Endpoint guide](https://developers.klaviyo.com/en/docs/using-the-query-metric-aggregates-endpoint).

    **Request body parameters** (nested under `attributes`):

    * `return_fields`: request specific fields using [sparse
    fieldsets](https://developers.klaviyo.com/en/reference/api_overview#sparse-fieldsets)
    * `sort`: sort results by a specified field, such as `\"-timestamp\"`
    * `page_cursor`: results can be paginated with [cursor-based
    pagination](https://developers.klaviyo.com/en/reference/api_overview#pagination)
    * `page_size`: limit the number of returned results per page
    * `by`: optional attributes used to group by the aggregation function
        * When using `by` attributes, an empty `dimensions` response is expected when the counts for the
    events do not have the associated dimension requested by the set `by` attribute. For example, a
    query including `\"by\": [\"$flow\"]` will return an empty dimensions response for counts of metrics
    not associated with a `$flow`
    * `measurement`: the measurement key supports the following values:
        * `\"sum_value\"`: perform a summation of the `_Event Value_`, optionally partitioned over any
    dimension provided in the `by` field
        * `\"count\"`: counts the number of events associated to a metric, optionally partitioned over
    any dimension provided in the `by` field
        * `\"unique\"` counts the number of unique customers associated to a metric, optionally
    partitioned over any dimension provided in the `by` field
    * `interval`: aggregation interval, such as `\"hour\"`,`\"day\"`,`\"week\"`, and `\"month\"`
    * `metric_id`: the metric ID used in the aggregation
    * `filter`: list of filters for specific fields, must include time range using ISO 8601 format
    (`\"YYYY-MM-DDTHH:MM:SS.mmmmmm\"`)
        * The time range can be filtered by providing a `greater-or-equal` filter on the datetime field,
    such as `\"greater-or-equal(datetime,2021-07-01T00:00:00)\"` and a `less-than` filter on the same
    datetime field, such as `\"less-than(datetime,2022-07-01T00:00:00)\"`
        * The time range may span a maximum of one year. Time range dates may be set to a maximum of 5
    years prior to the current date
        * Filter the list of supported aggregate dimensions using the common filter syntax, such as
    `\"equals(URL,\\"https://www.klaviyo.com/\\")\"`
    * `timezone`: the timezone used when processing the query. Case sensitive. This field is validated
    against a list of common timezones from the [IANA Time Zone Database](https://www.iana.org/time-
    zones)
        * While the payload accepts a timezone, the response datetimes returned will be in UTC.

    For a comprehensive list of native Klaviyo metrics and their associated attributes for grouping and
    filtering, please refer to the [metrics attributes
    guide](https://developers.klaviyo.com/en/docs/supported_metrics_and_attributes).<br><br>*Rate
    limits*:<br>Burst: `3/s`<br>Steady: `60/m`

    **Scopes:**
    `metrics:read`

    Args:
        revision (str):  Default: '2024-02-15'.
        body (MetricAggregateQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PostMetricAggregateResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
        revision=revision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: MetricAggregateQuery,
    revision: str = "2024-02-15",
) -> Optional[Union[Any, PostMetricAggregateResponse]]:
    r"""Query Metric Aggregates

     Query and aggregate event data associated with a metric, including native Klaviyo metrics,
    integration-specific metrics, and custom events. Queries must be passed in the JSON body of your
    `POST` request.

    Results can be filtered and grouped by time, event, or profile dimensions.

    To learn more about how to use this endpoint, check out our new [Using the Query Metric Aggregates
    Endpoint guide](https://developers.klaviyo.com/en/docs/using-the-query-metric-aggregates-endpoint).

    **Request body parameters** (nested under `attributes`):

    * `return_fields`: request specific fields using [sparse
    fieldsets](https://developers.klaviyo.com/en/reference/api_overview#sparse-fieldsets)
    * `sort`: sort results by a specified field, such as `\"-timestamp\"`
    * `page_cursor`: results can be paginated with [cursor-based
    pagination](https://developers.klaviyo.com/en/reference/api_overview#pagination)
    * `page_size`: limit the number of returned results per page
    * `by`: optional attributes used to group by the aggregation function
        * When using `by` attributes, an empty `dimensions` response is expected when the counts for the
    events do not have the associated dimension requested by the set `by` attribute. For example, a
    query including `\"by\": [\"$flow\"]` will return an empty dimensions response for counts of metrics
    not associated with a `$flow`
    * `measurement`: the measurement key supports the following values:
        * `\"sum_value\"`: perform a summation of the `_Event Value_`, optionally partitioned over any
    dimension provided in the `by` field
        * `\"count\"`: counts the number of events associated to a metric, optionally partitioned over
    any dimension provided in the `by` field
        * `\"unique\"` counts the number of unique customers associated to a metric, optionally
    partitioned over any dimension provided in the `by` field
    * `interval`: aggregation interval, such as `\"hour\"`,`\"day\"`,`\"week\"`, and `\"month\"`
    * `metric_id`: the metric ID used in the aggregation
    * `filter`: list of filters for specific fields, must include time range using ISO 8601 format
    (`\"YYYY-MM-DDTHH:MM:SS.mmmmmm\"`)
        * The time range can be filtered by providing a `greater-or-equal` filter on the datetime field,
    such as `\"greater-or-equal(datetime,2021-07-01T00:00:00)\"` and a `less-than` filter on the same
    datetime field, such as `\"less-than(datetime,2022-07-01T00:00:00)\"`
        * The time range may span a maximum of one year. Time range dates may be set to a maximum of 5
    years prior to the current date
        * Filter the list of supported aggregate dimensions using the common filter syntax, such as
    `\"equals(URL,\\"https://www.klaviyo.com/\\")\"`
    * `timezone`: the timezone used when processing the query. Case sensitive. This field is validated
    against a list of common timezones from the [IANA Time Zone Database](https://www.iana.org/time-
    zones)
        * While the payload accepts a timezone, the response datetimes returned will be in UTC.

    For a comprehensive list of native Klaviyo metrics and their associated attributes for grouping and
    filtering, please refer to the [metrics attributes
    guide](https://developers.klaviyo.com/en/docs/supported_metrics_and_attributes).<br><br>*Rate
    limits*:<br>Burst: `3/s`<br>Steady: `60/m`

    **Scopes:**
    `metrics:read`

    Args:
        revision (str):  Default: '2024-02-15'.
        body (MetricAggregateQuery):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PostMetricAggregateResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            revision=revision,
        )
    ).parsed
