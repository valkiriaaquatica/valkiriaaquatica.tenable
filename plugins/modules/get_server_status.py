# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_server_status
short_description: Gets the server status.
version_added: "0.0.1"
description:
  - This module retrieves the server status from Tenable.io.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Get server status
  get_server_status:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    code:
      description: HTTP status code returned by the API.
      type: int
      sample: 200
    status:
      description: Status of the server.
      type: str
      sample: "ready"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")

    argument_spec = {**common_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "server/status"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
