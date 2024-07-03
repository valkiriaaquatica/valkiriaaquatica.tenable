from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_attribute import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_attribute.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_attribute(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "attributes": [
            {"name": "Location", "description": "The geographical location of the asset"},
            {"name": "Department", "description": "The department to which the asset belongs"},
        ],
    }

    payload = {
        "attributes": [
            {"name": "Location", "description": "The geographical location of the asset"},
            {"name": "Department", "description": "The department to which the asset belongs"},
        ]
    }

    endpoint = "api/v3/assets/attributes"

    with patch(BASE_MODULE_PATH + "create_attribute.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_attribute.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["attributes"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
