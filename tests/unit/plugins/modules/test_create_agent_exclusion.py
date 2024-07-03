from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_agent_exclusion import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_agent_exclusion.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_agent_exclusion(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "name",
        "description": "description",
        "schedule": {
            "enabled": True,
            "starttime": "2023-01-01 00:00:00",
            "endtime": "2023-12-31 23:59:59",
            "timezone": "US/Pacific",
            "rrules": {"freq": "ONETIME", "interval": 1, "byweekday": "SU", "bymonthday": 1},
        },
    }

    payload = {
        "name": "name",
        "description": "description",
        "schedule": {
            "enabled": True,
            "starttime": "2023-01-01 00:00:00",
            "endtime": "2023-12-31 23:59:59",
            "timezone": "US/Pacific",
            "rrules": {"freq": "ONETIME", "interval": 1, "byweekday": "SU", "bymonthday": 1},
        },
    }

    endpoint = "scanners/null/agents/exclusions"

    with patch(BASE_MODULE_PATH + "create_agent_exclusion.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_agent_exclusion.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["name", "description", "schedule"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
