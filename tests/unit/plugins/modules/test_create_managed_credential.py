from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_managed_credential import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_managed_credential.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_managed_credential(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "name",
        "description": "description",
        "type": "type",
        "settings": {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"},
        "permissions": [{"grantee_uuid": "grantee_uuid", "type": "user", "permissions": 64, "name": "name"}],
    }

    payload = {
        "name": "name",
        "description": "description",
        "type": "type",
        "settings": {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"},
        "permissions": [{"grantee_uuid": "grantee_uuid", "type": "user", "permissions": 64, "name": "name"}],
    }

    endpoint = "credentials"

    with patch(BASE_MODULE_PATH + "create_managed_credential.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_managed_credential.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(
                mock_module.return_value, ["name", "description", "type", "settings", "permissions"]
            )
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
