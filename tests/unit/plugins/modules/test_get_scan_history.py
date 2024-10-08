from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_scan_history import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_scan_history.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_scan_history(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "scan_id": "123456",
        "exclude_rollover": True,
        "limit": 1,
    }

    endpoint = "scans/123456/history?exclude_rollover=True"

    with patch(BASE_MODULE_PATH + "get_scan_history.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="GET")
