# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: add_agents_to_a_group
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
"""

EXAMPLES = r"""
- name: Add agents to a group filtering
  add_agents_to_a_group:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: "123456789"
    criteria:
      filters: ["name:match:laptop"]
      all_agents: true
      wildcard: "wildcard"
      filter_type: "and"
      hardcoded_filters: ["name:match:office"]
    items: ["12345", "65789"]
    not_items: ["98765"]

- name: Add agents to a group using enviroment creds and no filters
  add_agents_to_a_group:
    group_id: "123456789"
    items: ["12345", "65789"]
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    task_id:
      description: ID of the created task.
      type: str
    container_uuid:
      description: UUID of the container.
      type: str
    status:
      description: Status of the task.
      type: str
    message:
      description: Message about the task status.
      type: str
    start_time:
      description: Start time of the task.
      type: int
    last_update_time:
      description: Last update time of the task.
      type: int
    total_work_units:
      description: Total work units of the task.
      type: int
    total_work_units_completed:
      description: Total work units completed.
      type: int
    completion_percentage:
      description: Completion percentage of the task.
      type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "criteria", "group_id", "items", "not_items")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}/agents/_bulk/add"

    payload_keys = ["criteria", "items", "not_items"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
