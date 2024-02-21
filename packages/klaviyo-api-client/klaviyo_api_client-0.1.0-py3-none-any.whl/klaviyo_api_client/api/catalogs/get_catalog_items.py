from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_catalog_item_response_collection_compound_document import (
    GetCatalogItemResponseCollectionCompoundDocument,
)
from ...models.get_catalog_items_fieldscatalog_item_item import GetCatalogItemsFieldscatalogItemItem
from ...models.get_catalog_items_fieldscatalog_variant_item import GetCatalogItemsFieldscatalogVariantItem
from ...models.get_catalog_items_include_item import GetCatalogItemsIncludeItem
from ...models.get_catalog_items_sort import GetCatalogItemsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    fieldscatalog_item: Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]] = UNSET,
    fieldscatalog_variant: Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    include: Union[Unset, List[GetCatalogItemsIncludeItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, GetCatalogItemsSort] = UNSET,
    revision: str = "2024-02-15",
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}
    headers["revision"] = revision

    params: Dict[str, Any] = {}

    json_fieldscatalog_item: Union[Unset, List[str]] = UNSET
    if not isinstance(fieldscatalog_item, Unset):
        json_fieldscatalog_item = []
        for fieldscatalog_item_item_data in fieldscatalog_item:
            fieldscatalog_item_item = fieldscatalog_item_item_data.value
            json_fieldscatalog_item.append(fieldscatalog_item_item)

    params["fields[catalog-item]"] = json_fieldscatalog_item

    json_fieldscatalog_variant: Union[Unset, List[str]] = UNSET
    if not isinstance(fieldscatalog_variant, Unset):
        json_fieldscatalog_variant = []
        for fieldscatalog_variant_item_data in fieldscatalog_variant:
            fieldscatalog_variant_item = fieldscatalog_variant_item_data.value
            json_fieldscatalog_variant.append(fieldscatalog_variant_item)

    params["fields[catalog-variant]"] = json_fieldscatalog_variant

    params["filter"] = filter_

    json_include: Union[Unset, List[str]] = UNSET
    if not isinstance(include, Unset):
        json_include = []
        for include_item_data in include:
            include_item = include_item_data.value
            json_include.append(include_item)

    params["include"] = json_include

    params["page[cursor]"] = pagecursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/catalog-items/",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetCatalogItemResponseCollectionCompoundDocument.from_dict(response.json())

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
) -> Response[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    fieldscatalog_item: Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]] = UNSET,
    fieldscatalog_variant: Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    include: Union[Unset, List[GetCatalogItemsIncludeItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, GetCatalogItemsSort] = UNSET,
    revision: str = "2024-02-15",
) -> Response[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    """Get Catalog Items

     Get all catalog items in an account.

    Catalog items can be sorted by the following fields, in ascending and descending order:
    `created`

    Currently, the only supported integration type is `$custom`, and the only supported catalog type is
    `$default`.

    Returns a maximum of 100 items per request.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady:
    `3500/m`

    **Scopes:**
    `catalogs:read`

    Args:
        fieldscatalog_item (Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]]):
        fieldscatalog_variant (Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]]):
        filter_ (Union[Unset, str]):
        include (Union[Unset, List[GetCatalogItemsIncludeItem]]):
        pagecursor (Union[Unset, str]):
        sort (Union[Unset, GetCatalogItemsSort]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]
    """

    kwargs = _get_kwargs(
        fieldscatalog_item=fieldscatalog_item,
        fieldscatalog_variant=fieldscatalog_variant,
        filter_=filter_,
        include=include,
        pagecursor=pagecursor,
        sort=sort,
        revision=revision,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    fieldscatalog_item: Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]] = UNSET,
    fieldscatalog_variant: Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    include: Union[Unset, List[GetCatalogItemsIncludeItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, GetCatalogItemsSort] = UNSET,
    revision: str = "2024-02-15",
) -> Optional[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    """Get Catalog Items

     Get all catalog items in an account.

    Catalog items can be sorted by the following fields, in ascending and descending order:
    `created`

    Currently, the only supported integration type is `$custom`, and the only supported catalog type is
    `$default`.

    Returns a maximum of 100 items per request.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady:
    `3500/m`

    **Scopes:**
    `catalogs:read`

    Args:
        fieldscatalog_item (Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]]):
        fieldscatalog_variant (Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]]):
        filter_ (Union[Unset, str]):
        include (Union[Unset, List[GetCatalogItemsIncludeItem]]):
        pagecursor (Union[Unset, str]):
        sort (Union[Unset, GetCatalogItemsSort]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetCatalogItemResponseCollectionCompoundDocument]
    """

    return sync_detailed(
        client=client,
        fieldscatalog_item=fieldscatalog_item,
        fieldscatalog_variant=fieldscatalog_variant,
        filter_=filter_,
        include=include,
        pagecursor=pagecursor,
        sort=sort,
        revision=revision,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    fieldscatalog_item: Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]] = UNSET,
    fieldscatalog_variant: Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    include: Union[Unset, List[GetCatalogItemsIncludeItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, GetCatalogItemsSort] = UNSET,
    revision: str = "2024-02-15",
) -> Response[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    """Get Catalog Items

     Get all catalog items in an account.

    Catalog items can be sorted by the following fields, in ascending and descending order:
    `created`

    Currently, the only supported integration type is `$custom`, and the only supported catalog type is
    `$default`.

    Returns a maximum of 100 items per request.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady:
    `3500/m`

    **Scopes:**
    `catalogs:read`

    Args:
        fieldscatalog_item (Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]]):
        fieldscatalog_variant (Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]]):
        filter_ (Union[Unset, str]):
        include (Union[Unset, List[GetCatalogItemsIncludeItem]]):
        pagecursor (Union[Unset, str]):
        sort (Union[Unset, GetCatalogItemsSort]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]
    """

    kwargs = _get_kwargs(
        fieldscatalog_item=fieldscatalog_item,
        fieldscatalog_variant=fieldscatalog_variant,
        filter_=filter_,
        include=include,
        pagecursor=pagecursor,
        sort=sort,
        revision=revision,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    fieldscatalog_item: Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]] = UNSET,
    fieldscatalog_variant: Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    include: Union[Unset, List[GetCatalogItemsIncludeItem]] = UNSET,
    pagecursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, GetCatalogItemsSort] = UNSET,
    revision: str = "2024-02-15",
) -> Optional[Union[Any, GetCatalogItemResponseCollectionCompoundDocument]]:
    """Get Catalog Items

     Get all catalog items in an account.

    Catalog items can be sorted by the following fields, in ascending and descending order:
    `created`

    Currently, the only supported integration type is `$custom`, and the only supported catalog type is
    `$default`.

    Returns a maximum of 100 items per request.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady:
    `3500/m`

    **Scopes:**
    `catalogs:read`

    Args:
        fieldscatalog_item (Union[Unset, List[GetCatalogItemsFieldscatalogItemItem]]):
        fieldscatalog_variant (Union[Unset, List[GetCatalogItemsFieldscatalogVariantItem]]):
        filter_ (Union[Unset, str]):
        include (Union[Unset, List[GetCatalogItemsIncludeItem]]):
        pagecursor (Union[Unset, str]):
        sort (Union[Unset, GetCatalogItemsSort]):
        revision (str):  Default: '2024-02-15'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GetCatalogItemResponseCollectionCompoundDocument]
    """

    return (
        await asyncio_detailed(
            client=client,
            fieldscatalog_item=fieldscatalog_item,
            fieldscatalog_variant=fieldscatalog_variant,
            filter_=filter_,
            include=include,
            pagecursor=pagecursor,
            sort=sort,
            revision=revision,
        )
    ).parsed
