# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_tag_values import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_tag_values.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_tag_values(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "filter_type": "and",
        "filters": [{"type": "value", "operator": "eq", "value": "test"}],
        "wildcard_fields": "category_name",
        "wildcard_text": "finance",
        "limit": 1,
        "offset": 0,
        "sort": "asc",
    }

    with patch(BASE_MODULE_PATH + "list_tag_values.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_tag_values.add_custom_filters"
    ) as mock_add_custom_filters, patch(
        BASE_MODULE_PATH + "list_tag_values.build_query_parameters"
    ) as mock_build_query_parameters, patch(
        BASE_MODULE_PATH + "list_tag_values.handle_special_filter"
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
        assert called_args[1] == "tags/values"
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
