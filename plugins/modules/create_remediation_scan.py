# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_remediation_scan
short_description: Create a remediation scan configuration.
version_added: "0.0.1"
description:
  - This module creates a remediation scan configuration in Tenable.io.
  - Note Tenable Vulnerability Management limits the number of scans you can create to 10,000 scans.
  - Tenable recommends you re-use scheduled scans instead of creating new scans.
  - An HTTP 403 error is returned if you attempt to create a scan after you have already reached the scan limit of 10,000.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
  - This module is made from https://developer.tenable.com/reference/io-scans-remediation-create docs.
options:
  uuid:
    description:
      - The UUID for the Tenable-provided remediation scan template to use.
      - Use the list_templates module to list the available scan templates.
    required: true
    type: str
  settings:
    description:
      - Settings object for the remediation scan.
    required: true
    type: dict
    suboptions:
      name:
        description:
          - The name of the scan.
        required: true
        type: str
      description:
        description:
          - The description of the scan.
        required: false
        type: str
      scanner_id:
        description:
          - The unique ID of the scanner to use.
          - Use the list_scanners module to find de scanner id.
          - You can use the special value AUTO-ROUTED to assign scan targets to scanner groups based on the groups'
            configured scan route.
          - For more information on Auto-Routed see https://developer.tenable.com/docs/manage-scan-routing-tio .
          - If no scanner_id is passed in the request, Tenable assigns the US Cloud Scanner by default.
        required: false
        type: str
      target_network_uuid:
        description:
          - Network UUID that targets the scan.
          - This field is required if the scanner_id parameter is AUTO-ROUTED
          - If your scans involve separate environments with overlapping IP ranges, specify the UUID of the network you want
            to associate with the results of the auto-routed scan
          - This value must match the network where you have assigned the scanner groups that you configured for scan routing.
          - Note This parameter does not override network associations for scans that are not auto-routed.
          - Tenable Vulnerability Management automatically associates a non-routed scan with the network to which you have
            assigned the scanner that performs the scan.
        required: false
        type: str
      scan_time_window:
        description:
          - Time window in minutes for when the scan can run.
          - For Nessus Agent scans is the time frame in minutes during agents send data to tenable. If no value is passed,
            tenable assigns 180 min.
          - For Nessus Scanner is the time frame, in minutes, after which the scan will automatically stop. If no value
            is passed, Tenable assigns 0 min.
        required: false
        type: int
      text_targets:
        description:
          - The list of targets to scan.
          - This parameter is required if your request omits other target parameters.
          - Note that Tenable does not verify if values passed are correct or not.
        required: false
        type: str
      target_groups:
        description:
          - DEPRECATED
        required: false
        type: list
        elements: int
      file_targets:
        description:
          - The name of a file containing the list of targets to scan.
          - Before you use this parameter, use the upload_file module to upload the file to Tenable Vulnerability Management; then,
            use the fileuploaded attribute of the response message as the file_targets parameter value.
          - This parameter is required if your request omits other target parameters.
          - Note Unicode/UTF-8 encoding is not supported in the targets file.
        required: false
        type: str
      tag_targets:
        description:
          - The list of asset tag identifiers that the scan uses to determine which assets it evaluates.
          - For more information about tag-based scans, see https://developer.tenable.com/docs/manage-tag-based-scans-tio .
          - This parameter is required if your request omits other target parameters.
        required: false
        type: list
        elements: str
      agent_group_id:
        description:
          - An array of agent group UUIDs to scan.
          - Required if the scan is an agent scan.
        required: false
        type: list
        elements: str
      emails:
        description:
          - Email addresses to notify when the scan completes.
          - A comma-separated list of accounts that receive the email summary report.
        required: false
        type: str
      acls:
        description:
          - A list of access control entries specifying permissions to apply to the scan.
          - An array containing permissions to apply to the scan.
        type: list
        elements: dict
        required: False
        suboptions:
          permissions:
            description:
              - The scan permission.
              - For more information, refer to the Permissions section in the Tenable documentation.
            type: int
            required: False
          owner:
            description:
              - Indicates whether the specified user or group owns the scan.
              - Possible values are null (system-owned), 0 (not an owner), 1 (owner).
            type: int
            required: False
          display_name:
            description:
              - The display name of the user or group in the Tenable Vulnerability Management UI.
            type: str
            required: False
          name:
            description:
              - The name of the user or group granted the permissions.
            type: str
            required: False
          id:
            description:
              - The identifier used to order the display of user or groups in the Permissions tab in the Tenable Vulnerability Management UI.
            type: int
            required: False
          type:
            description:
              - The type of scan permission.
              - "'default' for default permissions, 'user' for individual user permissions, 'group' for user group permissions."
            type: str
            required: False
  enabled_plugins:
    description:
      - A comma-delimited list of plugins IDs to add to a remediation scan.
    required: false
    type: list
    elements: int
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan_credentials
"""

EXAMPLES = r"""
- name: Create a remediation scan with explicit credentials
  create_remediation_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    uuid: "12345"
    settings:
      name: "remediation scan"
      description: "Scan to remediate issues"
      scanner_id: "scanner_id"
      target_network_uuid: "target_network_uuid"
      scan_time_window: 180
      text_targets: "192.0.2.1/24"
      file_targets: "targets.txt"
      tag_targets:
        - "tag1"
        - "tag2"
      agent_group_id:
        - "agent_group_1"
        - "agent_group_2"
      emails: "user@example.com"
      acls:
        - permissions: 64
          owner: 1
          display_name: "Admin"
          name: "admin"
          id: 1
          type: "group"
    credentials:
      add:
        Host:
          Windows:
            - domain: "domain"
              username: "username"
              auth_method: "Password"
              password: "password"
    enabled_plugins:
      - 12345
      - 654212

