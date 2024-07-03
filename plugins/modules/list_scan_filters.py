# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_scan_filters
short_description: List filters for scans.
version_added: "0.0.1"
description:
  - This module list  filters for scans.
  - Lists the filtering, sorting, and pagination capabilities available for agent records on endpoints that support them
  - Requires BASIC  [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/io-filters-scan-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List scan filters
  list_scan_filters:
      access_key: "{{ tenable_access_key }}"
      secret_key: "{{ tenable_secret_key }}"

- name: List tag asset filters with enviroment creds
  list_scan_filters:
"""


RETURN = r"""
api_response:
  description: Detailed information returned by the API.
  returned: always
  type: complex
  contains:
    data:
      description: The main data content returned by the API.
      type: dict
      returned: always
      contains:
        filters:
          description: A list of filter objects that define metadata for asset tagging.
          type: list
          returned: always
          elements: dict
          contains:
            name:
              description: The name of the filter or tag attribute.
              type: str
              returned: always
            operators:
              description: List of applicable operators for the filter.
              type: list
              elements: str
              returned: always
            readable_name:
              description: A human-readable name for the filter.
              type: str
              returned: always
            control:
              description: Defines the control type and options for the filter, applicable for dropdown or multiple choice types.
              type: dict
              returned: optional
              contains:
                list:
                  description: List of options available under this control.
                  type: list
                  elements: dict
                  contains:
                    name:
                      description: The internal name of the option.
                      type: str
                      returned: always
                    value:
                      description: The value associated with this option.
                      type: str
                      returned: always
                type:
                  description: Type of control for the UI element.
                  type: str
                  returned: always
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "filters/scans/reports"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
