from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_remediation_scan import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_remediation_scan.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_remediation_scan(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "uuid": "12345",
        "settings": {
            "name": "remediation scan",
            "description": "Scan to remediate issues",
            "scanner_id": "scanner_id",
            "target_network_uuid": "target_network_uuid",
            "scan_time_window": 180,
            "text_targets": "192.0.2.1/24",
            "file_targets": "targets.txt",
            "tag_targets": ["tag1", "tag2"],
            "agent_group_id": ["agent_group_1", "agent_group_2"],
            "emails": "user@example.com",
            "acls": [
                {"permissions": 64, "owner": 1, "display_name": "Admin", "name": "admin", "id": 1, "type": "group"}
            ],
        },
        "credentials": {
            "add": {
                "Host": {
                    "Windows": [
                        {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"}
                    ]
                }
            }
        },
        "enabled_plugins": [12345, 654212],
    }

    payload = {
        "uuid": "12345",
        "settings": {
            "name": "remediation scan",
            "description": "Scan to remediate issues",
            "scanner_id": "scanner_id",
            "target_network_uuid": "target_network_uuid",
            "scan_time_window": 180,
            "text_targets": "192.0.2.1/24",
            "file_targets": "targets.txt",
            "tag_targets": ["tag1", "tag2"],
            "agent_group_id": ["agent_group_1", "agent_group_2"],
            "emails": "user@example.com",
            "acls": [
                {"permissions": 64, "owner": 1, "display_name": "Admin", "name": "admin", "id": 1, "type": "group"}
            ],
        },
        "credentials": {
            "add": {
                "Host": {
                    "Windows": [
                        {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"}
                    ]
                }
            }
        },
        "enabled_plugins": [12345, 654212],
    }

    endpoint = "scans/remediation"

    with patch(BASE_MODULE_PATH + "create_remediation_scan.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_remediation_scan.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(
                mock_module.return_value, ["uuid", "settings", "credentials", "enabled_plugins"]
            )
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
