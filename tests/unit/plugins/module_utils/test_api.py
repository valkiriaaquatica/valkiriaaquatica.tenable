import json
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.error import URLError

import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api import TenableAPI
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import AuthenticationError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import BadRequestError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import TenableAPIError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import UnexpectedAPIResponse


@pytest.fixture
def module():
    return MagicMock()


def test_tenable_api_initialization(module):
    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    assert api.base_url == "https://cloud.tenable.com"
    assert api.headers["X-ApiKeys"] == "accessKey=test_access_key;secretKey=test_secret_key"


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request(mock_open, module):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"result": "success"}).encode("utf-8")
    mock_response.getcode.return_value = 200
    mock_open.return_value = mock_response

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    response = api.request("GET", "test_endpoint", params={"param1": "value1"})

    mock_open.assert_called_once_with(
        method="GET",
        url="https://cloud.tenable.com/test_endpoint?param1=value1",
        headers={"Accept": "application/json", "X-ApiKeys": "accessKey=test_access_key;secretKey=test_secret_key"},
        data=None,
    )
    assert response == {"status_code": 200, "data": {"result": "success"}}


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_with_data(mock_open, module):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"result": "success"}).encode("utf-8")
    mock_response.getcode.return_value = 200
    mock_open.return_value = mock_response

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    response = api.request("POST", "test_endpoint", data={"key": "value"})

    mock_open.assert_called_once_with(
        method="POST",
        url="https://cloud.tenable.com/test_endpoint",
        headers={
            "Accept": "application/json",
            "X-ApiKeys": "accessKey=test_access_key;secretKey=test_secret_key",
            "Content-Type": "application/json",
        },
        data=json.dumps({"key": "value"}).encode("utf-8"),
    )
    assert response == {"status_code": 200, "data": {"result": "success"}}


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_http_error(mock_open, module):
    mock_error_fp = MagicMock()
    mock_error_fp.read.return_value = b"Bad Request"
    mock_open.side_effect = HTTPError(url=None, code=400, msg="Bad Request", hdrs=None, fp=mock_error_fp)

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    with pytest.raises(BadRequestError) as excinfo:
        api.request("GET", "test_endpoint")
    assert "Bad Request" in str(excinfo.value)


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_auth_error(mock_open, module):
    mock_error_fp = MagicMock()
    mock_error_fp.read.return_value = b"Unauthorized"
    mock_open.side_effect = HTTPError(url=None, code=401, msg="Unauthorized", hdrs=None, fp=mock_error_fp)

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    with pytest.raises(AuthenticationError) as excinfo:
        api.request("GET", "test_endpoint")
    assert "Authentication failure. Please check your API keys." in str(excinfo.value)


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_unexpected_error(mock_open, module):
    mock_error_fp = MagicMock()
    mock_error_fp.read.return_value = b"Server Error"
    mock_open.side_effect = HTTPError(url=None, code=500, msg="Server Error", hdrs=None, fp=mock_error_fp)

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    with pytest.raises(UnexpectedAPIResponse) as excinfo:
        api.request("GET", "test_endpoint")
    assert "500" in str(excinfo.value)


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_url_error(mock_open, module):
    mock_open.side_effect = URLError("URL Error")

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    with pytest.raises(TenableAPIError) as excinfo:
        api.request("GET", "test_endpoint")
    assert "URL error occurred" in str(excinfo.value)


@patch("ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api.Request.open")
def test_tenable_api_request_timeout_error(mock_open, module):
    mock_open.side_effect = TimeoutError("Request timed out")

    module.params = {"access_key": "test_access_key", "secret_key": "test_secret_key"}
    api = TenableAPI(module)
    with pytest.raises(TenableAPIError) as excinfo:
        api.request("GET", "test_endpoint")
    assert "Request timed out" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main()
