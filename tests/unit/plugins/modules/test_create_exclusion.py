# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_exclusion import main


@pytest.fixture
def mock_module():
    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_exclusion.AnsibleModule", autospec=True
    ) as mock:
        yield mock


def test_create_exclusion(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "test_exclusion",
        "members": "192.168.1.10,192.168.1.11",
        "description": "i am the exclusion",
        "schedule": {
            "enabled": True,
            "starttime": "2023-04-01 09:00:00",
            "endtime": "2023-04-01 17:00:00",
            "timezone": "America/New_York",
            "rrules": {"freq": "WEEKLY", "interval": 1, "byweekday": "MO,TU,WE,TH,FR"},
        },
        "network_id": "123456",
    }

    with patch(
        "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_exclusion.build_payload"
    ) as mock_build_payload:
        mock_build_payload.return_value = {
            "name": "test_exclusion",
            "members": "192.168.1.10,192.168.1.11",
            "description": "i am the exclusion",
            "schedule": {
                "enabled": True,
                "starttime": "2023-04-01 09:00:00",
                "endtime": "2023-04-01 17:00:00",
                "timezone": "America/New_York",
                "rrules": {"freq": "WEEKLY", "interval": 1, "byweekday": "MO,TU,WE,TH,FR"},
            },
            "network_id": "123456",
        }
        with patch(
            "ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_exclusion.run_module"
        ) as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(
                mock_module.return_value, ["name", "members", "description", "schedule", "network_id"]
            )
            mock_run_module.assert_called_once_with(
                mock_module.return_value,
                "exclusions",
                method="POST",
                data={
                    "name": "test_exclusion",
                    "members": "192.168.1.10,192.168.1.11",
                    "description": "i am the exclusion",
                    "schedule": {
                        "enabled": True,
                        "starttime": "2023-04-01 09:00:00",
                        "endtime": "2023-04-01 17:00:00",
                        "timezone": "America/New_York",
                        "rrules": {"freq": "WEEKLY", "interval": 1, "byweekday": "MO,TU,WE,TH,FR"},
                    },
                    "network_id": "123456",
                },
            )
