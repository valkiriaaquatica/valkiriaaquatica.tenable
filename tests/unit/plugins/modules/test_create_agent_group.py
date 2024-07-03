# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_agent_group import main


@pytest.fixture
def mock_module():
    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_agent_group.AnsibleModule", autospec=True
    ) as mock:
        yield mock


def test_create_agent_group(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "test_group",
    }

    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_agent_group.build_payload"
    ) as mock_build_payload:
        mock_build_payload.return_value = {"name": "test_group"}

        with patch(
            "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_agent_group.run_module"
        ) as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["name"])
            mock_run_module.assert_called_once_with(
                mock_module.return_value, "scanners/null/agent-groups", method="POST", data={"name": "test_group"}
            )
