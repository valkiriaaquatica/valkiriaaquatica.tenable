# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: resume_scan
short_description: Resumes a scan.
version_added: "0.0.1"
description:
  - This module resumes a scan.
  - You can only resume a scan that has a status of paused.
  - The module is made from https://developer.tenable.com/reference/scans-resume docs.
  - Requires SCAN OPERATOR [24] and CAN EXECUTE [32] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
"""

EXAMPLES = r"""
- name: Resumes a scan using enviroment creds
  resume_scan:
    scan_id: "123456"

- name: Resumes a scan
  resume_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "123456"
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scan_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"scans/{module.params['scan_id']}/resume"

    run_module(module, endpoint, method="POST")


if __name__ == "__main__":
    main()
