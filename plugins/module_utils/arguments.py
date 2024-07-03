# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback

ARG_SPECS = {
    "access_key": {
        "type": "str",
        "required": False,
        "no_log": True,
        "fallback": (env_fallback, ["TENABLE_ACCESS_KEY"]),
    },
    "secret_key": {
        "type": "str",
        "required": False,
        "no_log": True,
        "fallback": (env_fallback, ["TENABLE_SECRET_KEY"]),
    },
    "type": {"type": "str", "required": True, "choices": ["scan", "policy", "remediation"]},
    "value_uuid": {"type": "str", "required": True},
    "value": {"type": "str", "required": False},
    "user_id": {"type": "str", "required": True},
    "history_id": {"type": "str", "required": False},
    "plugin_id": {"type": "str", "required": True},
    "scanner_id": {"type": "int", "required": True},
    "wizard_uuid": {"type": "str", "required": True},
    "name": {"type": "str", "required": True},
    "credential_uuid": {"required": True, "type": "str"},
    "scan_id": {"type": "str", "required": True},
    "exclusion_id": {"type": "int", "required": True},
    "asset_uuid": {"type": "str", "required": True},
    "attribute_id": {"type": "str", "required": True},
    "folder_id": {"type": "int", "required": False},
    "last_modification_date": {"type": "int", "required": False},
    "group_id": {"type": "str", "required": True},
    "agent_id": {"type": "str", "required": True},
    "limit": {"type": "int", "required": False},
    "offset": {"type": "int", "required": False},
    "filters": {"type": "list", "elements": "dict", "required": False},
    "sort": {"type": "str", "required": False},
    "date_range": {"type": "int", "required": False},
    "filter_search_type": {"type": "str", "choices": ["and", "or"], "required": False},
    "filter_type": {"type": "str", "choices": ["and", "or"], "required": False},
    "wildcard": {"type": "str", "required": False},
    "wildcard_text": {"type": "str", "required": False},
    "wildcard_fields": {"type": "list", "elements": "str", "required": False},
    "last_updated": {"type": "str", "required": False},
    "page": {"type": "int", "required": False},
    "size": {"type": "int", "required": False},
    "assets_ttl_days": {"type": "int", "required": False},
    "schedule": {
        "type": "dict",
        "required": False,
        "options": {
            "enabled": {"type": "bool"},
            "starttime": {"type": "str", "required": False},
            "endtime": {"type": "str", "required": False},
            "timezone": {"type": "str", "required": False},
            "rrules": {
                "type": "dict",
                "required": False,
                "options": {
                    "freq": {"type": "str", "required": False},
                    "interval": {"type": "int", "required": False},
                    "byweekday": {"type": "str", "required": False},
                    "bymonthday": {"type": "int", "required": False},
                },
            },
        },
    },
    "criteria": {
        "required": False,
        "type": "dict",
        "options": {
            "all_agents": {"required": False, "type": "bool"},
            "wildcard": {"required": False, "type": "str"},
            "filters": {"required": False, "type": "list", "elements": "str"},
            "filter_type": {"required": False, "type": "str", "choices": ["and", "or"]},
            "hardcoded_filters": {"required": False, "type": "list", "elements": "str"},
        },
    },
    "items": {"required": False, "type": "list", "elements": "str"},
    "not_items": {"required": False, "type": "list", "elements": "str"},
    "directive": {
        "required": True,
        "type": "dict",
        "options": {
            "type": {"required": True, "type": "str", "choices": ["restart", "settings"]},
            "options": {
                "required": True,
                "type": "dict",
                "options": {
                    "hard": {"required": False, "type": "bool"},
                    "idle": {"required": False, "type": "bool"},
                    "settings": {
                        "required": False,
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "setting": {"required": True, "type": "str"},
                            "value": {"required": True, "type": "str"},
                        },
                    },
                },
            },
        },
    },
    "network_id": {"type": "str", "required": False},
    "network_uuid": {"type": "str", "required": True},
    "alt_targets": {"type": "list", "elements": "str", "required": False},
    "rollover": {"type": "bool", "required": False},
    "all_fields": {"type": "str", "required": False, "choices": ["default", "full"]},
    "age": {"type": "int", "required": False},
    "authenticated": {"type": "bool", "required": False},
    "exploitable": {"type": "bool", "required": False},
    "resolvable": {"type": "bool", "required": False},
    "severity": {"type": "string", "choices": ["critical", "high", "medium", "low", "info"], "required": False},
    "uuid": {"type": "str", "required": True},
    "settings": {
        "type": "dict",
        "required": True,
        "options": {
            "name": {"type": "str", "required": True},
            "description": {"type": "str", "required": False},
            "policy_id": {"type": "int", "required": False},
            "folder_id": {"type": "int", "required": False},
            "scanner_id": {"type": "str", "required": False},
            "target_network_uuid": {"type": "str", "required": False},
            "enabled": {"type": "bool", "required": False},
            "launch": {
                "type": "str",
                "choices": ["ON_DEMAND", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
                "required": False,
            },
            "scan_time_window": {"type": "int", "required": False},
            "starttime": {"type": "str", "required": False},
            "rrules": {"type": "str", "required": False},
            "timezone": {"type": "str", "required": False},
            "text_targets": {"type": "str", "required": False},
            "target_groups": {"type": "list", "elements": "int", "required": False},
            "file_targets": {"type": "str", "required": False},
            "tag_targets": {"type": "list", "elements": "str", "required": False},
            "host_tagging": {"type": "str", "required": False},
            "agent_group_id": {"type": "list", "elements": "str", "required": False},
            "agent_scan_launch_type": {"type": "str", "required": False, "choices": ["scheduled", "triggered"]},
            "triggers": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "type": {"type": "str", "required": False, "choices": ["periodic", "file-exists"]},
                    "options": {
                        "type": "dict",
                        "options": {
                            "periodic_hourly_interval": {
                                "type": "int",
                                "required": False,
                            },
                            "filename": {"type": "str", "required": False},
                        },
                    },
                },
            },
            "refresh_reporting_type": {"type": "str", "required": False, "choices": ["scans", "days"]},
            "refresh_reporting_frequency_scans": {"type": "int", "required": False},
            "refresh_reporting_frequency_days": {"type": "int", "required": False},
            "disable_refresh_reporting": {"type": "str", "required": False, "choices": ["yes", "no"]},
            "emails": {"type": "str", "required": False},
            "acls": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "permissions": {
                        "type": "int",
                        "required": False,
                    },
                    "owner": {
                        "type": "int",
                        "required": False,
                    },
                    "display_name": {
                        "type": "str",
                        "required": False,
                    },
                    "name": {
                        "type": "str",
                        "required": False,
                    },
                    "id": {
                        "type": "int",
                        "required": False,
                    },
                    "type": {
                        "type": "str",
                        "required": False,
                        "choices": ["default", "user", "group"],
                    },
                },
            },
        },
    },
    "credentials": {
        "required": False,
        "type": "dict",
        "options": {
            "add": {
                "required": False,
                "type": "dict",
                "options": {
                    "Host": {
                        "required": False,
                        "type": "dict",
                        "options": {
                            "Windows": {
                                "required": False,
                                "type": "list",
                                "elements": "dict",
                                "options": {
                                    "domain": {"required": False, "type": "str"},
                                    "username": {"required": False, "type": "str"},
                                    "auth_method": {"required": False, "type": "str"},
                                    "password": {"required": False, "type": "str", "no_log": True},
                                },
                            }
                        },
                    }
                },
            }
        },
    },
    "plugin_configurations": {
        "type": "list",
        "required": False,
        "elements": "dict",
        "options": {
            "plugin_family_name": {"type": "str", "required": True},
            "plugins": {
                "type": "list",
                "required": True,
                "elements": "dict",
                "options": {
                    "plugin_id": {"type": "str", "required": True},
                    "status": {"type": "str", "required": True, "choices": ["enabled", "disabled"]},
                },
            },
        },
    },
    "category_name": {"type": "str", "required": False},
    "category_uuid": {"type": "str", "required": False},
    "category_description": {"type": "str", "required": False},
    "description": {"type": "str", "required": False},
    "access_control": {
        "type": "dict",
        "options": {
            "current_user_permissions": {"type": "list", "elements": "str", "required": False},
            "defined_domain_permissions": {"type": "list", "elements": "str", "required": False},
            "all_users_permissions": {"type": "list", "elements": "str", "required": False},
            "current_domain_permissions": {
                "type": "list",
                "elements": "dict",
                "options": {
                    "id": {"type": "str", "required": False},
                    "name": {"type": "str", "required": False},
                    "type": {"type": "str", "choices": ["USER", "GROUP", "ROLE"], "required": False},
                    "permissions": {"type": "list", "elements": "str", "required": False},
                },
                "required": False,
            },
            "version": {"type": "int", "required": False},
        },
    },
    "filters_tags": {
        "type": "dict",
        "options": {
            "asset": {
                "type": "dict",
                "options": {
                    "and": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "field": {"type": "str", "required": False},
                            "operator": {"type": "str", "required": False},
                            "value": {"type": "str", "required": False},
                        },
                        "required": False,
                    },
                    "or": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "field": {"type": "str", "required": False},
                            "operator": {"type": "str", "required": False},
                            "value": {"type": "str", "required": False},
                        },
                        "required": False,
                    },
                },
            }
        },
    },
}


REPEATED_SPECIAL_ARGS = {
    "filters": {
        "type": "dict",
        "options": {
            "asset": {
                "type": "dict",
                "options": {
                    "and": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "field": {"type": "str", "required": False},
                            "operator": {"type": "str", "required": False},
                            "value": {"type": "str", "required": False},
                        },
                        "required": False,
                    },
                    "or": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "field": {"type": "str", "required": False},
                            "operator": {"type": "str", "required": False},
                            "value": {"type": "str", "required": False},
                        },
                        "required": False,
                    },
                },
            }
        },
    },
    "value": {"type": "str", "required": True},
    "name": {"type": "str", "required": False},
    "network_id": {"type": "str", "required": True},
    "folder_id": {"type": "int", "required": True},
}


def get_spec(*param_names):
    """Extracts the specific necessary parameters."""
    return {name: ARG_SPECS[name] for name in param_names if name in ARG_SPECS}


def get_repeated_special_spec(*param_names):
    """Extracts the specific necessary parameters that arre repitted from get_spec."""
    spec = {}
    for name in param_names:
        if name in REPEATED_SPECIAL_ARGS:
            spec[name] = REPEATED_SPECIAL_ARGS[name]
    return spec
