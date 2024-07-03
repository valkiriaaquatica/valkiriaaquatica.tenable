# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.rename_folder import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "rename_folder.AnsibleModule", autospec=True) as mock:
        yield mock


def test_rename_folder(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "folder_id": 12345,
        "name": "new_name",
    }

    expected_payload = {"name": "new_name"}

    with patch(
        BASE_MODULE_PATH + "rename_folder.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(BASE_MODULE_PATH + "rename_folder.run_module") as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "folders/12345"
        assert called_kwargs["method"] == "PUT"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(mock_module.return_value, ["name"])
