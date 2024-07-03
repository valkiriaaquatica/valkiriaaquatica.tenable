# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: download_exported_scan
short_description: Download an exported scan.
version_added: "0.0.1"
description:
  - This module download an exported scan.
  - The module is made from https://developer.tenable.com/reference/scans-export-download  docs.
  - Requires SCAN OPERATOR [24] user permissions and CAN VIEW [16] scan permissions user permissions as specified in the Tenable.io API documentation.
options:
  scan_id:
    description:
      - The unique identifier for the exported scan you want to download.
      - This identifier can be either the scans.schedule_uuid or the scans.id attribute in
        the response message from the list_scans module. Tenable recommends that you use scans.schedule_uuid
    required: true
    type: str
  file_id:
    description:
      - The ID of the file to download (Included in response from /scans/{scan_id}/export).
    required: true
    type: str
  download_path:
    description:
      - The path where the downloaded exported scan should be saved and the name.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Download exported scan using enviroment creds
  download_exported_scan:
    scan_id: "1234"
    file_id: "wedcdfgdsfr-csv"
    download_path: "/tmp/descarga.csv"

- name: Download exported scan using enviroment creds
  download_exported_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "1234"
    file_id: "wedcdfgdsfr-csv"
    download_path: "/tmp/descarga.csv"
"""

RETURN = r"""
"""


import os

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api import TenableAPI
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import TenableAPIError

from ansible.module_utils.basic import AnsibleModule

# this module does not follow the same "skeleton" of the post, get, put and patch modules


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {
        "scan_id": {"required": True, "type": "str"},
        "file_id": {"required": True, "type": "str"},
        "download_path": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/export/{module.params['file_id']}/download"
    download_path = module.params["download_path"]

    if not os.path.isdir(os.path.dirname(download_path)):
        module.fail_json(msg=f"The specified directory does not exist: {os.path.dirname(download_path)}")

    try:
        tenable_api = TenableAPI(module)
        tenable_api.headers["Accept"] = "application/octet-stream"
        response = tenable_api.request("GET", endpoint)

        with open(download_path, "wb") as f:
            f.write(response["data"])

        module.exit_json(changed=True, msg="Scan downloaded successfully", path=download_path)
    except TenableAPIError as e:
        module.fail_json(msg=str(e), status_code=getattr(e, "status_code", "Unknown"))
    except Exception as e:
        module.fail_json(msg=f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
