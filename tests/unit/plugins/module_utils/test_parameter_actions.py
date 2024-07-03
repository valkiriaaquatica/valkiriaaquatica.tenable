# Copyright: (c) 2024, Fernando Mendieta <fernandomendietaovejero@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import MagicMock

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import add_custom_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_complex_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_query_parameters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_tag_values_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_multiple_filters
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import handle_special_filter


def test_build_query_parameters():
    """Test building query parameters."""
    params = build_query_parameters(a="value1", b=["list1", "list2"], c=True, d=None)
    assert params == {"a": "value1", "b": "list1,list2", "c": "true"}


def test_handle_multiple_filters():
    """Test handling asset vulnerability filters."""
    query_params = {}
    filters = [
        {"type": "type1", "operator": "eq", "value": "value1"},
        {"type": "type2", "operator": "neq", "value": "value2"},
    ]
    result = handle_multiple_filters(query_params, filters)
    assert result == {
        "filter.0.filter": "type1",
        "filter.0.quality": "eq",
        "filter.0.value": "value1",
        "filter.1.filter": "type2",
        "filter.1.quality": "neq",
        "filter.1.value": "value2",
    }


def test_handle_special_filter():
    """Test handling special filter."""
    query_params = {}
    filters = [
        {"type": "type1", "operator": "eq", "value": "value1"},
        {"type": "type2", "operator": "neq", "value": "value2"},
    ]
    result = handle_special_filter(query_params, filters)
    assert result == {"f": "type1:eq:value1&type2:neq:value2"}


def test_add_custom_filters():
    """Test adding custom filters."""
    query_params = {}
    filters = [
        {"type": "type1", "operator": "eq", "value": "value1"},
        {"type": "type2", "operator": "neq", "value": "value2"},
    ]
    result = add_custom_filters(query_params, filters, handle_multiple_filters)
    assert result == {
        "filter.0.filter": "type1",
        "filter.0.quality": "eq",
        "filter.0.value": "value1",
        "filter.1.filter": "type2",
        "filter.1.quality": "neq",
        "filter.1.value": "value2",
    }


def test_build_payload():
    """Test building payload from module params."""
    module = MagicMock()
    module.params = {
        "param1": "value1",
        "param2": {"subparam1": "subvalue1", "subparam2": None},
        "param3": None,
        "param4": ["item1", "item2"],
    }
    keys = ["param1", "param2", "param3", "param4"]
    payload = build_payload(module, keys)
    assert payload == {"param1": "value1", "param2": {"subparam1": "subvalue1"}, "param4": ["item1", "item2"]}


def test_build_complex_payload():
    """Test building complex payload."""
    params = {
        "uuid": "test_uuid",
        "settings": {
            "setting1": "value1",
            "setting2": {"subsetting1": "subvalue1", "subsetting2": None},
            "setting3": None,
        },
        "credentials": {"cred1": {"user": "user1", "password": None}, "cred2": {"api_key": "key2"}},
        "plugin_configurations": [
            {"plugin_family_name": "family1", "plugins": [{"plugin_id": "plugin1", "status": "enabled"}]}
        ],
    }
    payload = build_complex_payload(params)
    assert payload == {
        "uuid": "test_uuid",
        "settings": {"setting1": "value1", "setting2": {"subsetting1": "subvalue1"}},
        "credentials": {"cred1": {"user": "user1"}, "cred2": {"api_key": "key2"}},
        "plugins": {"family1": {"individual": {"plugin1": "enabled"}}},
    }


def test_build_tag_values_payload():
    """Test building tag values payload."""
    params = {
        "category_name": "category1",
        "category_uuid": "uuid1",
        "value": "value1",
        "category_description": "desc1",
        "description": None,
        "access_control": {"control1": "value1", "control2": None},
        "filters": {"filter1": "value1", "filter2": None},
    }
    payload = build_tag_values_payload(params)
    assert payload == {
        "category_name": "category1",
        "category_uuid": "uuid1",
        "value": "value1",
        "category_description": "desc1",
        "access_control": {"control1": "value1"},
        "filters": {"filter1": "value1"},
    }
