from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_attributes_assigned_to_asset import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_attributes_assigned_to_asset.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_attributes_assigned_to_asset(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "asset_uuid": "12345",
    }

    endpoint = "api/v3/assets/12345/attributes"

    with patch(BASE_MODULE_PATH + "list_attributes_assigned_to_asset.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="GET")
