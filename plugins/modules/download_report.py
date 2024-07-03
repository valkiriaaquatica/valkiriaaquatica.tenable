# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: download_report
short_description: Downloads the specified PDF report.
version_added: "0.0.1"
description:
  - Downloads the specified PDF report.
  - The module is made from  https://developer.tenable.com/reference/vm-reports-download  docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  report_uuid:
    description:
      - The UUID of the report to download.
    required: true
    type: str
  download_path:
    description:
      - The path where the downloaded PDF report should be saved and the name.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

RETURN = r"""
path:
  description: The path where the downloaded PDF report is saved.
  returned: always
  type: str
  sample: "/path/to_save/report.pdf"
size:
  description: The size of the downloaded PDF report in bytes.
  returned: always
  type: int
  sample: 46938
msg:
  description: A message indicating the status of the download.
  returned: always
  type: str
  sample: "Report downloaded successfully"
"""

EXAMPLES = r"""
- name: Download a report
  download_report:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    report_uuid: "123456"
    download_path: "/tmp/report.pdf"

- name: Download a report using enviroment creds
  download_report:
    report_uuid: "123456"
    download_path: "/tmp/report.pdf"
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
        "report_uuid": {"required": True, "type": "str"},
        "download_path": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"reports/export/{module.params['report_uuid']}/download"
    download_path = module.params["download_path"]

    if not os.path.isdir(os.path.dirname(download_path)):
        module.fail_json(msg=f"The specified directory does not exist: {os.path.dirname(download_path)}")

    try:
        tenable_api = TenableAPI(module)
        tenable_api.headers["Accept"] = "application/pdf"
        response = tenable_api.request("GET", endpoint)

        with open(download_path, "wb") as f:
            f.write(response["data"])

        module.exit_json(changed=True, msg="Report downloaded successfully", path=download_path)
    except TenableAPIError as e:
        module.fail_json(msg=str(e), status_code=getattr(e, "status_code", "Unknown"))
    except Exception as e:
        module.fail_json(msg=f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
