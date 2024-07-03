# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_asset_vulnerabilities_for_plugin import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_asset_vulnerabilities_for_plugin.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_asset_vulnerabilities_for_plugin(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "asset_id": "123456",
        "plugin_id": "987654",
        "date_range": 5,
        "filters": [{"type": "plugin.name", "operator": "match", "value": "RHEL"}],
        "filter_search_type": "or",
    }

    endpoint = "workbenches/assets/123456/vulnerabilities/987654/outputs"

    with patch(BASE_MODULE_PATH + "list_asset_vulnerabilities_for_plugin.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_asset_vulnerabilities_for_plugin.build_query_parameters"
    ) as mock_build_query_parameters, patch(
        BASE_MODULE_PATH + "list_asset_vulnerabilities_for_plugin.add_custom_filters"
    ) as mock_add_custom_filters, patch(
        BASE_MODULE_PATH + "list_asset_vulnerabilities_for_plugin.handle_multiple_filters"
    ) as mock_handle_multiple_filters:

        def query_params_func():
            return mock_add_custom_filters(
                mock_build_query_parameters(
                    date_range=mock_module.return_value.params["date_range"],
                    filter_search_type=mock_module.return_value.params["filter_search_type"],
                ),
                mock_module.return_value.params["filters"],
                mock_handle_multiple_filters,
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == endpoint
        assert called_kwargs["method"] == "GET"

        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_any_call(
            date_range=mock_module.return_value.params["date_range"],
            filter_search_type=mock_module.return_value.params["filter_search_type"],
        )
        mock_add_custom_filters.assert_any_call(
            mock_build_query_parameters.return_value,
            mock_module.return_value.params["filters"],
            mock_handle_multiple_filters,
        )
