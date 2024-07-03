# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.add_agents_to_a_group import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "add_agents_to_a_group.AnsibleModule", autospec=True) as mock:
        yield mock


def test_add_agents_to_a_group(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "group_id": "123456789",
        "criteria": {
            "filters": ["name:match:laptop"],
            "all_agents": True,
            "wildcard": "wildcard",
            "filter_type": "and",
            "hardcoded_filters": ["name:match:office"],
        },
        "items": ["1111"],
        "not_items": ["98765"],
    }
    with patch(BASE_MODULE_PATH + "add_agents_to_a_group.build_payload") as mock_build_payload:
        mock_build_payload.return_value = {
            "criteria": {
                "filters": ["name:match:laptop"],
                "all_agents": True,
                "wildcard": "wildcard",
                "filter_type": "and",
                "hardcoded_filters": ["name:match:office"],
            },
            "items": ["12345", "65789"],
            "not_items": ["98765"],
        }
        with patch(BASE_MODULE_PATH + "add_agents_to_a_group.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["criteria", "items", "not_items"])
            mock_run_module.assert_called_once_with(
                mock_module.return_value,
                "scanners/null/agent-groups/123456789/agents/_bulk/add",
                method="POST",
                data={
                    "criteria": {
                        "filters": ["name:match:laptop"],
                        "all_agents": True,
                        "wildcard": "wildcard",
                        "filter_type": "and",
                        "hardcoded_filters": ["name:match:office"],
                    },
                    "items": ["12345", "65789"],
                    "not_items": ["98765"],
                },
            )
