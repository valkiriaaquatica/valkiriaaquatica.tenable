# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: send_instructions_to_agents_group
short_description: Creates a bulk operation task to add agents to a group.
version_added: "0.0.1"
description:
  - This module creates a bulk operation task to add agents to a group.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module was made with https://developer.tenable.com/reference/bulk-add-agents docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
  - valkiriaaquatica.tenable.bulk
  - valkiriaaquatica.tenable.directive
"""

EXAMPLES = r"""
- name: Send restart instructions to agent group
  send_instructions_to_agents_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: "123456"
    criteria:
      all_agents: true
      wildcard: "wildcard"
      filters: ["core_version:lt:10.0.0"]
      filter_type: "and"
      hardcoded_filters: ["hardcoded_filters"]
    directive:
      type: "restart"
      options:
        hard: true
        idle: false
    items:
      - "12345"

- name: Send settings instructions to agents group using environment creds
  send_instructions_to_agents_group:
    group_id: "123456"
    criteria:
      filters: ["core_version:lt:10.0.0"]
      filter_type: "and"
      hardcoded_filters: ["hardcoded_filters"]
    directive:
      type: "settings"
      options:
        settings:
          - setting: "backend_log_level"
            value: "debug"
          - setting: "auto_update"
            value: "enabled"
    items:
      - "12345"
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
    argument_spec = get_spec("access_key", "secret_key", "criteria", "group_id", "items", "not_items", "directive")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}/agents/_bulk/directive"

    payload_keys = ["criteria", "items", "not_items", "directive"]
    payload = build_payload(module, payload_keys)

    directive_type = module.params["directive"]["type"]
    if directive_type == "restart":
        if "settings" in module.params["directive"]["options"]:
            module.fail_json(msg="Cannot use 'settings' options with 'restart' directive type")
    elif directive_type == "settings":
        if "hard" in module.params["directive"]["options"] or "idle" in module.params["directive"]["options"]:
            module.fail_json(msg="Cannot use 'hard' or 'idle' options with 'settings' directive type")

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
