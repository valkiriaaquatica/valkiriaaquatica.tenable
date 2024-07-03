from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.enable_schedule import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "enable_schedule.AnsibleModule", autospec=True) as mock:
        yield mock


def test_enable_schedule(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scan_id": "123456",
        "enabled": True,
    }

    endpoint = "scans/123456/schedule"
    payload = {"enabled": True}

    with patch(BASE_MODULE_PATH + "enable_schedule.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="PUT", data=payload)
