# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_folders
short_description: Lists both Tenable-provided folders and the current user's custom folders.
version_added: "0.0.1"
description:
  - This module lists both Tenable-provided folders and the current user's custom folders.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/folders-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all folders in Tenable
  list_folders:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
- name: List all folders in Tenable using envirometn credentials
  list_folders:
"""

RETURN = r"""
api_response:
  description: Detailed information returned by the API.
  type: dict
  returned: always
  contains:
    data:
      description: Contains data about folders.
      type: dict
      contains:
        folders:
          description: A list of folder details retrieved from the API.
          type: list
          elements: dict
          contains:
            custom:
              description: Indicates if the folder is custom (1) or not (0).
              type: int
              returned: always
              sample: 0
            default_tag:
              description: Indicates if the folder is a default tag (1) or not (0).
              type: int
              returned: always
              sample: 1
            id:
              description: Unique identifier for the folder.
              type: int
              returned: always
              sample: 1
            name:
              description: Name of the folder.
              type: str
              returned: always
              sample: "name"
            type:
              description: Type of the folder, e.g., 'main'.
              type: str
              returned: always
              sample: "main"
            unread_count:
              description: Count of unread items in the folder.
              type: int
              returned: always
              sample: 1
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "folders", method="GET")


if __name__ == "__main__":
    main()
