# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: agent_profile_operations
short_description: Assign or remove agents from a profile.
version_added: "0.0.1"
description:
  - This modulecCreates a bulk operation task to either assign agents to a profile or to remove agents from a profile.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/agent-bulk-operations-profile  docs.
options:
  action:
    description:
      - The action to perform assign or remove agents from a profile.
      - It is nto specified in the Tenable docs but is added because it helps.
    required: true
    type: str
    choices: ["assign", "remove"]
  profile_uuid:
    description:
      - The UUID of the profile to assign the agents to (only for assign action).
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.bulk
"""

EXAMPLES = r"""
- name: Assign agents to a profile
  agent_profile_operations:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    action: "assign"
    profile_uuid: "1233"
    criteria:
      all_agents: true
      wildcard: "wildcard"
      filters: ["name:match:laptop"]
      filter_type: "and"
      hardcoded_filters: ["name:match:office"]
    items:
      - "34334"
    not_items:
      - "98765"

- name: Remove agents from a profile using enviroment creds
  agent_profile_operations:
    action: "remove"
    items:
      - "22333"
      - "1111"
    not_items:
      - "3434"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    task_id:
      description: The unique identifier for the task.
      type: str
    container_uuid:
      description: The UUID of the container.
      type: str
    status:
      description: The current status of the task.
      type: str
    message:
      description: A message describing the current state of the task.
      type: str
    start_time:
      description: The start time of the task in epoch milliseconds.
      type: int
    last_update_time:
      description: The last update time of the task in epoch milliseconds.
      type: int
    total_work_units:
      description: The total number of work units for the task.
      type: int
    total_work_units_completed:
      description: The number of work units completed for the task.
      type: int
    completion_percentage:
      description: The completion percentage of the task.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "criteria", "items", "not_items")
    specific_spec = {
        "action": {"required": True, "type": "str", "choices": ["assign", "remove"]},
        "profile_uuid": {"required": False, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    action = module.params["action"]
    if action == "assign" and not module.params.get("profile_uuid"):
        module.fail_json(msg="The 'profile_uuid' parameter is required when action is 'assign'.")

    endpoint = "scanners/null/agents/_bulk/assignToProfile"
    payload_keys = ["criteria", "items", "not_items", "profile_uuid"]
    payload = build_payload(module, payload_keys)

    if action == "remove":
        payload.pop("profile_uuid", None)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
