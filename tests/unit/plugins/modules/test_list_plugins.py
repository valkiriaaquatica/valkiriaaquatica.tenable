# (c) 2024, Fernando Mendieta Ovejero (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_plugins import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_plugins.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_plugins(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "last_updated": "2024-01-01",
        "size": 10,
        "page": 1,
    }

    with patch(BASE_MODULE_PATH + "list_plugins.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_plugins.build_query_parameters"
    ) as mock_build_query_parameters:

        def query_params_func():
            return mock_build_query_parameters(
                last_updated=mock_module.return_value.params["last_updated"],
                size=mock_module.return_value.params["size"],
                page=mock_module.return_value.params["page"],
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "plugins/plugin"
        assert called_kwargs["method"] == "GET"

        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params

        mock_build_query_parameters.assert_any_call(
            last_updated=mock_module.return_value.params["last_updated"],
            size=mock_module.return_value.params["size"],
            page=mock_module.return_value.params["page"],
        )
