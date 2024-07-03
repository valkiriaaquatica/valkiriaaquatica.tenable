# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: create_scan
short_description: Creates a scan configuration.
version_added: "0.0.1"
description:
  - This module creates a scan configuration.
  - For more information on the scan visit https://developer.tenable.com/docs/create-scan-tio.
  - Note Tenable Vulnerability Management limits the number of scans you can create to 10,000 scans.
  - Tenable recommends you re-use scheduled scans instead of creating new scans.
  - An HTTP 403 error is returned if you attempt to create a scan after you have already reached the scan limit of 10,000.
  - With SCAN OPERATOR [24] permissions, policy_id is required.
  - This module is made from https://developer.tenable.com/reference/scans-create  docs.
  - Requires SCAN OPERATOR [24] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan_configuration
  - valkiriaaquatica.tenable.scan_credentials
"""


EXAMPLES = r"""
- name: Create a scan with simple parameters, host_tagging and frequency scans
  create_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    uuid: "{{ template_scan_uuid }}"
    host_tagging: "yes"
    refresh_reporting_frequency_scans: 2
    settings:
      name: "{{ name_scan_creation }}"
      agent_group_id: "{{ agent_group_id_created }}"

- name: Create a scan with settings and using enviroment creds
  create_scan:
    uuid: "{{ template_scan_uuid }}"
    settings:
      name: "{{ name_scan_creation }}"
      folder_id: 111
      scanner_id: 123456
      launch: "ON_DEMAND"
      rrules: "WEEKLY"
      timezone: "Atlantic/Madeira"
      text_targets: "192.168.1.1,192.168.1.2"

- name: Create a scan with a file of targets and passing credentials as variables and adding credentials
  create_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    uuid: "{{ template_scan_uuid }}"
    settings:
      name: "name_scan"
      file_targets: scan_targets_file
    credentials:
      add:
        Host:
          Windows:
            - domain: "domain"
              username: "username"
              auth_method: "Password"
              password: "password"


- name: Create a scan configuring plugins and enviroment creds
  create_scan:
    uuid: "123456789"
    settings:
      name: "name"
      policy_id: 12345
    plugin_configurations:
      - plugin_family_name: "Red Hat Local Security Checks"
        plugins:
          - plugin_id: "79798"
            status: "enabled"
          - plugin_id: "79799"
            status: "disabled"
"""

RETURN = r"""
api_response:
  description: Detailed information about the response related to a scan configuration or outcome.
  type: dict
  returned: always
  contains:
    data:
      description: Contains all relevant details about the scan.
      type: dict
      contains:
        scan:
          description: Details of the specific scan.
          type: dict
          contains:
            agent_scan_launch_type:
              description: Launch type of the scan, e.g., manual or scheduled.
              type: str
              returned: always
              sample: "scheduled"
            auto_routed:
              description: Indicates if the scan was automatically routed.
              type: int
              returned: always
              sample: 0
            baseline_next_scan:
              description: Indicates the next baseline scan if applicable.
              type: str
              returned: when applicable
              sample: null
            container_id:
              description: Identifier of the container where the scan was configured.
              type: str
              returned: always
              sample: "123456789"
            creation_date:
              description: UNIX timestamp when the scan was created.
              type: int
              returned: always
              sample: 123456789
            custom_targets:
              description: Custom targets specified for the scan.
              type: str
              returned: always
              sample: "123456789"
            default_permissions:
              description: Default permissions applied to the scan.
              type: int
              returned: always
              sample: 0
            description:
              description: Description of the scan.
              type: str
              returned: when applicable
              sample: null
            emails:
              description: Emails associated with notifications for the scan.
              type: str
              returned: when applicable
              sample: null
            enabled:
              description: Indicates whether the scan is enabled.
              type: bool
              returned: always
              sample: false
            id:
              description: Unique identifier of the scan.
              type: int
              returned: always
              sample: 2203
            include_aggregate:
              description: Indicates if aggregate data is included in the scan results.
              type: bool
              returned: always
              sample: true
            interval_type:
              description: Type of interval for recurring scans.
              type: str
              returned: when applicable
              sample: null
            interval_value:
              description: Value of the interval for recurring scans.
              type: str
              returned: when applicable
              sample: null
            last_modification_date:
              description: UNIX timestamp when the scan was last modified.
              type: int
              returned: always
              sample: 123456789
            name:
              description: Name of the scan.
              type: str
              returned: always
              sample: "123456789"
            notification_filters:
              description: Filters applied to notifications for the scan.
              type: str
              returned: when applicable
              sample: null
            owner:
              description: Email of the owner of the scan.
              type: str
              returned: always
              sample: "autobit@nttdata.com"
            owner_id:
              description: User ID of the scan owner.
              type: int
              returned: always
              sample: 2308677
            owner_uuid:
              description: UUID of the scan owner.
              type: str
              returned: always
              sample: "123456789"
            policy_id:
              description: Identifier of the policy applied to the scan.
              type: int
              returned: always
              sample: 2202
            remediation:
              description: Indicates if remediation is enabled for the scan.
              type: int
              returned: always
              sample: 0
            reporting_mode:
              description: Reporting mode for the scan.
              type: str
              returned: when applicable
              sample: null
            rrules:
              description: Recurrence rules for scheduled scans.
              type: str
              returned: when applicable
              sample: null
            scan_time_window:
              description: Time window for the scan.
              type: int
              returned: always
              sample: 123456789
            scanner_id:
              description: Identifier of the scanner used.
              type: str
              returned: when applicable
              sample: null
            scanner_uuid:
              description: UUID of the scanner used.
              type: str
              returned: always
              sample: "123456789"
            shared:
              description: Indicates if the scan is shared with other users.
              type: int
              returned: always
              sample: 0
            sms:
              description: SMS notifications for the scan.
              type: str
              returned: always
              sample: ""
            starttime:
              description: Start time for the scan.
              type: str
              returned: when applicable
              sample: null
            tag_type:
              description: Type of tags associated with the scan.
              type: str
              returned: when applicable
              sample: null
            target_network_uuid:
              description: UUID of the network targeted by the scan.
              type: str
              returned: when applicable
              sample: null
            timezone:
              description: Timezone in which the scan is scheduled.
              type: str
              returned: when applicable
              sample: null
            triggers:
              description: Triggers that initiate the scan.
              type: str
              returned: when applicable
              sample: null
            type:
              description: Type of scan, e.g., public or private.
              type: str
              returned: always
              sample: "public"
            user_permissions:
              description: Permissions of the user on the scan.
              type: int
              returned: always
              sample: 128
            uuid:
              description: UUID of the scan.
              type: str
              returned: always
              sample: "template-123456789"
            version:
              description: Version number of the scan setup.
              type: int
              returned: always
              sample: 1
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_complex_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "uuid", "settings", "credentials", "plugin_configurations")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "scans"
    payload = build_complex_payload(module.params)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
