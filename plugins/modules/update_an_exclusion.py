# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_an_exclusion
short_description: Updates an exclusion.
version_added: "0.0.1"
description:
  - This module updates an exclusion.
  - This module is made from https://developer.tenable.com/reference/exclusions-edit docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
options:
  name:
    description:
      - The name of the exclusion.
    type: str
    required: false
  members:
    description:
      - The targets that you want excluded from scans. Specify multiple targets as a comma-separated string.
      - Targets can be in the following formats IPv4 address, range of IPv4 addresses, CIDR notation, or a FQDN.
      - Target example an individual IPv4 address 192.0.2.1
      - Target example a range of IPv4 addresses 192.0.2.1-192.0.2.255
      - Target example a CIDR notation 192.0.2.0/24
      - Target example a fully-qualified domain name FQDN host.domain.com
    type: str
    required: false
  network_id:
    description:
      - The UUID of the network object you want to update.
      - You cannot update the default network object.
      - To list all networks and get the ID use the list_networks moduke.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.exclusion
  - valkiriaaquatica.tenable.exclusion_params
  - valkiriaaquatica.tenable.schedule
"""

EXAMPLES = r"""
- name: Create a exclusion using enviroment creds
  update_an_exclusion:
    exclusion_id: 1
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

- name: Update a exclusion using variable creds
  update_an_exclusion:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    exclusion_id: 1
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
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "exclusion_id", "description", "schedule", "network_id")
    specific_spec = {
        "name": {"required": False, "type": "str"},
        "members": {"required": False, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    payload_keys = ["name", "members", "description", "schedule", "network_id"]

    payload = build_payload(module, payload_keys)
    endpoint = f"exclusions/{module.params['exclusion_id']}"

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
