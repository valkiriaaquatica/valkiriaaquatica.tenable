from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_agents import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_agents.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_agents(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "filters": [{"type": "platform", "operator": "eq", "value": "LINUX"}],
        "wildcard_text": "test",
        "wildcard_fields": "name",
        "limit": 100,
        "offset": 0,
        "sort": "asc",
        "filter_type": "and",
    }

    endpoint = "scanners/null/agents"

    with patch(BASE_MODULE_PATH + "list_agents.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_agents.add_custom_filters"
    ) as mock_add_custom_filters, patch(
        BASE_MODULE_PATH + "list_agents.build_query_parameters"
    ) as mock_build_query_parameters, patch(
        BASE_MODULE_PATH + "list_agents.handle_special_filter"
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
        assert called_args[1] == endpoint
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

        mock_add_custom_filters.assert_any_call(
            mock_build_query_parameters.return_value,
            mock_module.return_value.params["filters"],
            mock_handle_special_filter,
        )
