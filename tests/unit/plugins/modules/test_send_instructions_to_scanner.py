# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.send_instructions_to_scanner import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "send_instructions_to_scanner.AnsibleModule", autospec=True) as mock:
        yield mock


def test_send_instructions_to_scanner(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scanner_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "type": "restart",
        "restart": {"hard": True, "idle": False},
    }

    expected_payload = {"type": "restart", "restart": {"hard": True, "idle": False}}

    with patch(
        BASE_MODULE_PATH + "send_instructions_to_scanner.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(BASE_MODULE_PATH + "send_instructions_to_scanner.run_module") as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scanners/123e4567-e89b-12d3-a456-426614174000/directive"
        assert called_kwargs["method"] == "POST"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(mock_module.return_value, ["type", "restart", "settings"])
