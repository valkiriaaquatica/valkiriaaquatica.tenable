from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.assign_scanners import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "assign_scanners.AnsibleModule", autospec=True) as mock:
        yield mock


def test_assign_scanners(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "network_id": "12345",
        "scanner_uuid": "9874",
    }

    endpoint = "networks/12345/scanners/9874"

    with patch(BASE_MODULE_PATH + "assign_scanners.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST")
