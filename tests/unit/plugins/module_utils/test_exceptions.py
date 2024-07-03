import pytest
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import AuthenticationError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import BadRequestError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import TenableAPIError
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import UnexpectedAPIResponse


def test_tenable_api_error():
    """Test para la excepción TenableAPIError"""
    error = TenableAPIError("Error message", 500)
    assert str(error) == "Error message"
    assert error.status_code == 500


def test_authentication_error():
    """Test para la excepción AuthenticationError"""
    error = AuthenticationError("Unauthorized access", 401)
    assert str(error) == "Unauthorized access"
    assert error.status_code == 401
    assert isinstance(error, TenableAPIError)


def test_unexpected_api_response():
    """Test para la excepción UnexpectedAPIResponse"""
    error = UnexpectedAPIResponse("Unexpected error", 502)
    assert str(error) == "Unexpected error"
    assert error.status_code == 502
    assert isinstance(error, TenableAPIError)


def test_bad_request_error():
    """Test para la excepción BadRequestError"""
    error = BadRequestError("Bad request", 400)
    assert str(error) == "Bad request"
    assert error.status_code == 400
    assert isinstance(error, TenableAPIError)


# Ejecución de las pruebas
if __name__ == "__main__":
    pytest.main()
