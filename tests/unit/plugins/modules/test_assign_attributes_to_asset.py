from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.assign_attributes_to_asset import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "assign_attributes_to_asset.AnsibleModule", autospec=True) as mock:
        yield mock


def test_assign_attributes_to_asset(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "asset_uuid": "12345",
        "attributes": [{"id": "123456", "value": "Dallas"}, {"id": "23897", "value": "Paris"}],
    }

    payload = {"attributes": [{"id": "123456", "value": "Dallas"}, {"id": "23897", "value": "Paris"}]}

    endpoint = "api/v3/assets/12345/attributes"

    with patch(BASE_MODULE_PATH + "assign_attributes_to_asset.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "assign_attributes_to_asset.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["attributes"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="PUT", data=payload)
