# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_tag_categories import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_tag_categories.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_tag_categories(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "limit": 1,
        "offset": 0,
        "sort": "asc",
        "filters": [{"type": "name", "operator": "eq", "value": "test"}],
        "filter_type": "and",
    }

    with patch(BASE_MODULE_PATH + "list_tag_categories.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_tag_categories.add_custom_filters"
    ) as mock_add_custom_filters, patch(
        BASE_MODULE_PATH + "list_tag_categories.build_query_parameters"
    ) as mock_build_query_parameters, patch(
        BASE_MODULE_PATH + "list_tag_categories.handle_special_filter"
    ) as mock_handle_special_filter:

        def query_params_func():
            return mock_add_custom_filters(
                mock_build_query_parameters(
                    limit=mock_module.return_value.params["limit"],
                    offset=mock_module.return_value.params["offset"],
                    sort=mock_module.return_value.params["sort"],
                    filter_type=mock_module.return_value.params["filter_type"],
                ),
                mock_module.return_value.params["filters"],
                mock_handle_special_filter,
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "tags/categories"
        assert called_kwargs["method"] == "GET"

        query_params = query_params_func()
        mock_add_custom_filters.assert_any_call(
            mock_build_query_parameters.return_value,
            mock_module.return_value.params["filters"],
            mock_handle_special_filter,
        )
        mock_build_query_parameters.assert_any_call(
            limit=mock_module.return_value.params["limit"],
            offset=mock_module.return_value.params["offset"],
            sort=mock_module.return_value.params["sort"],
            filter_type=mock_module.return_value.params["filter_type"],
        )
        mock_handle_special_filter.assert_not_called()
        actual_query_params_func = called_kwargs["query_params_func"]
        assert actual_query_params_func() == query_params
