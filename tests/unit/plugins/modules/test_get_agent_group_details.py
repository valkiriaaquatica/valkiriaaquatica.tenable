# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_agent_group_details import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_agent_group_details.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_agent_group_details(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "group_id": "123456",
        "filters": [{"type": "platform", "operator": "eq", "value": "LINUX"}],
        "filter_type": None,
        "limit": None,
        "offset": None,
        "sort": None,
        "wildcard_text": None,
        "wildcard_fields": None,
    }

    with patch(BASE_MODULE_PATH + "get_agent_group_details.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "get_agent_group_details.add_custom_filters"
    ) as mock_add_custom_filters, patch(
        BASE_MODULE_PATH + "get_agent_group_details.build_query_parameters"
    ) as mock_build_query_parameters, patch(
        BASE_MODULE_PATH + "get_agent_group_details.handle_special_filter"
    ) as mock_handle_special_filter:

        def query_params_func():
            return mock_add_custom_filters(
                mock_build_query_parameters(
                    filter_type=mock_module.return_value.params["filter_type"],
                    wildcard_text=mock_module.return_value.params["wildcard_text"],
                    wildcard_fields=mock_module.return_value.params["wildcard_fields"],
                    limit=mock_module.return_value.params["limit"],
                    offset=mock_module.return_value.params["offset"],
                    sort=mock_module.return_value.params["sort"],
                ),
                mock_module.return_value.params["filters"],
                mock_handle_special_filter,
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scanners/null/agent-groups/123456"
        assert called_kwargs["method"] == "GET"

        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_any_call(
            filter_type=mock_module.return_value.params["filter_type"],
            wildcard_text=mock_module.return_value.params["wildcard_text"],
            wildcard_fields=mock_module.return_value.params["wildcard_fields"],
            limit=mock_module.return_value.params["limit"],
            offset=mock_module.return_value.params["offset"],
            sort=mock_module.return_value.params["sort"],
        )
