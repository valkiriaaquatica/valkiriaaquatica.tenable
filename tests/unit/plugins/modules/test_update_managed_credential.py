# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.update_managed_credential import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "update_managed_credential.AnsibleModule", autospec=True) as mock:
        yield mock


def test_update_managed_credential(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "credential_uuid": "123456",
        "name": "name",
        "description": "description",
        "settings": {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"},
        "permissions": [{"grantee_uuid": "grantee_uuid", "type": "user", "permissions": 64, "name": "name"}],
        "ad_hoc": True,
    }

    expected_payload = {
        "name": "name",
        "description": "description",
        "settings": {"domain": "domain", "username": "username", "auth_method": "Password", "password": "password"},
        "permissions": [{"grantee_uuid": "grantee_uuid", "type": "user", "permissions": 64, "name": "name"}],
        "ad_hoc": True,
    }

    with patch(
        BASE_MODULE_PATH + "update_managed_credential.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(BASE_MODULE_PATH + "update_managed_credential.run_module") as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "credentials/123456"
        assert called_kwargs["method"] == "POST"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(
            mock_module.return_value, ["name", "description", "type", "settings", "permissions", "ad_hoc"]
        )
