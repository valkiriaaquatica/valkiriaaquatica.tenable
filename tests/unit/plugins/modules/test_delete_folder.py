# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.delete_folder import main


@pytest.fixture
def mock_module():
    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.delete_folder.AnsibleModule", autospec=True
    ) as mock:
        yield mock


def test_delete_folder(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "folder_id": 12346,
    }

    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.delete_folder.run_module"
    ) as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, "folders/12346", method="DELETE")