- name: Create a remediation scan using environment credentials
  create_remediation_scan:
    uuid: "12345"
    settings:
      name: "remediation scan"
      description: "Scan to remediate issues"
      text_targets: "192.0.2.1/24"
"""

RETURN = r"""
api_response:
  description: Response from the Tenable.io API.
  type: dict
  returned: always
  contains:
    scan:
      description: Details of the created scan.
      type: dict
      contains:
        tag_type:
          description: The tag type.
          type: str
        container_id:
          description: The container ID.
          type: str
        owner_uuid:
          description: The owner UUID.
          type: str
        uuid:
          description: The UUID of the scan.
          type: str
        name:
          description: The name of the scan.
          type: str
        description:
          description: The description of the scan.
          type: str
        policy_id:
          description: The policy ID.
          type: int
        scanner_id:
          description: The scanner ID.
          type: str
        scanner_uuid:
          description: The scanner UUID.
          type: str
        emails:
          description: The emails associated with the scan.
          type: str
        sms:
          description: The SMS associated with the scan.
          type: str
        enabled:
          description: Indicates if the scan is enabled.
          type: bool
        include_aggregate:
          description: Indicates if aggregate is included.
          type: bool
        scan_time_window:
          description: The scan time window.
          type: int
        custom_targets:
          description: The custom targets of the scan.
          type: str
        target_network_uuid:
          description: The target network UUID.
          type: str
        auto_routed:
          description: Indicates if the scan is auto-routed.
          type: bool
        remediation:
          description: Indicates if the scan is a remediation scan.
          type: bool
        starttime:
          description: The start time of the scan.
          type: str
        rrules:
          description: The recurrence rules for the scan.
          type: str
        timezone:
          description: The timezone of the scan.
          type: str
        notification_filters:
          description: The notification filters of the scan.
          type: str
        shared:
          description: Indicates if the scan is shared.
          type: bool
        user_permissions:
          description: The user permissions for the scan.
          type: int
        default_permissions:
          description: The default permissions for the scan.
          type: int
        owner:
          description: The owner of the scan.
          type: str
        owner_id:
          description: The owner ID.
          type: int
        last_modification_date:
          description: The last modification date of the scan.
          type: int
        creation_date:
          description: The creation date of the scan.
          type: int
        type:
          description: The type of the scan.
          type: str
        id:
          description: The ID of the scan.
          type: int
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key", "uuid", "credentials")
    specific_spec = {
        "uuid": {"required": True, "type": "str"},
        "settings": {  # different from the one in arguments that uses create_scan module
            "required": True,
            "type": "dict",
            "options": {
                "name": {"required": True, "type": "str"},
                "description": {"required": False, "type": "str"},
                "scanner_id": {"required": False, "type": "str"},
                "target_network_uuid": {"required": False, "type": "str"},
                "scan_time_window": {"required": False, "type": "int"},
                "text_targets": {"required": False, "type": "str"},
                "target_groups": {"required": False, "type": "list", "elements": "int"},
                "file_targets": {"required": False, "type": "str"},
                "tag_targets": {"required": False, "type": "list", "elements": "str"},
                "agent_group_id": {"required": False, "type": "list", "elements": "str"},
                "emails": {"required": False, "type": "str"},
                "acls": {
                    "required": False,
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "permissions": {"required": False, "type": "int"},
                        "owner": {"required": False, "type": "int"},
                        "display_name": {"required": False, "type": "str"},
                        "name": {"required": False, "type": "str"},
                        "id": {"required": False, "type": "int"},
                        "type": {"required": False, "type": "str"},
                    },
                },
            },
        },
        "enabled_plugins": {"required": False, "type": "list", "elements": "int"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scans/remediation"

    payload_keys = ["uuid", "settings", "credentials", "enabled_plugins"]
    payload = build_payload(module, payload_keys)

    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
