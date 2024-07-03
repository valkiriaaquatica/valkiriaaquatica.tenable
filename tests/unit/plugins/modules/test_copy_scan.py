from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.copy_scan import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "copy_scan.AnsibleModule", autospec=True) as mock:
        yield mock


def test_copy_scan(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scan_id": "12345",
        "folder_id": "67890",
        "name": "new scan",
    }

    payload = {"folder_id": "67890", "name": "new scan"}

    endpoint = "scans/12345/copy"

    with patch(BASE_MODULE_PATH + "copy_scan.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "copy_scan.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["folder_id", "name"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
