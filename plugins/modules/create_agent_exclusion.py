# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_agent_exclusion
short_description: Creates a new agent exclusion.
version_added: "0.0.1"
description:
  - This module creates a new agent exclusion.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/agent-exclusions-create docs.
options:
  description:
    description:
      - The description of the exclusion.
    type: str
    required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.name
  - valkiriaaquatica.tenable.schedule
"""

EXAMPLES = r"""
- name: Create agent exclusion
  create_agent_exclusion:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    name: "name"
    description: "description"
    schedule:
      enabled: true
      starttime: "2023-01-01 00:00:00"
      endtime: "2023-12-31 23:59:59"
      timezone: "US/Pacific"
      rrules:
        freq: "ONETIME"
        interval: 1
        byweekday: "SU"
        bymonthday: 1
  tags: create_agent_exclusion
"""

RETURN = r"""
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    id:
      description: The ID of the created exclusion.
      type: int
      sample: 124234
    name:
      description: The name of the created exclusion.
      type: str
      sample: "Routers"
    description:
      description: The description of the created exclusion.
      type: str
      sample: "Router scan exclusion"
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
              sample: "DAILY"
            interval:
              description: Interval for the recurrence.
              type: int
              sample: 8
            byweekday:
              description: Days of the week for the recurrence.
              type: str
              sample: "SU,MO"
            bymonthday:
              description: Days of the month for the recurrence.
              type: int
              sample: 9
        timezone:
          description: Timezone for the schedule.
          type: str
          sample: "US/Pacific"
        starttime:
          description: The start time of the schedule.
          type: str
          sample: "2018-12-31 19:35:00"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "schedule", "name", "description")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scanners/null/agents/exclusions"

    payload_keys = ["name", "description", "schedule"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
