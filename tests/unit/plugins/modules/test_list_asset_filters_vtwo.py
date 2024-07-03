from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_asset_filters_vtwo import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_asset_filters_vtwo.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_asset_filters_vtwo(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "tag_uuids": ["123456", "987654"],
    }

    endpoint = "filters/workbenches/assets"
    payload = {"tag_uuids": ["123456", "987654"]}

    with patch(BASE_MODULE_PATH + "list_asset_filters_vtwo.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
