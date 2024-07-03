# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_agent_configuration
short_description: Updates the configuration of agents associated with a specific scanner.
version_added: "0.0.1"
description:
  - This module updates the configuration of agents associated with a specific scanner.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/agent-config-edit docs.
options:
  auto_unlink:
    description:
      - The auto unlink configuration.
    required: false
    type: dict
    suboptions:
      enabled:
        description:
          - If true, agent auto-unlink is enabled.
          - Enabling auto-unlink causes it to take effect against all agents retroactively.
        required: false
        type: bool
      expiration:
        description:
          - The expiration time for agents, in days.
        required: false
        type: int
  software_update:
    description:
      - The expiration time for agents, in days.
      -  If an agent has not communicated in this number of days, it will be considered expired and auto-unlinked
        if auto_unlink.enabled is true
      - Valid values are 1-365.
    required: false
    type: bool
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: Update agent configuration
  update_agent_configuration:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: 12345
    auto_unlink:
      enabled: true
      expiration: 180
    software_update: true

- name: Update agent configuration using enviroment creds
  update_agent_configuration:
    scanner_id: 12345
    auto_unlink:
      enabled: true
      expiration: 180
    software_update: true
  tags: update_agent_config
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
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scanner_id")
    specific_spec = {
        "auto_unlink": {  # unique for this module
            "required": False,
            "type": "dict",
            "options": {
                "enabled": {"required": False, "type": "bool"},
                "expiration": {"required": False, "type": "int"},
            },
        },
        "software_update": {"required": False, "type": "bool"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/{module.params['scanner_id']}/agents/config"

    payload_keys = ["software_update", "auto_unlink"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
