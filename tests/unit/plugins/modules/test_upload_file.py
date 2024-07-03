# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.upload_file import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "upload_file.AnsibleModule", autospec=True) as mock:
        yield mock


def test_upload_file(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "file_path": "/tmp/test_file.txt",
        "no_enc": 1,
    }

    with patch(BASE_MODULE_PATH + "upload_file.run_module_with_file") as mock_run_module_with_file:
        main()

        mock_run_module_with_file.assert_called_once()
        called_args, called_kwargs = mock_run_module_with_file.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "file/upload"
        assert called_args[2] == "/tmp/test_file.txt"
        assert "no_enc" in mock_module.return_value.params
        assert mock_module.return_value.params["no_enc"] == 1
