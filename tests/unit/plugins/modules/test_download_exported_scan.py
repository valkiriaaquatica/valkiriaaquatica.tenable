from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from unittest.mock import mock_open
from unittest.mock import patch

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.modules.download_exported_scan import main
from ansible_collections.valkiriaaquatica.tenable.tests.unit.constants import BASE_MODULE_PATH


@pytest.fixture
def mock_module():
    with patch(BASE_MODULE_PATH + "download_exported_scan.AnsibleModule", autospec=True) as mock:
        yield mock


def test_download_exported_scan(mock_module):
    mock_module.return_value.params = {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "scan_id": "1234",
        "file_id": "wedcdfgdsfr-csv",
        "download_path": "/tmp/descarga.csv",
    }

    endpoint = "scans/1234/export/wedcdfgdsfr-csv/download"

    with patch(BASE_MODULE_PATH + "download_exported_scan.TenableAPI") as mock_tenable_api, patch(
        "builtins.open", mock_open()
    ) as mock_file:
        instance = mock_tenable_api.return_value
        instance.request.return_value = {"data": b"fake_data"}

        main()

        instance.request.assert_called_once_with("GET", endpoint)
        mock_file.assert_called_once_with("/tmp/descarga.csv", "wb")
        mock_file().write.assert_called_once_with(b"fake_data")
