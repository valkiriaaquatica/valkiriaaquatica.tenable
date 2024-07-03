# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.agent_profile_operations import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "agent_profile_operations.AnsibleModule", autospec=True) as mock:
        yield mock


def test_agent_profile_operations_assign(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "action": "assign",
        "profile_uuid": "1233",
        "criteria": {
            "filters": ["name:match:laptop"],
            "all_agents": True,
            "wildcard": "wildcard",
            "filter_type": "and",
            "hardcoded_filters": ["name:match:office"],
        },
        "items": ["34334"],
        "not_items": ["98765"],
    }

    payload = {
        "criteria": {
            "filters": ["name:match:laptop"],
            "all_agents": True,
            "wildcard": "wildcard",
            "filter_type": "and",
            "hardcoded_filters": ["name:match:office"],
        },
        "items": ["34334"],
        "not_items": ["98765"],
        "profile_uuid": "1233",
    }

    endpoint = "scanners/null/agents/_bulk/assignToProfile"

    with patch(BASE_MODULE_PATH + "agent_profile_operations.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "agent_profile_operations.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(
                mock_module.return_value, ["criteria", "items", "not_items", "profile_uuid"]
            )
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)


def test_agent_profile_operations_remove(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "action": "remove",
        "criteria": {
            "filters": ["name:match:laptop"],
            "all_agents": True,
            "wildcard": "wildcard",
            "filter_type": "and",
            "hardcoded_filters": ["name:match:office"],
        },
        "items": ["34334"],
        "not_items": ["98765"],
    }

    payload = {
        "criteria": {
            "filters": ["name:match:laptop"],
            "all_agents": True,
            "wildcard": "wildcard",
            "filter_type": "and",
            "hardcoded_filters": ["name:match:office"],
        },
        "items": ["34334"],
        "not_items": ["98765"],
    }

    endpoint = "scanners/null/agents/_bulk/assignToProfile"

    with patch(BASE_MODULE_PATH + "agent_profile_operations.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "agent_profile_operations.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(
                mock_module.return_value, ["criteria", "items", "not_items", "profile_uuid"]
            )
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
