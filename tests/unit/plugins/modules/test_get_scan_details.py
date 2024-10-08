# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_scan_details import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_scan_details.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_scan_details(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "scan_id": "11111",
        "history_id": "12345",
    }

    endpoint = "scans/11111"

    with patch(BASE_MODULE_PATH + "get_scan_details.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "get_scan_details.build_query_parameters"
    ) as mock_build_query_parameters:

        def query_params_func():
            return mock_build_query_parameters(history_id=mock_module.return_value.params["history_id"])

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == endpoint
        assert called_kwargs["method"] == "GET"

        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_called_with(history_id=mock_module.return_value.params["history_id"])
