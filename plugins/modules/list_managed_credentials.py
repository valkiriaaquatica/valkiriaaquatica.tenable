# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_managed_credentials
short_description: Lists managed credentials where you have been assigned at least CAN USE (32) permissions.
version_added: "0.0.1"
description:
  - This module lists all credential types supported for managed credentials in Tenable Vulnerability Management
  - Note This endpoint does not list scan-specific or policy-specific credentials (that is, credentials
    stored in either a scan or a policy)
    see https://developer.tenable.com/docs/determine-settings-for-credential-type
  - To view a list of scan-specific or policy-specific credentials, use the editor details endpoint (GET /editor/{type}/{id}).
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/credentials-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List managed credentials
  list_managed_credentials:
      access_key: "{{ tenable_access_key }}"
      secret_key: "{{ tenable_secret_key }}"

- name: List managed credential  types file filters with enviroment creds
  list_managed_credentials:
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    credentials:
      description: A list of managed credentials.
      type: list
      elements: dict
      contains:
        uuid:
          description: The unique identifier for the credential.
          type: str
          sample: "a3820211-a59c-4fdd-b6f9-65583f61bf61"
        name:
          description: The name of the credential.
          type: str
          sample: "Windows devices (Headquarters)"
        description:
          description: The description of the credential.
          type: str
          sample: "Use for scans of Windows devices located at headquarters."
        category:
          description: The category of the credential.
          type: dict
          contains:
            id:
              description: The identifier for the category.
              type: str
              sample: "Host"
            name:
              description: The name of the category.
              type: str
              sample: "Host"
        type:
          description: The type of the credential.
          type: dict
          contains:
            id:
              description: The identifier for the type.
              type: str
              sample: "Windows"
            name:
              description: The name of the type.
              type: str
              sample: "Windows"
        created_date:
          description: The date the credential was created, in Unix timestamp format.
          type: int
          sample: 1551295980
        created_by:
          description: Information about the user who created the credential.
          type: dict
          contains:
            id:
              description: The identifier for the user.
              type: int
              sample: 15
            display_name:
              description: The display name of the user.
              type: str
              sample: "user@example.com"
        last_used_by:
          description: Information about the last user who used the credential.
          type: dict
          contains:
            id:
              description: The identifier for the user.
              type: int
              sample: null
            display_name:
              description: The display name of the user.
              type: str
              sample: null
        permission:
          description: The permission level of the credential.
          type: int
          sample: 32
        user_permissions:
          description: The user permissions for the credential.
          type: int
          sample: 32
    pagination:
      description: Information about the pagination of the results.
      type: dict
      contains:
        total:
          description: The total number of credentials.
          type: int
          sample: 1
        limit:
          description: The number of credentials per page.
          type: int
          sample: 50
        offset:
          description: The offset for the current page of results.
          type: int
          sample: 0
        sort:
          description: The sorting criteria for the results.
          type: list
          elements: dict
          contains:
            name:
              description: The field by which the results are sorted.
              type: str
              sample: "created_date"
            order:
              description: The order of the sorting (ascending or descending).
              type: str
              sample: "desc"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "credentials/types"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
