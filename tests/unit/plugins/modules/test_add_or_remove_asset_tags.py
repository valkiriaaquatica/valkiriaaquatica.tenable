# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.add_or_remove_asset_tags import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "add_or_remove_asset_tags.AnsibleModule", autospec=True) as mock:
        yield mock


def test_add_or_remove_asset_tags(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "action": "add",
        "assets": ["123456789"],
        "tags": ["first_tag_uuid", "second_tag_uuid"],
    }

    with patch(BASE_MODULE_PATH + "add_or_remove_asset_tags.build_payload") as mock_build_payload:
        mock_build_payload.return_value = {
            "action": "add",
            "assets": ["123456789"],
            "tags": ["first_tag_uuid", "second_tag_uuid"],
        }

        with patch(BASE_MODULE_PATH + "add_or_remove_asset_tags.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["action", "assets", "tags"])
            mock_run_module.assert_called_once_with(
                mock_module.return_value,
                "tags/assets/assignments",
                method="POST",
                data={"action": "add", "assets": ["123456789"], "tags": ["first_tag_uuid", "second_tag_uuid"]},
            )
