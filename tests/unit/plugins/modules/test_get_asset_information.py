# (c) 2024, Fernando Mendieta Ovejero (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_asset_information import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_asset_information.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_asset_information(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "asset_id": "123456",
        "all_fields": "full",
    }

    with patch(BASE_MODULE_PATH + "get_asset_information.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "get_asset_information.build_query_parameters"
    ) as mock_build_query_parameters:

        def query_params_func():
            return mock_build_query_parameters(all_fields=mock_module.return_value.params["all_fields"])

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "workbenches/assets/123456/info"
        assert called_kwargs["method"] == "GET"
        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_any_call(
            all_fields=mock_module.return_value.params["all_fields"],
        )
