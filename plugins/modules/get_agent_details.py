# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: get_agent_details
short_description: Retrieve detailed information of a agent using its agent_id.
version_added: "0.0.1"
description:
  - This module fetches detailed information about a specific agent.
  - The module is made from https://developer.tenable.com/reference/agents-agent-info docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.agent
"""

EXAMPLES = r"""
- name: Get information of a agent
  get_agent_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_id: 11111

- name: Get information of a agent using enviroment keys
  get_agent_details:
    agent_id: 11111
"""

RETURN = r"""
api_response:
  description: Detailed information about the network.
  type: dict
  returned: always
  contains:
    data:
      description: Detailed data about the machine including its network settings and specific attributes.
      type: dict
      returned: always
      sample:
        id: 1234567
        uuid: "the_uuid"
        name: "name_machine"
        platform: "WINDOWS"
        distro: "win-x86-64"
        ip: "10.55.0.254"
        last_scanned: 123456789
        plugin_feed_id: "202312010556"
        core_build: "7"
        core_version: "10.4.4"
        linked_on: 123456789
        last_connect: 123456789
        status: "off"
        aws_instance_id: "i-123456"
        aws_account_id: "123456789"
        supports_remote_logs: false
        network_uuid: "the_network_uuid"
        network_name: "the_network_name"
        remote_settings:
          - name: "Minimum Health Update Interval"
            setting: "min_agent_health_update_interval"
            type: "integer"
            description: "Specifies, in minutes, the minimum interval to update health events"
            min: 60
            status: "current"
            value: "60"
            default: "60"
        supports_remote_settings: true
        restart_pending: false
        health_events: []
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
    argument_spec = get_spec("access_key", "secret_key", "agent_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    run_module(module, "scanners/null/agents", module.params["agent_id"], method="GET")


if __name__ == "__main__":
    main()
