# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: create_exclusion
short_description: Creates a new exclusion.
version_added: "0.0.1"
description:
  - This module manages agents in Tenable, allowing to add or remove agents from specific groups.
  - This module is made from https://developer.tenable.com/reference/exclusions-create  docs.
  - Requires  SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  name:
    description:
      - The name of the exclusion.
    type: str
    required: true
  members:
    description:
      - The targets that you want excluded from scans. Specify multiple targets as a comma-separated string.
      - An individual IPv4 address (192.0.2.1)
      - A range of IPv4 addresses (192.0.2.1-192.0.2.255)
      - CIDR notation (192.0.2.0/24)
      - A fully-qualified domain name (FQDN) (host.domain.com)
    type: str
    required: true
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.exclusion_params
  - valkiriaaquatica.tenable.schedule
"""

EXAMPLES = r"""
- name: Create a exclusion using enviroment creds
  create_exclusion:
    name: "name"
    description: "i am the exclusion"
    members: "192.168.1.10"
    schedule:
      enabled: true
      starttime: "2023-04-01 09:00:00"
      endtime: "2023-04-01 17:00:00"
      timezone: "America/New_York"
      rrules:
      freq: "WEEKLY"
      interval: 1
      byweekday: "MO,TU,WE,TH,FR"
    network_id: "123456"

- name: Create a exclusion using variable creds
  create_exclusion:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    name: "name"
    members: "192.168.1.10,192.168.1.11"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains the data of the exclusion that was created or updated.
      type: dict
      contains:
        creation_date:
          description: UNIX timestamp when the exclusion was created.
          type: int
          returned: always
          sample: 123456
        description:
          description: Description of the exclusion.
          type: str
          returned: always
          sample: "i am the exclusion"
        id:
          description: Unique identifier of the exclusion.
          type: int
          returned: always
          sample: 123456
        last_modification_date:
          description: UNIX timestamp when the exclusion was last modified.
          type: int
          returned: always
          sample: 123456
        members:
          description: IP addresses or other identifiers included in the exclusion.
          type: str
          returned: always
          sample: "192.168.1.120"
        name:
          description: Name of the exclusion.
          type: str
          returned: always
          sample: "exclusion"
        network_id:
          description: Network ID associated with the exclusion.
          type: str
          returned: always
          sample: "123456"
        schedule:
          description: Schedule details for when the exclusion is active.
          type: dict
          returned: always
          contains:
            enabled:
              description: Whether the schedule is enabled.
              type: bool
              sample: true
            endtime:
              description: End time of the exclusion schedule.
              type: str
              sample: "2023-04-01 17:00:00"
            rrules:
              description: Recurrence rules for the exclusion schedule.
              type: dict
              contains:
                bymonthday:
                  description: Day of the month the exclusion recurs on (if applicable).
                  type: str
                  returned: when applicable
                  sample: null
                byweekday:
                  description: Days of the week the exclusion recurs on.
                  type: str
                  sample: "MO,TU,WE,TH,FR"
                freq:
                  description: Frequency of the recurrence.
                  type: str
                  sample: "WEEKLY"
                interval:
                  description: Interval at which the recurrence repeats.
                  type: int
                  sample: 1
            starttime:
              description: Start time of the exclusion schedule.
              type: str
              sample: "2023-04-01 09:00:00"
            timezone:
              description: Timezone of the exclusion schedule.
              type: str
              sample: "America/New_York"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "description", "schedule", "network_id")
    specific_spec = {
        "name": {"required": True, "type": "str"},
        "members": {"required": True, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["name", "members", "description", "schedule", "network_id"]
    payload = build_payload(module, payload_keys)

    endpoint = "exclusions"

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
