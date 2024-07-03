from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.check_agent_group_operation_status import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "check_agent_group_operation_status.AnsibleModule", autospec=True) as mock:
        yield mock


def test_check_agent_group_operation_status(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "group_id": "1233",
        "task_uuid": "321",
    }

    endpoint = "scanners/null/agent-groups/1233/agents/_bulk/321"

    with patch(BASE_MODULE_PATH + "check_agent_group_operation_status.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="GET")
