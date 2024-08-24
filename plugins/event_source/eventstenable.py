"""
eventstenable.py

An ansible-rulebook event source scrapper plugin module for fetching data from public Tenable API using its API.

Arguments:
---------
    endpoint: The API endpoint to query, relative to the base Tenable API URL.
              This should be a valid endpoint within the Tenable API, e.g.,
              "workbenches/vulnerabilities". Required.
    data_key: The key in the JSON response that contains the list of items to be
              processed. Default is "data", place "" to none key to filter.
              Easy to look ip up, just go to the Tenable
              API official docs and for example for: https://developer.tenable.com/reference/io-filters-assets-list
              data_key is filters
    tenable_access_key: The access key for authenticating with the Tenable API.
                       Can be provided directly or set as an environment
                       variable TENABLE_ACCESS_KEY. Required.
    tenable_secret_key: The secret key for authenticating with the Tenable API.
                       Can be provided directly or set as an environment
                       variable TENABLE_SECRET_KEY. Required.
    interval: The interval in minutes at which the API should be queried.
              Default is 5 minutes.

Example:
-------
    # gets all vulnerabilities querying every 10 minutes
    - valkiriaaquatica.tenable.eventstenable:
        endpoint: "workbenches/vulnerabilities"
        data_key: "vulnerabilities"
        tenable_access_key: "{{ TENABLE_ACCESS_KEY }}"
        tenable_secret_key: "{{ TENABLE_SECRET_KEY }}"
        interval: 10

    # gets all critical vulnerabilites  every 5 minutes
    - valkiriaaquatica.tenable.eventstenable:
        endpoint: "workbenches/vulnerabilities?filter.0.filter=severity&filter.0.quality=eq&filter.0.value=Critical"
        data_key: "vulnerabilities"
        tenable_access_key: "{{ TENABLE_ACCESS_KEY }}"
        tenable_secret_key: "{{ TENABLE_SECRET_KEY }}"
        interval: 0.5

    # gets all vulnerabilites from an asset every 30 seconds using enviroment vars
    - valkiriaaquatica.tenable.eventstenable:
        endpoint: "workbenches/assets/0004544c-0a6d-45ee-9e5f-c1fbc436092b/vulnerabilities"
        data_key: "vulnerabilities"
        interval: 0.5

    # gets plugins in nested json every day using enviroment vars
    - valkiriaaquatica.tenable.eventstenable:
        endpoint: "plugins/plugin"
        data_key: "data.plugin_details"
        interval: 1440

    # gets all agent groups querying every 30 minuted using enviroment vars
    - valkiriaaquatica.tenable.eventstenable:
        endpoint: "scanners/null/agent-groups"
        data_key: "groups"
        interval: 30
"""

import asyncio
import json
import os
from typing import Any
from typing import Dict
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlencode

from ansible.module_utils.urls import Request


class AuthenticationError(Exception):
    pass


class BadRequestError(Exception):
    pass


class TenableAPIError(Exception):
    pass


class UnexpectedAPIResponse(Exception):
    pass


def get_tenable_credentials(access_key=None, secret_key=None):
    access_key = access_key or os.getenv("TENABLE_ACCESS_KEY")
    secret_key = secret_key or os.getenv("TENABLE_SECRET_KEY")
    if not access_key or not secret_key:
        raise ValueError("Access key and secret key are required for Tenable API.")

    return access_key, secret_key


class TenableAPI:
    def __init__(self, access_key=None, secret_key=None):
        self.access_key, self.secret_key = get_tenable_credentials(access_key, secret_key)
        self.base_url = "https://cloud.tenable.com"
        self.headers = {
            "Accept": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key};secretKey={self.secret_key}",
        }
        self.client = Request(validate_certs=True, timeout=30)

    def request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"

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
                return json.loads(response_body.decode("utf-8"))
            return {}
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


def get_nested_value(d, keys):
    """Recursively get a value from a nested dictionary just when nested is in json response"""
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    valid_keys = {"endpoint", "data_key", "tenable_access_key", "tenable_secret_key", "interval"}

    for key in args:
        if key not in valid_keys:
            raise ValueError(f"Invalid argument '{key}' provided.")

    endpoint = args.get("endpoint")
    data_key = args.get("data_key", "data")
    access_key = args.get("tenable_access_key")
    secret_key = args.get("tenable_secret_key")
    interval_minutes = args.get("interval", 5)
    interval_seconds = interval_minutes * 60

    if not endpoint:
        raise ValueError("Endpoint must be provided, It cannot be empty.")

    tenable_api = TenableAPI(access_key=access_key, secret_key=secret_key)

    while True:
        try:
            response = tenable_api.request(method="GET", endpoint=endpoint)
            keys = data_key.split(".")
            data_to_process = get_nested_value(response, keys)

            if data_to_process:
                for item in data_to_process:
                    await queue.put({"tenable": item})
            else:
                await queue.put({"tenable": response})

            await asyncio.sleep(interval_seconds)

        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in Tenable plugin: {e}")


if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue(asyncio.Queue[Any]):
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    asyncio.run(main(MockQueue(), {}))
