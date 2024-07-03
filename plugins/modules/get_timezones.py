# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_timezones
short_description: Lists all available time zones in Tenable.
version_added: "0.0.1"
description:
  - This module retrieves a list of all available time zones from Tenable.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/scans-timezones docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all available time zones in Tenable
  get_timezones:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
- name: List all available time zones in Tenable using envirometn credentials
  get_timezones:
  register: all_timezones
"""

RETURN = r"""
api_response:
  description: Detailed information returned by the API.
  returned: always
  type: complex
  contains:
    data:
      description: Data containing the timezones.
      type: dict
      returned: always
      contains:
        timezones:
          description: List of timezones.
          type: list
          returned: always
          contains:
            name:
              description: The name identifier of the timezone.
              type: str
              returned: always
              sample: "Africa/Abidjan"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "scans/timezones", method="GET")


if __name__ == "__main__":
    main()
