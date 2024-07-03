from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_group import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_group.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_group(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "Example Group",
    }

    payload = {"name": "Example Group"}

    endpoint = "groups"

    with patch(BASE_MODULE_PATH + "create_group.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_group.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["name"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
