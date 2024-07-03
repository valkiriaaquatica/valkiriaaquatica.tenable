import urllib.parse
from typing import Any
from typing import Callable
from typing import Dict
from typing import List


def build_query_parameters(**kwargs: Any) -> Dict[str, str]:
    query_params = {}
    param_map = {
        "limit": "limit",
        "offset": "offset",
        "sort": "sort",
        "include_deleted": "includeDeleted",
        "date_range": "date_range",
        "filter_search_type": "filter.search_type",
        "filters": "filters",
        "wildcard_text": "w",
        "wildcard_fields": "wf",
        "filter_type": "ft",
        "all_fields": "all_fields",
        "last_updated": "last_updated",
        "size": "size",
        "page": "page",
        "folder_id": "folder_id",
        "last_modification_date": "last_modification_date",
        "history_id": "history_id",
        "description": "description",
        "assets_ttl_days": "assets_ttl_days",
    }

    for key, value in kwargs.items():
        if value is not None:
            mapped_key = param_map.get(key, key)
            if isinstance(value, list):
                query_params[mapped_key] = ",".join(value)
            else:
                query_params[mapped_key] = str(value).lower() if isinstance(value, bool) else str(value)

    return query_params


def handle_multiple_filters(query_params: Dict[str, str], filters: List[Dict[str, str]]) -> Dict[str, str]:
    if filters:
        for idx, filter_ in enumerate(filters):
            prefix = f"filter.{idx}"
            query_params[f"{prefix}.filter"] = urllib.parse.quote_plus(filter_["type"])
            query_params[f"{prefix}.quality"] = urllib.parse.quote_plus(filter_["operator"])
            query_params[f"{prefix}.value"] = urllib.parse.quote_plus(filter_["value"])
    return query_params


def handle_special_filter(query_params: Dict[str, str], filters: List[Dict[str, str]]) -> Dict[str, str]:
    if filters:
        query_params["f"] = "&".join([f"{f['type']}:{f['operator']}:{f['value']}" for f in filters])
    return query_params


def add_custom_filters(
    query_params: Dict[str, str], filters: List[Dict[str, str]], filter_handler: Callable
) -> Dict[str, str]:
    return filter_handler(query_params, filters)


def build_payload(module, keys: List[str]) -> Dict[str, Any]:
    payload = {}

    def recurse_build(payload: Dict[str, Any], params: Dict[str, Any], keys: List[str]) -> None:
        for key in keys:
            value = params.get(key)
            if isinstance(value, dict):
                sub_payload = {}
                recurse_build(sub_payload, value, value.keys())
                if sub_payload:
                    payload[key] = sub_payload
            elif value is not None:
                payload[key] = value

    recurse_build(payload, module.params, keys)
    return payload


def build_complex_payload(params: Dict[str, Any]) -> Dict[str, Any]:
    payload = {"uuid": params["uuid"], "settings": {}}
    for key, value in params["settings"].items():
        if value is not None:
            if isinstance(value, dict):
                payload["settings"][key] = {k: v for k, v in value.items() if v is not None}
            else:
                payload["settings"][key] = value

    if "credentials" in params and params["credentials"]:
        payload["credentials"] = {}
        for cred_key, cred_value in params["credentials"].items():
            payload["credentials"][cred_key] = {k: v for k, v in cred_value.items() if v is not None}

    if "plugin_configurations" in params and params["plugin_configurations"]:
        payload["plugins"] = {}
        for plugin_config in params["plugin_configurations"]:
            family_name = plugin_config.get("plugin_family_name")
            plugins = plugin_config.get("plugins", [])
            if family_name and plugins:
                if family_name not in payload["plugins"]:
                    payload["plugins"][family_name] = {"individual": {}}
                for plugin in plugins:
                    plugin_id = plugin.get("plugin_id")
                    status = plugin.get("status")
                    if plugin_id and status:
                        payload["plugins"][family_name]["individual"][plugin_id] = status

    return payload


def build_tag_values_payload(params: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "category_name": params.get("category_name"),
        "category_uuid": params.get("category_uuid"),
        "value": params.get("value"),
    }

    if params.get("category_description"):
        payload["category_description"] = params["category_description"]
    if params.get("description"):
        payload["description"] = params["description"]
    if params.get("access_control"):
        payload["access_control"] = {k: v for k, v in params["access_control"].items() if v is not None}
    if params.get("filters"):
        payload["filters"] = {k: v for k, v in params["filters"].items() if v is not None}

    return payload
