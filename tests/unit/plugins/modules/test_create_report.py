from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.create_report import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "create_report.AnsibleModule", autospec=True) as mock:
        yield mock


def test_create_report(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "name": "report_test",
        "template_name": "host_vulns_summary",
        "filters": [
            {"property": "plugin_id", "operator": "eq", "value": [12345]},
            {"property": "source", "operator": "eq", "value": ["AWS"]},
        ],
    }

    payload = {
        "name": "report_test",
        "template_name": "host_vulns_summary",
        "filters": [
            {"property": "plugin_id", "operator": "eq", "value": [12345]},
            {"property": "source", "operator": "eq", "value": ["AWS"]},
        ],
    }

    endpoint = "reports/export"

    with patch(BASE_MODULE_PATH + "create_report.build_payload") as mock_build_payload:
        mock_build_payload.return_value = payload

        with patch(BASE_MODULE_PATH + "create_report.run_module") as mock_run_module:
            main()
            mock_build_payload.assert_called_once_with(mock_module.return_value, ["name", "template_name", "filters"])
            mock_run_module.assert_called_once_with(mock_module.return_value, endpoint, method="POST", data=payload)
