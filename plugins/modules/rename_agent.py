# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rename_agent
short_description: Renames an agent.
version_added: "0.0.1"
description:
  - This module fetches renames an agent.
  - The module is made from https://developer.tenable.com/reference/io-agents-rename docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.agent
  - valkiriaaquatica.tenable.name
"""

EXAMPLES = r"""
- name: Rename agent using enviroment creds
  rename_agent:
    agent_id: "123456789"
    name: "new_name"

- name: Rename agent using creds in vars
  rename_agent:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    agent_id: "123456789"
    name: "new_name"
"""

RETURN = r"""
api_response:
  description: Detailed information about the agent.
  type: dict
  returned: always
  contains:
    data:
      description: Contains all relevant details about the agent.
      type: dict
      contains:
        agent_uuid:
          description: UUID of the agent.
          type: str
          returned: always
          sample: "1233456789"
        aws_account_id:
          description: AWS account ID associated with the agent.
          type: str
          returned: always
          sample: "1233456789"
        aws_instance_id:
          description: AWS instance ID of the agent.
          type: str
          returned: always
          sample: "i-1233456789"
        container_uuid:
          description: UUID of the container in which the agent is located.
          type: str
          returned: always
          sample: "1233456789"
        created:
          description: UNIX timestamp of when the agent was created.
          type: int
          returned: always
          sample: 1233456789
        created_in_seconds:
          description: Creation time in seconds.
          type: int
          returned: always
          sample: 1233456789
        distro:
          description: Distribution information of the agent's operating system.
          type: str
          returned: always
          sample: "1233456789"
        engine_version:
          description: Version of the scanning engine used on the agent.
          type: str
          returned: always
          sample: "1.1.1"
        health_events:
          description: List of health events associated with the agent.
          type: list
          returned: always
          sample: []
        id:
          description: Unique identifier of the agent.
          type: int
          returned: always
          sample: 1233456789
        ip:
          description: IP address of the agent.
          type: str
          returned: always
          sample: "192.168.1.0"
        last_connect:
          description: UNIX timestamp of the last time the agent connected.
          type: int
          returned: always
          sample: 1233456789
        last_connect_in_seconds:
          description: Last connection time in seconds.
          type: int
          returned: always
          sample: 1233456789
        last_scanned:
          description: UNIX timestamp of the last time the agent was scanned.
          type: int
          returned: always
          sample: 1233456789
        last_scanned_in_seconds:
          description: Last scanned time in seconds.
          type: int
          returned: always
          sample: 1233456789
        loaded_plugin_set:
          description: The set of plugins loaded during the last scan.
          type: str
          returned: always
          sample: "1233456789"
        mac_addrs:
          description: MAC addresses associated with the agent.
          type: str
          returned: always
          sample: "macs"
        modified:
          description: UNIX timestamp of when the agent was last modified.
          type: int
          returned: always
          sample: 1233456789
        modified_in_seconds:
          description: Last modified time in seconds.
          type: int
          returned: always
          sample: 1233456789
        name:
          description: Name of the agent.
          type: str
          returned: always
          sample: "name"
        network_uuid:
          description: UUID of the network to which the agent belongs.
          type: str
          returned: always
          sample: "1233456789"
        owner_uuid:
          description: UUID of the owner of the agent.
          type: str
          returned: always
          sample: "1233456789"
        platform:
          description: Operating system platform of the agent.
          type: str
          returned: always
          sample: "LINUX"
        remote_settings:
          description: Settings configured remotely for the agent.
          type: list
          elements: dict
          contains:
            allowable_values:
              description: List of allowable values for a setting.
              type: list
              elements: dict
              contains:
                value:
                  description: An allowable value for the setting.
                  type: str
                  sample: "high"
            default:
              description: Default value for the setting.
              type: str
              sample: "high"
            description:
              description: Description of the setting.
              type: str
              sample: "description"
            name:
              description: Name of the setting.
              type: str
              sample: "Sname"
            service_restart:
              description: Indicates if a service restart is needed after changing the setting.
              type: bool
              sample: true
            setting:
              description: Specific setting being described.
              type: str
              sample: "setting"
            status:
              description: Status of the setting.
              type: str
              sample: "status"
            type:
              description: Type of the setting.
              type: str
              sample: "type"
            value:
              description: Current value of the setting.
              type: str
              sample: "value"
        restart_pending:
          description: Indicates if a restart is pending for the agent.
          type: bool
          returned: always
          sample: false
        status:
          description: Current status of the agent.
          type: str
          returned: always
          sample: "off"
        supports_remote_logs:
          description: Indicates if the agent supports remote logging.
          type: bool
          returned: always
          sample: false
        supports_remote_settings:
          description: Indicates if the agent supports remote settings management.
          type: bool
          returned: always
          sample: true
        tracking_id:
          description: Tracking identifier for the agent.
          type: str
          returned: always
          sample: "tracking_id"
        ui_build:
          description: Build version of the user interface on the agent.
          type: str
          returned: always
          sample: "12"
        ui_version:
          description: Version of the user interface on the agent.
          type: str
          returned: always
          sample: "ui_version"
        uuid:
          description: UUID of the agent.
          type: str
          returned: always
          sample: "uuid"
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
    argument_spec = get_spec("access_key", "secret_key", "agent_id", "name")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/null/agents/{module.params['agent_id']}"
    payload_keys = ["name"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PATCH", data=payload)


if __name__ == "__main__":
    main()
