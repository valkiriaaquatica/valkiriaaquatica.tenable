# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_network_asset_count import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_network_asset_count.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_network_asset_count(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "network_id": "123456",
        "num_days": 100,
    }

    with patch(BASE_MODULE_PATH + "get_network_asset_count.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(
            mock_module.return_value, "networks/123456/counts/assets-not-seen-in/100", method="GET"
        )
