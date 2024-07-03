# (c) 2024, Fernando Mendieta Ovejero (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_scanner
short_description: Updates the specified scanner.
version_added: "0.0.1"
description:
  - This module updates the specified scanner.
  - You cannot use this endpoint to assign the scanner to a network object. Instead, use the POST /networks/{network_id}/scanners/{scanner_uuid} endpoint.
  - This module is made from https://developer.tenable.com/reference/scanners-edit docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
options:
  name:
    description:
      - The new name for the scanner.
    type: str
    required: false
  force_plugin_update:
    description:
      - Pass 1 to force a plugin update.
    type: int
    required: false
  force_ui_update:
    description:
      - Pass 1 to force a UI update.
    type: int
    required: false
  finish_update:
    description:
      - Pass 1 to reboot the scanner and run the latest software update (only valid if automatic updates are disabled).
    type: int
    required: false
  registration_code:
    description:
      - Sets the registration code for the scanner.
    type: str
    required: false
  aws_update_interval:
    description:
      - Specifies how often, in minutes, the scanner checks in with Tenable Vulnerability Management (Amazon Web Services scanners only).
    type: int
    required: false
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: Update scanner name and force plugin update
  update_scanner:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scanner_id: 12345
    name: "New Scanner Name"
    force_plugin_update: 1

- name: Update scanner registration code using enviroment creds
  update_scanner:
    scanner_id: 12345
    registration_code: "new_registration_code"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    owner_uuid:
      description: The UUID of the owner.
      type: str
      sample: "169a9fad-c23b-454a-8519-285e30b11d94"
    created:
      description: Timestamp when the scanner was created.
      type: int
      sample: 1576171974205
    modified:
      description: Timestamp when the scanner was last modified.
      type: int
      sample: 1579909576455
    container_uuid:
      description: UUID of the container.
      type: str
      sample: "234a6a72-0fe6-4d5b-aaab-9f97774d42da"
    uuid:
      description: UUID of the scanner.
      type: str
      sample: "9e226caf-ef74-419a-875e-205e77534cba"
    id:
      description: ID of the scanner.
      type: int
      sample: 44741097
    name:
      description: Name of the scanner.
      type: str
      sample: "test13"
    type:
      description: Type of the scanner.
      type: str
      sample: "local"
    network_name:
      description: Network name of the scanner.
      type: str
      sample: "Default"
    default_permissions:
      description: Default permissions of the scanner.
      type: int
      sample: 16
    shared:
      description: Whether the scanner is shared.
      type: int
      sample: 1
    user_permissions:
      description: User permissions of the scanner.
      type: int
      sample: 64
    key:
      description: Key of the scanner.
      type: str
      sample: "e3eeefeacca0d998c466af126549d68ef0f4e0d0ba3ab04a6e59a1d8a8a57079"
    system:
      description: Whether the scanner is a system scanner.
      type: bool
      sample: true
    linked:
      description: Whether the scanner is linked.
      type: int
      sample: 1
    settings:
      description: Settings of the scanner.
      type: dict
      sample: {}
    aws_update_interval:
      description: AWS update interval of the scanner.
      type: int
      sample: 0
    status:
      description: Status of the scanner.
      type: str
      sample: "on"
    lce:
      description: Whether the scanner is an LCE scanner.
      type: bool
      sample: false
    pvs:
      description: Whether the scanner is a PVS scanner.
      type: bool
      sample: false
    aws:
      description: Whether the scanner is an AWS scanner.
      type: bool
      sample: false
    industrial_security:
      description: Whether the scanner supports industrial security.
      type: bool
      sample: false
    scanner_scanner:
      description: Whether the scanner is a scanner scanner.
      type: bool
      sample: false
    webapp:
      description: Whether the scanner supports web application scanning.
      type: bool
      sample: false
    group:
      description: Whether the scanner is a group scanner.
      type: bool
      sample: true
    can_factory_reset:
      description: Whether the scanner can perform a factory reset.
      type: bool
      sample: false
    system_group_scanner:
      description: Whether the scanner is a system group scanner.
      type: bool
      sample: true
    system_scanner_scanner:
      description: Whether the scanner is a system scanner scanner.
      type: bool
      sample: false
    system_webapp_scanner:
      description: Whether the scanner is a system web application scanner.
      type: bool
      sample: false
    supports_remote_logs:
      description: Whether the scanner supports remote logs.
      type: bool
      sample: false
    created_in_seconds:
      description: Creation timestamp in seconds.
      type: int
      sample: 1576171974
    modified_in_seconds:
      description: Modified timestamp in seconds.
      type: int
      sample: 1579909576
    network_id:
      description: Network ID of the scanner.
      type: str
      sample: "00000000-0000-0000-0000-000000000000"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "scanner_id")
    specific_spec = {
        "name": {"required": False, "type": "str"},  # uniques for this module
        "force_plugin_update": {"required": False, "type": "int"},
        "force_ui_update": {"required": False, "type": "int"},
        "finish_update": {"required": False, "type": "int"},
        "registration_code": {"required": False, "type": "str"},
        "aws_update_interval": {"required": False, "type": "int"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scanners/{module.params['scanner_id']}"

    payload_keys = [
        "name",
        "force_plugin_update",
        "force_ui_update",
        "finish_update",
        "registration_code",
        "aws_update_interval",
    ]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
