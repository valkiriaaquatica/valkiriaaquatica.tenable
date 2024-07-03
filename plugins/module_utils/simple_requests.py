from .api import TenableAPI
from .exceptions import TenableAPIError


def run_module(
    module, endpoint: str, param: str = None, method: str = None, data: dict = None, query_params_func=None, **kwargs
):
    tenable_api = TenableAPI(module)
    changed = False
    if param:
        endpoint = f"{endpoint}/{param}"
    query_params = {}
    if query_params_func:
        query_params = query_params_func(**kwargs)
    try:
        if method in ["POST", "PUT", "DELETE", "PATCH"]:
            changed = True
            response = tenable_api.request(method, endpoint, params=query_params, data=data)
        else:
            response = tenable_api.request(method, endpoint, params=query_params)
        module.exit_json(changed=changed, api_response=response)
    except TenableAPIError as e:
        module.fail_json(msg=str(e), status_code=getattr(e, "status_code", "Unknown"))


def run_module_with_file(module, endpoint: str, file_path: str):
    tenable_api = TenableAPI(module)
    try:
        response = tenable_api.upload_file(endpoint, file_path)
        module.exit_json(changed=True, api_response=response)
    except TenableAPIError as e:
        module.fail_json(msg=str(e), status_code=getattr(e, "status_code", "Unknown"))
