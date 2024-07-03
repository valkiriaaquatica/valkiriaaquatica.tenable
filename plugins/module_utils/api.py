import json
import mimetypes
import os
from urllib.parse import urlencode

from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six.moves.urllib.error import URLError
from ansible.module_utils.urls import Request

from .exceptions import AuthenticationError
from .exceptions import BadRequestError
from .exceptions import TenableAPIError
from .exceptions import UnexpectedAPIResponse


def get_tenable_credentials(module=None):
    access_key = None
    secret_key = None

    if module:
        access_key = module.params.get("access_key")
        secret_key = module.params.get("secret_key")

    if not access_key:
        access_key = os.getenv("TENABLE_ACCESS_KEY")
    if not secret_key:
        secret_key = os.getenv("TENABLE_SECRET_KEY")

    if not access_key or not secret_key:
        if module:
            module.fail_json(msg="Access key and secret key are required for Tenable API.")
        else:
            raise ValueError("Access key and secret key are required for Tenable API.")

    return access_key, secret_key


class TenableAPI:
    """API client class for Tenable."""

    def __init__(self, module=None, access_key=None, secret_key=None):
        self.module = module
        self.base_url = "https://cloud.tenable.com"

        if module:
            self.access_key, self.secret_key = get_tenable_credentials(module=module)
        else:
            self.access_key = access_key or os.getenv("TENABLE_ACCESS_KEY")
            self.secret_key = secret_key or os.getenv("TENABLE_SECRET_KEY")

        if not self.access_key or not self.secret_key:
            raise ValueError("Access key and secret key are required for Tenable API.")

        self.headers = {
            "Accept": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key};secretKey={self.secret_key}",
        }
        self.client = Request(validate_certs=True, timeout=30)

    def request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        if params:
            query_string = urlencode(params, doseq=True)
            url += f"?{query_string}"

        if data:
            data = json.dumps(data).encode("utf-8")
            if method in ["PATCH", "POST", "PUT"]:
                self.headers["Content-Type"] = "application/json"
        else:
            self.headers.pop("Content-Type", None)

        try:
            response = self.client.open(method=method, url=url, headers=self.headers, data=data)
            response_body = response.read()
            if response_body:
                return {"status_code": response.getcode(), "data": json.loads(response_body.decode("utf-8"))}
            else:
                return {"status_code": response.getcode(), "data": {}}
        except HTTPError as e:
            error_data = e.read().decode("utf-8")
            if e.code == 400:
                raise BadRequestError(error_data, e.code)
            elif e.code == 401:
                raise AuthenticationError("Authentication failure. Please check your API keys.", e.code)
            else:
                raise UnexpectedAPIResponse(e.code, error_data)
        except URLError as e:
            raise TenableAPIError(f"URL error occurred: {str(e)}", None)
        except TimeoutError as e:
            raise TenableAPIError(f"Request timed out: {str(e)}", None)

    def upload_file(self, endpoint: str, file_path: str) -> dict:
        url = f"{self.base_url}/{endpoint}"
        file_name = os.path.basename(file_path)
        content_type, unused_mime_type = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        self.headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        data = []
        data.append(f"--{boundary}")
        data.append(f'Content-Disposition: form-data; name="Filedata"; filename="{file_name}"')
        data.append(f"Content-Type: {content_type}")
        data.append("")

        with open(file_path, "rb") as f:
            data.append(f.read())

        data.append(f"--{boundary}--")
        data.append("")
        data = "\r\n".join(data).encode("utf-8")

        try:
            response = self.client.open(method="POST", url=url, data=data, headers=self.headers)
            response_body = response.read().decode("utf-8")
            return {"status_code": response.getcode(), "data": json.loads(response_body) if response_body else {}}
        except Exception as e:
            if self.module:
                self.module.fail_json(msg=str(e))
            else:
                raise TenableAPIError(f"Failed to upload file: {str(e)}", None)


def init_tenable_api(module=None, access_key=None, secret_key=None):
    return TenableAPI(module=module, access_key=access_key, secret_key=secret_key)
