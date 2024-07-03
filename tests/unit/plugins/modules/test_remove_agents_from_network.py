# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.remove_agents_from_network import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "remove_agents_from_network.AnsibleModule", autospec=True) as mock:
        yield mock


def test_remove_agents_from_network(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "network_uuid": "123456789",
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

    expected_payload = {
        "network_uuid": "123456789",
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

    with patch(
        BASE_MODULE_PATH + "remove_agents_from_network.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(BASE_MODULE_PATH + "remove_agents_from_network.run_module") as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scanners/null/agents/_bulk/removeFromNetwork"
        assert called_kwargs["method"] == "POST"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(
            mock_module.return_value, ["network_uuid", "criteria", "items", "not_items"]
        )
