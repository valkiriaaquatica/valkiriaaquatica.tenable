from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.force_stop_scan import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "force_stop_scan.AnsibleModule", autospec=True) as mock:
        yield mock


def test_force_stop_scan(mock_module):
    mock_module.return_value.params = {
        "access_key": "mock_access_key",
        "secret_key": "mock_secret_key",
        "scan_id": "123456",
    }

    with patch(BASE_MODULE_PATH + "force_stop_scan.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, "scans/123456/force-stop", method="POST")
