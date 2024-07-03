# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_agent_exclusion_details
short_description: Returns details for the specified agent exclusion.
version_added: "0.0.1"
description:
  - This module returns details for the specified agent exclusion.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/agent-exclusions-details docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.exclusion
"""

EXAMPLES = r"""
- name: Get agent exclusion details
  get_agent_exclusion_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    exclusion_id: 124234

- name: Get agent exclusion details using environment credentials
  get_agent_exclusion_details:
    exclusion_id: 124234
  register: exclusion_details
"""

RETURN = r"""
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    id:
      description: The ID of the exclusion.
      type: int
      sample: 124234
    name:
      description: The name of the exclusion.
      type: str
      sample: "Routers"
    description:
      description: The description of the exclusion.
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
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "exclusion_id")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agents/exclusions/{module.params['exclusion_id']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
