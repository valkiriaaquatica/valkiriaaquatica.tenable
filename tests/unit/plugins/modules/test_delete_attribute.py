from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.delete_attribute import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "delete_attribute.AnsibleModule", autospec=True) as mock:
        yield mock


def test_delete_attribute(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "attribute_id": "123",
    }

    endpoint = "api/v3/assets/attributes/123"

    with patch(BASE_MODULE_PATH + "delete_attribute.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="DELETE")
