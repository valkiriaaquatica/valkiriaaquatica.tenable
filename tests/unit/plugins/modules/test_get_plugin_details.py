# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_plugin_details import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_plugin_details.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_plugin_details(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "plugin_id": "123456",
        "filters": [{"type": "plugin.attributes.vpr.score", "operator": "gte", "value": "6.5"}],
        "filter_search_type": "and",
        "date_range": "last_7_days",
    }

    with patch(BASE_MODULE_PATH + "get_plugin_details.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "get_plugin_details.build_query_parameters"
    ) as mock_build_query_parameters:

        def query_params_func():
            return mock_build_query_parameters(
                date_range=mock_module.return_value.params["date_range"],
                filter_search_type=mock_module.return_value.params["filter_search_type"],
                filters=mock_module.return_value.params["filters"],
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "workbenches/vulnerabilities/123456/info"
        assert called_kwargs["method"] == "GET"

        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_any_call(
            date_range=mock_module.return_value.params["date_range"],
            filter_search_type=mock_module.return_value.params["filter_search_type"],
            filters=mock_module.return_value.params["filters"],
        )
