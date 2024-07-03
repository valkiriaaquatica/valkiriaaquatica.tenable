# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.send_instructions_to_agents_group import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "send_instructions_to_agents_group.AnsibleModule", autospec=True) as mock:
        yield mock


def test_send_instructions_to_agents_group(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "group_id": "123456",
        "criteria": {
            "all_agents": True,
            "wildcard": "wildcard",
            "filters": ["core_version:lt:10.0.0"],
            "filter_type": "and",
            "hardcoded_filters": ["hardcoded_filters"],
        },
        "directive": {"type": "restart", "options": {"hard": True, "idle": False}},
        "items": ["12345"],
        "not_items": ["98765"],
    }

    expected_payload = {
        "criteria": {
            "all_agents": True,
            "wildcard": "wildcard",
            "filters": ["core_version:lt:10.0.0"],
            "filter_type": "and",
            "hardcoded_filters": ["hardcoded_filters"],
        },
        "items": ["12345"],
        "not_items": ["98765"],
        "directive": {"type": "restart", "options": {"hard": True, "idle": False}},
    }

    with patch(
        BASE_MODULE_PATH + "send_instructions_to_agents_group.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(
        BASE_MODULE_PATH + "send_instructions_to_agents_group.run_module"
    ) as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scanners/null/agent-groups/123456/agents/_bulk/directive"
        assert called_kwargs["method"] == "POST"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(
            mock_module.return_value, ["criteria", "items", "not_items", "directive"]
        )
