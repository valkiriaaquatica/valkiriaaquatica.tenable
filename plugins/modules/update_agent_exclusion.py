# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_agent_exclusion
short_description: Updates an agent exclusion.
version_added: "0.0.1"
description:
  - This module updates an agent exclusion.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/scanners-32-agents-exclusions docs.
options:
  name:
    description:
      - The name of the exclusion.
    type: str
    required: false
  description:
    description:
      - The description of the exclusion.
    type: str
    required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.exclusion
  - valkiriaaquatica.tenable.schedule
"""

EXAMPLES = r"""
- name: Update agent exclusion
  update_agent_exclusion:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    exclusion_id: 124234
    name: "Updated exclusion name"
    description: "Updated description"
    schedule:
      enabled: true
      starttime: "2024-06-01 00:00:00"
      endtime: "2024-07-07 23:59:59"
      timezone: "US/Pacific"
      rrules:
        freq: "ONETIME"
        interval: 1
        byweekday: "SU"
        bymonthday: 1
  tags: update_agent_exclusion
"""

RETURN = r"""
changed:
  description: Indicates if the task resulted in any changes.
  returned: always
  type: bool
  sample: true
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    id:
      description: The ID of the updated exclusion.
      type: int
      sample: 124234
    name:
      description: The name of the updated exclusion.
      type: str
      sample: "Updated exclusion name"
    description:
      description: The description of the updated exclusion.
      type: str
      sample: "Updated description"
    creation_date:
      description: The date when the exclusion was created.
      type: int
      sample: 1543541807
    last_modification_date:
      description: The date when the exclusion was last modified.
      type: int
      sample: 1543541807
    schedule:
      description: Schedule details for the exclusion.
      type: dict
      contains:
        endtime:
          description: The end time of the schedule.
          type: str
          sample: "2019-12-31 19:35:00"
        enabled:
          description: Indicates if the schedule is enabled.
          type: bool
          sample: true
        rrules:
          description: Recurrence rules for the schedule.
          type: dict
          contains:
            freq:
              description: Frequency of the recurrence.
              type: str
              sample: "ONETIME"
            interval:
              description: Interval for the recurrence.
              type: int
              sample: 1
            byweekday:
              description: Days of the week for the recurrence.
              type: str
              sample: "SU"
            bymonthday:
              description: Days of the month for the recurrence.
              type: int
              sample: 1
        timezone:
          description: Timezone for the schedule.
          type: str
          sample: "US/Pacific"
        starttime:
          description: The start time of the schedule.
          type: str
          sample: "2024-06-01 00:00:00"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "schedule", "description", "exclusion_id")
    specific_spec = {
        "name": {"required": False, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    exclusion_id = module.params["exclusion_id"]
    endpoint = f"scanners/null/agents/exclusions/{exclusion_id}"

    payload_keys = ["name", "description", "schedule"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
