# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_groups
short_description: Returns a list of groups in Tenable.IO.
version_added: "0.0.1"
description:
  - The module returns a list of groups.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/groups-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List groups using enviroment credentials
  list_groups:
  register:
    - groups

- name: List groups using keys
  list_groups:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
  register:
    - groups
"""

RETURN = r"""
api_response:
  description: The API response containing a list of groups.
  type: dict
  returned: on success
  contains:
    groups:
      description: A list of groups retrieved from the API.
      type: list
      elements: dict
      contains:
        uuid:
          description: Unique identifier for the group.
          type: str
          returned: always
          sample: "123456"
        managed_by_saml:
          description: Indicates whether the group is managed by SAML.
          type: bool
          returned: always
          sample: false
        name:
          description: Name of the group.
          type: str
          returned: always
          sample: "Security Group"
        user_count:
          description: Number of users in the group.
          type: int
          returned: always
          sample: 24
        id:
          description: Numeric ID of the group.
          type: int
          returned: always
          sample: 1234567
        container_uuid:
          description: UUID of the container associated with the group.
          type: str
          returned: always
          sample: "123454r"
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
    endpoint = "groups"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
