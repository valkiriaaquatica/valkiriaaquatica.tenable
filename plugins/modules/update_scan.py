# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_scan
short_description: Updates the scan configuration.
version_added: "0.0.1"
description:
  - This module updates the scan configuration.
  - For example, you can enable or disable a scan, change the scan name, description, folder,
    scanner, targets, and schedule parameters.
  - For more information and request body examples, see https://developer.tenable.com/docs/update-scan-tio
  - For information on updating remediation scans and request body examples, https://developer.tenable.com/docs/io-manage-remediation-scans
  - With SCAN OPERATOR [24] permissions, policy_id is required.
  - This module is made from https://developer.tenable.com/reference/scans-configure docs.
  - Requires SCAN OPERATOR [24] and CAN EDIT [64] scan permissions  user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
  - valkiriaaquatica.tenable.scan_configuration
  - valkiriaaquatica.tenable.scan_credentials
"""


EXAMPLES = r"""
- name: Create a scan with simple parameters, host_tagging and frequency scans
  update_scan:
    scan_id: 123456789
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    uuid: "{{ template_scan_uuid }}"
    host_tagging: "yes"
    refresh_reporting_frequency_scans: 2
    settings:
      name: "{{ name_scan_creation }}"
      agent_group_id: "{{ agent_group_id_created }}"

- name: Create a scan with settings and using enviroment creds
  update_scan:
    scan_id: 123456789
    uuid: "{{ template_scan_uuid }}"
    settings:
      name: "{{ name_scan_creation }}"
      folder_id: 111
      scanner_id: 123456
      launch: "ON_DEMAND"
      rrules: "WEEKLY"
      timezone: "Atlantic/Madeira"
      text_targets: "192.168.1.1,192.168.1.2"

- name: Create a scan with a file of targets and passing credentials as variables
  update_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: 123456789
    uuid: "{{ template_scan_uuid }}"
    settings:
      name: "name_scan"
      file_targets: scan_targets_file

- name: Create a scan configuring plugins and enviroment creds
  update_scan:
    scan_id: 123456789
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
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_complex_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec(
        "access_key", "secret_key", "scan_id", "uuid", "settings", "credentials", "plugin_configurations"
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}"
    payload = build_complex_payload(module.params)
    run_module(module, endpoint, method="PUT", data=payload)


if __name__ == "__main__":
    main()
