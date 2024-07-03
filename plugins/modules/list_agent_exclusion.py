# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_agent_exclusion
short_description: Returns the list of current agent exclusions.
version_added: "0.0.1"
description:
  - This module returns the list of current agent exclusions.
  - Requires  SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/agent-exclusions-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List agent exclusions
  list_agent_exclusion:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"

- name: List agent exclusions with enviroment creds
  list_agent_exclusion:
"""

RETURN = r"""
exclusions:
  description: List of scan exclusions.
  returned: success
  type: list
  elements: dict
  contains:
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
    last_modification_date:
      description: The date when the exclusion was last modified.
      type: int
      sample: 1543541807
    creation_date:
      description: The date when the exclusion was created.
      type: int
      sample: 1543541807
    description:
      description: Description of the exclusion.
      type: str
      sample: "Router scan exclusion"
    name:
      description: Name of the exclusion.
      type: str
      sample: "Routers"
    id:
      description: ID of the exclusion.
      type: int
      sample: 124234
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "scanners/null/agents/exclusions"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
