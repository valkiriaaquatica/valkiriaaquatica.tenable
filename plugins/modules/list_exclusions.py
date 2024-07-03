# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_exclusions
short_description: Lists exclusions for your Tenable Vulnerability Management scans.
version_added: "0.0.1"
description:
  - This module lists exclusions for your Tenable Vulnerability Management scans.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/exclusions-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List exclusions in Tenable
  list_exclusions:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
- name: List exclusions in Tenable using envirometn credentials
  list_exclusions:
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    exclusions:
      description: A list of agent exclusions.
      type: list
      elements: dict
      contains:
        schedule:
          description: The schedule details of the exclusion.
          type: dict
          contains:
            endtime:
              description: The end time of the exclusion formatted as YYYY-MM-DD HH:MM:SS or null.
              type: str
              sample: null
            enabled:
              description: If true, the exclusion is scheduled.
              type: bool
              sample: false
            rrules:
              description: The recurrence rules for the exclusion or null.
              type: dict
              sample: null
            timezone:
              description: The timezone for the exclusion as returned by scans or null.
              type: str
              sample: null
            starttime:
              description: The start time of the exclusion formatted as YYYY-MM-DD HH:MM:SS or null.
              type: str
              sample: null
        network_id:
          description: The network ID associated with the exclusion.
          type: str
          sample: "00000000-0000-0000-0000-000000000000"
        last_modification_date:
          description: The last modification date of the exclusion.
          type: int
          sample: 1544459404
        creation_date:
          description: The creation date of the exclusion.
          type: int
          sample: 1544459404
        members:
          description: The members included in the exclusion.
          type: str
          sample: "192.0.2.1-192.0.2.255,192.0.2.0/24,host.domain.com"
        description:
          description: The description of the exclusion or null.
          type: str
          sample: null
        name:
          description: The name of the exclusion.
          type: str
          sample: "Western Region"
        id:
          description: The identifier of the exclusion.
          type: int
          sample: 1
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "exclusions"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
