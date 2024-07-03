# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING o https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.get_template_details import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "get_template_details.AnsibleModule", autospec=True) as mock:
        yield mock


def test_get_template_details(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "type": "scan",
        "wizard_uuid": "12345789",
    }

    with patch(BASE_MODULE_PATH + "get_template_details.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(
            mock_module.return_value, "editor/scan/templates/12345789", method="GET"
        )


def test_get_template_details_policy(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "type": "policy",
        "wizard_uuid": "987654",
    }

    with patch(BASE_MODULE_PATH + "get_template_details.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(
            mock_module.return_value, "editor/policy/templates/987654", method="GET"
        )


def test_get_template_details_remediation(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "type": "remediation",
        "wizard_uuid": "654321",
    }

    with patch(BASE_MODULE_PATH + "get_template_details.run_module") as mock_run_module:
        main()
        mock_run_module.assert_called_once_with(
            mock_module.return_value, "editor/remediation/templates/654321", method="GET"
        )
