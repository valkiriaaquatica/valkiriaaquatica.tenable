# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_agent_group
short_description: Creates an agent group.
version_added: "0.0.1"
description:
  - This module creates an agent group.
  - The module is made from https://developer.tenable.com/reference/agent-groups-create docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  name:
    description:
      - The name of the agent group.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Create agent group  using enviroment creds
  create_agent_group:
    name: "name"

- name: Create agent group passing creds as vars
  create_agent_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    name: "name"
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable API after a request.
  type: dict
  returned: always
  contains:
    data:
      description: Contains detailed information about the agent group.
      type: dict
      returned: always
      contains:
        agents_count:
          description: Number of agents in the group.
          type: int
          returned: always
          sample: 0
        creation_date:
          description: The date when the agent group was created.
          type: str
          returned: always
          sample: "2021-01-01T00:00:00Z"
        id:
          description: Unique identifier for the agent group.
          type: int
          returned: always
          sample: 123456
        last_modification_date:
          description: The date when the agent group was last modified.
          type: str
          returned: always
          sample: "2021-01-02T00:00:00Z"
        name:
          description: The name of the agent group.
          type: str
          returned: always
          sample: "example_group"
        owner:
          description: The id that owns the agent group.
          type: str
          returned: always
          sample: "system"
        owner_id:
          description: The  ID of the owner.
          type: int
          returned: always
          sample: 123456
        owner_name:
          description: The name of the owner.
          type: str
          returned: always
          sample: "system"
        owner_uuid:
          description: The UUID of the owner.
          type: str
          returned: always
          sample: "123456"
        shared:
          description: Indicates if the group is shared with other users.
          type: int
          returned: always
          sample: 0
        timestamp:
          description: The timestamp when the last modification was made.
          type: int
          returned: always
          sample: 1610000000
        user_permissions:
          description: The permissions associated with the user.
          type: int
          returned: always
          sample: 0
        uuid:
          description: The UUID of the agent group.
          type: str
          returned: always
          sample: "123456"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {"name": {"required": True, "type": "str"}}
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scanners/null/agent-groups"

    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
