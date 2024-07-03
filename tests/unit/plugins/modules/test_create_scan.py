from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_scan import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_scan.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_scan(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "uuid": "template_scan_uuid",
        "settings": {
            "name": "name_scan_creation",
            "folder_id": 111,
            "scanner_id": 123456,
            "launch": "ON_DEMAND",
            "rrules": "WEEKLY",
            "timezone": "Atlantic/Madeira",
            "text_targets": "192.168.1.1,192.168.1.2",
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
        "plugin_configurations": [
            {
                "plugin_family_name": "Red Hat Local Security Checks",
                "plugins": [{"plugin_id": "79798", "status": "enabled"}, {"plugin_id": "79799", "status": "disabled"}],
            }
        ],
    }

    payload = {
        "uuid": "template_scan_uuid",
        "settings": {
            "name": "name_scan_creation",
            "folder_id": 111,
            "scanner_id": 123456,
            "launch": "ON_DEMAND",
            "rrules": "WEEKLY",
            "timezone": "Atlantic/Madeira",
            "text_targets": "192.168.1.1,192.168.1.2",
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
        "plugin_configurations": [
            {
                "plugin_family_name": "Red Hat Local Security Checks",
                "plugins": [{"plugin_id": "79798", "status": "enabled"}, {"plugin_id": "79799", "status": "disabled"}],
            }
        ],
    }

    endpoint = "scans"

    with patch(BASE_MODULE_PATH + "create_scan.build_complex_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_scan.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value.params)
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
