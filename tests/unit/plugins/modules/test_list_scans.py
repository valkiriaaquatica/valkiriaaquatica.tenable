from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_scans import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_scans.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_scans(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "folder_id": 123456,
        "last_modification_date": 1234567890,
    }

    with patch(BASE_MODULE_PATH + "list_scans.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_scans.build_query_parameters"
    ) as mock_build_query_parameters:

        def query_params_func():
            return mock_build_query_parameters(
                folder_id=mock_module.return_value.params["folder_id"],
                last_modification_date=mock_module.return_value.params["last_modification_date"],
            )

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scans"
        assert called_kwargs["method"] == "GET"
        expected_query_params = query_params_func()
        actual_query_params = called_kwargs["query_params_func"]()

        assert expected_query_params == actual_query_params
        mock_build_query_parameters.assert_any_call(
            folder_id=mock_module.return_value.params["folder_id"],
            last_modification_date=mock_module.return_value.params["last_modification_date"],
        )
