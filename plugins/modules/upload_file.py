# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: upload_file
short_description: Lists all available time zones in Tenable.
version_added: "0.0.1"
description:
  - This module uploads a file.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/file-upload docs.
options:
  no_enc:
    description:
      - Send value of 1 when uploading an encrypted file.
    required: false
    type: int
  file_path:
    description:
      - The file to upload.
      - The route of the file.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Upload a file that is no encrypted
  upload_file:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    file_path: "/tmp/hoss_targets.txt"

- name: Upload a file encrypted using tenable enviroment creds
  upload_file:
    file_path: "/tmp/hoss_targets.txt"
    no_enc: 1
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the API following a file upload operation.
  type: dict
  returned: always
  contains:
    data:
      description: Contains details about the uploaded file.
      type: dict
      contains:
        fileuploaded:
          description: Name of the file that was successfully uploaded.
          type: str
          returned: always
          sample: "thefilename.txt"
    status_code:
      description: HTTP status code returned by the API, indicating the result of the file upload operation.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module_with_file

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    special_args = {  # uniques for this module
        "file_path": {"type": "str", "required": True},
        "no_enc": {"type": "int", "required": False},
    }
    argument_spec = {**common_spec, **special_args}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    file_path = module.params["file_path"]

    run_module_with_file(module, "file/upload", file_path)


if __name__ == "__main__":
    main()
