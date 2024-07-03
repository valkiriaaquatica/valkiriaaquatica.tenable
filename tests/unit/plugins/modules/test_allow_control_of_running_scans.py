# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.allow_control_of_running_scans import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "allow_control_of_running_scans.AnsibleModule", autospec=True) as mock:
        yield mock


def test_allow_control_of_running_scans(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scanner_id": 123456,
        "scan_id": 987,
        "action": "resume",
    }

    payload = {"action": "resume"}

    endpoint = "scanners/123456/scans/987"

    with patch(BASE_MODULE_PATH + "allow_control_of_running_scans.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "allow_control_of_running_scans.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["action"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
