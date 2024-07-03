# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.list_plugins_in_family_name import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "list_plugins_in_family_name.AnsibleModule", autospec=True) as mock:
        yield mock


def test_list_plugins_in_family_name(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "Linux",
    }

    with patch(BASE_MODULE_PATH + "list_plugins_in_family_name.run_module") as mock_run_module, patch(
        BASE_MODULE_PATH + "list_plugins_in_family_name.build_payload"
    ) as mock_build_payload:
        mock_build_payload.return_value = {"name": "Linux"}  # Simulate the payload

        main()
        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "plugins/families/_byName"
        assert called_kwargs["method"] == "POST"

        mock_build_payload.assert_called_once_with(mock_module.return_value, ["name"])

        assert called_kwargs["data"] == {"name": "Linux"}
