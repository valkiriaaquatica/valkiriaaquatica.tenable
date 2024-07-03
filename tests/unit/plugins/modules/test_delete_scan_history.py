from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.delete_scan_history import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "delete_scan_history.AnsibleModule", autospec=True) as mock:
        yield mock


def test_delete_scan_history(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scan_id": "123456",
        "history_id": "23545",
        "exclude_rollover": True,
    }

    endpoint = "scans/123456/history/23545?delete_rollovers=True"

    with patch(BASE_MODULE_PATH + "delete_scan_history.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="DELETE")


def test_delete_scan_history_without_exclude_rollover(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scan_id": "123456",
        "history_id": "23545",
        "exclude_rollover": False,
    }

    endpoint = "scans/123456/history/23545"

    with patch(BASE_MODULE_PATH + "delete_scan_history.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="DELETE")
