# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: add_agents_to_a_network
short_description: Creates a bulk operation task to add agents to a custom network.
version_added: "0.0.1"
description:
  - This module creates a bulk operation task to add agents to a custom network.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Is set to network_uuid  differente from other modules where is network_id because here creates the payload.
  - This module was made with https://developer.tenable.com/reference/io-agent-bulk-operations-add-to-network docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
options:
  network_uuid:
    description:
      - The UUID of the network object you want to update.
      -  You cannot update the default network object.
      - To list all networks and get the ID use the list_networks moduke.
    required: true
    type: str
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.bulk
"""

EXAMPLES = r"""
- name: Add agents to a group filtering
  add_agents_to_a_network:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    network_uuid: "123456789"
    criteria:
      filters: ["name:match:laptop"]
      all_agents: true
      wildcard: "wildcard"
      filter_type: "and"
      hardcoded_filters: ["name:match:office"]
    items: ["12345", "65789"]
    not_items: ["98765"]

- name: Add agents to a group using enviroment creds and no filters
  add_agents_to_a_network:
    network_uuid: "123456789"
    items: ["12345", "65789"]
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
    argument_spec = get_spec("access_key", "secret_key", "criteria", "items", "not_items", "network_uuid")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scanners/null/agents/_bulk/addToNetwork"

    payload_keys = ["network_uuid", "criteria", "items", "not_items"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
