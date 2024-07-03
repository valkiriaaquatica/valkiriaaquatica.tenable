# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: check_agent_group_operation_status
short_description: Check the status of a bulk operation on an agent group.
version_added: "0.0.1"
description:
  - This module checks the status of a bulk operation on an agent group.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/bulk-task-agent-group-status docs.
options:
  task_uuid:
    description:
      - The UUID of the task.
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.group
"""

EXAMPLES = r"""
- name: Check the status of a bulk operation on an agent group
  check_agent_group_operation_status:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    group_id: "1233"
    task_uuid: "321"

- name: Check the status of a bulk operation on an agent group using environment creds
  check_agent_group_operation_status:
    group_id: "1233"
    task_uuid: "321"
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
    end_time:
      description: The end time of the task in epoch milliseconds.
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
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "group_id")
    specific_spec = {"task_uuid": {"required": True, "type": "str"}}
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agent-groups/{module.params['group_id']}/agents/_bulk/{module.params['task_uuid']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
