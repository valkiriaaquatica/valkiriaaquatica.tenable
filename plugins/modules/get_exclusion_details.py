# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_exclusion_details
short_description: Returns exclusion details.
version_added: "0.0.1"
description:
  - This module returns exclusion details.
  - The module is made from https://developer.tenable.com/reference/exclusions-details docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.exclusion
"""

EXAMPLES = r"""
- name: Get information of an exclusion
  get_exclusion_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    exclusion_id: 11111

- name: Get information of an exclusion using enviroment keys
  get_exclusion_details:
    exclusion_id: 11111
"""


RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: always when a request is made, independent if it correct or incorrect.
  contains:
    data:
      description: Details of the exclusion including scheduling and network information.
      type: dict
      returned: always
      sample:
        creation_date: 123456
        description: "i am the exclusion"
        id: 123456
        last_modification_date: 123456
        members: "192.168.1.120"
        name: "exclusion"
        network_id: "123456"
        schedule:
          enabled: true
          endtime: "2023-04-01 17:00:00"
          rrules:
            bymonthday: null
            byweekday: "MO,TU,WE,TH,FR"
            freq: "WEEKLY"
            interval: 1
          starttime: "2023-04-01 09:00:00"
          timezone: "America/New_York"
    status_code:
      description: HTTP status code of the response.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "exclusion_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "exclusions", module.params["exclusion_id"], method="GET")


if __name__ == "__main__":
    main()
