# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_agent_groups
short_description: Retrieves a list of agent groups.
version_added: "0.0.1"
description:
  - This module retrieves a list of agent groups.
  - The module is made from https://developer.tenable.com/reference/agents-agent-info docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List agent groups
  list_agent_groups:
    access_key: "your_access_key"
    secret_key: "your_secret_key"

- name: List agent groups with envioment creds
  list_agent_groups:
"""

RETURN = r"""
api_response:
  description: The API response containing a list of assets.
  returned: on success
  type: dict
  contains:
    data:
      description: A list of agent groups.
      type: dict
      contains:
        assets:
          description: Details of each group.
          type: list
          elements: dict
          contains:
            groups:
              description: Details information of the agent group.
              type: list
              elements: dict
              contains:
                id:
                  description: Unique identifier for the group.
                  type: int
                  returned: always
                  sample: 12345
                uuid:
                  description: UUID associated with the group.
                  type: str
                  returned: always
                  sample: "12345678"
                name:
                  description: Name of the group.
                  type: str
                  returned: always
                  sample: "account_1"
                creation_date:
                  description: Timestamp when the group was created.
                  type: int
                  returned: always
                  sample: 111111
                last_modification_date:
                  description: Timestamp when the group was last modified.
                  type: int
                  returned: always
                  sample: 222222
                timestamp:
                  description: Timestamp when the last action was performed on the group.
                  type: int
                  returned: always
                  sample: 333333
                shared:
                  description: Indicates if the group is shared with other users.
                  type: int
                  returned: always
                  sample: 1
                owner:
                  description: The system account that owns the group.
                  type: str
                  returned: always
                  sample: "system"
                owner_id:
                  description: The system-generated ID of the owner.
                  type: int
                  returned: always
                  sample: 1111
                owner_name:
                  description: The name of the owner.
                  type: str
                  returned: always
                  sample: "system"
                owner_uuid:
                  description: The UUID of the owner.
                  type: str
                  returned: always
                  sample: "11111"
                user_permissions:
                  description: The permissions associated with the user.
                  type: int
                  returned: always
                  sample: 111
                agents_count:
                  description: Number of agents in the group.
                  type: int
                  returned: always
                  sample: 0
          returned: always
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
    run_module(module, "scanners/null/agent-groups", method="GET")


if __name__ == "__main__":
    main()
