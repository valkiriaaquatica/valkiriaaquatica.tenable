# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: send_instructions_to_scanner
short_description: Create instructions for a single scanner to perform.
version_added: "0.0.1"
description:
  - This module sends instructions to a specified scanner.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/io-scanners-directive docs.
options:
  scanner_uuid:
    description:
      - The UUID of the scanner.
    type: str
    required: true
  type:
    description:
      - The type of instruction to perform.
      - To restart the scanner, choose restart.
      - To modify settings, choose settings.
    type: str
    required: true
    choices: ["restart", "settings"]
  restart:
    description:
      - Options for the restart operation.
    type: dict
    required: false
    suboptions:
      hard:
        description:
          - Indicates whether or not to perform a hard restart.
          - A hard restart will inform the scanner to restart immediately regardless of what it is doing.
        type: bool
        required: false
      idle:
        description:
          - Indicates whether or not to restart when the scanning engine is idle.
        type: bool
        required: false
  settings:
    description:
      - The settings to change.
    type: list
    elements: dict
    required: false
    suboptions:
      setting:
        description:
          - The setting to send to the scanner.
          - Supported settings are backend_log_level, auto_update, and auto_update_delay
          - For information about these settings and a list of possible values to use with the settings in Tenable docs.
        type: str
        required: false
        choices: ["backend_log_level", "auto_update", "auto_update_delay"]
      value:
        description:
          - The value to use for the specified setting.
          - Choose either a single string value or a single integer value to use for the value.
        type: raw
        required: false
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: Send restart instructions to a scanner
  send_instructions_to_scanner:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scanner_uuid: "123e4567-e89b-12d3-a456-426614174000"
    type: "restart"
    restart:
      hard: true
      idle: false

- name: Send settings instructions to a scanner using enviroment creds
  send_instructions_to_scanner:
    scanner_uuid: "123e4567-e89b-12d3-a456-426614174000"
    type: "settings"
    settings:
      - setting: "backend_log_level"
        value: "debug"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    container_uuid:
      description: UUID of the container.
      type: str
    uuid:
      description: UUID of the directive.
      type: str
    sensor_uuid:
      description: UUID of the sensor.
      type: str
    owner_uuid:
      description: UUID of the owner.
      type: str
    type:
      description: Type of the directive.
      type: str
    status:
      description: Status of the directive.
      type: str
    created:
      description: Creation timestamp.
      type: int
    modified:
      description: Modification timestamp.
      type: int
    results_blob_size:
      description: Size of the results blob.
      type: int
    options:
      description: Options for the directive.
      type: dict
      contains:
        settings:
          description: List of settings.
          type: list
          elements: dict
          contains:
            setting:
              description: The setting to change.
              type: str
            value:
              description: The value for the setting.
              type: raw
    ttl:
      description: Time to live for the directive.
      type: int
    id:
      description: ID of the directive.
      type: str
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {
        "scanner_uuid": {"required": True, "type": "str"},
        "type": {"required": True, "type": "str", "choices": ["restart", "settings"]},
        "restart": {
            "required": False,
            "type": "dict",
            "options": {"hard": {"required": False, "type": "bool"}, "idle": {"required": False, "type": "bool"}},
        },
        "settings": {
            "required": False,
            "type": "list",
            "elements": "dict",
            "options": {
                "setting": {
                    "required": False,
                    "type": "str",
                    "choices": ["backend_log_level", "auto_update", "auto_update_delay"],
                },
                "value": {"required": False, "type": "raw"},
            },
        },
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    payload_keys = ["type", "restart", "settings"]
    payload = build_payload(module, payload_keys)

    if module.params["type"] == "restart" and module.params.get("settings"):
        module.fail_json(msg="You cannot provide both 'restart' and 'settings' options")
    if module.params["type"] == "settings" and module.params.get("restart"):
        module.fail_json(msg="You cannot provide both 'restart' and 'settings' options")

    scanner_uuid = module.params["scanner_uuid"]
    endpoint = f"scanners/{scanner_uuid}/directive"

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
