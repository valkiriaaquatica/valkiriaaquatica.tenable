# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_agent_configuration
short_description: Returns the configuration of agents associated with a specific scanner.
version_added: "0.0.1"
description:
  - This module returns the configuration of agents associated with a specific scanner.
  - gent configuration controls agent settings for global agent software update enablement and agent auto-expiration.
  - The module is made from https://developer.tenable.com/reference/agent-config-details docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: Get agent configuratin
  get_agent_configuration:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: "123456"
    tags: get_agent_configuration

- name: Get agent configuratin using enviroment creds
  get_agent_configuration:
    scanner_id: "123456"
    tags: get_agent_configuration
"""

RETURN = r"""
api_response:
  description: Contains the raw response from the Tenable API.
  returned: success
  type: dict
  contains:
    auto_unlink:
      description: Auto unlink settings.
      returned: success
      type: dict
      contains:
        enabled:
          description: Indicates if auto unlink is enabled.
          type: bool
          sample: true
        expiration:
          description: The expiration period for auto unlink.
          type: int
          sample: 180
    software_update:
      description: Indicates if software update is enabled.
      returned: success
      type: bool
      sample: true
    hybrid_scanning_enabled:
      description: Indicates if hybrid scanning is enabled.
      returned: success
      type: bool
      sample: false
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scanner_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/{module.params['scanner_id']}/agents/config"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
