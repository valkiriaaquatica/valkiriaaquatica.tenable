# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.update_agent_exclusion import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "update_agent_exclusion.AnsibleModule", autospec=True) as mock:
        yield mock


def test_update_agent_exclusion(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "exclusion_id": 124234,
        "name": "Updated exclusion name",
        "description": "Updated description",
        "schedule": {
            "enabled": True,
            "starttime": "2024-06-01 00:00:00",
            "endtime": "2024-07-07 23:59:59",
            "timezone": "US/Pacific",
            "rrules": {"freq": "ONETIME", "interval": 1, "byweekday": "SU", "bymonthday": 1},
        },
    }

    expected_payload = {
        "name": "Updated exclusion name",
        "description": "Updated description",
        "schedule": {
            "enabled": True,
            "starttime": "2024-06-01 00:00:00",
            "endtime": "2024-07-07 23:59:59",
            "timezone": "US/Pacific",
            "rrules": {"freq": "ONETIME", "interval": 1, "byweekday": "SU", "bymonthday": 1},
        },
    }

    with patch(
        BASE_MODULE_PATH + "update_agent_exclusion.build_payload", return_value=expected_payload
    ) as mock_build_payload, patch(BASE_MODULE_PATH + "update_agent_exclusion.run_module") as mock_run_module:
        main()

        mock_run_module.assert_called_once()
        called_args, called_kwargs = mock_run_module.call_args
        assert called_args[0] == mock_module.return_value
        assert called_args[1] == "scanners/null/agents/exclusions/124234"
        assert called_kwargs["method"] == "PUT"
        assert called_kwargs["data"] == expected_payload

        mock_build_payload.assert_called_once_with(mock_module.return_value, ["name", "description", "schedule"])
