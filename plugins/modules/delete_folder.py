# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: delete_folder
short_description: Deletes a folder.
version_added: "0.0.1"
description:
  - This module deletes a folder.
  - If you delete a folder that contains scans, Tenable Vulnerability Management automatically moves those scans to the Trash folder
  - You cannot delete Tenable-provided folders or custom folders that belong to other users
  - The module is made from https://developer.tenable.com/reference/folders-delete  docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  folder_id:
    description:
      - The ID of the folder to delete.
    required: true
    type: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Deletes a folder using enviroment creds
  delete_folder:
    folder_id: 12346

- name: Deletes  a folder passing creds as vars
  delete_folder:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    folder_id: 12346
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable api.
  returned: always when a request is made, independent if it correct or incorrect.
  type: complex
  contains:
    status_code:
      description: The HTTP status code returned by the API if an error occurred.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_repeated_special_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "folder_id")
    special_spec = get_repeated_special_spec("folder_id")
    argument_spec = {**common_spec, **special_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"folders/{module.params['folder_id']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
