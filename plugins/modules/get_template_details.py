# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_template_details
short_description: Gets details for the specified template.
version_added: "0.0.1"
description:
  - Gets details for the specified template.
  - The module is made from  https://developer.tenable.com/reference/editor-template-details docs.
  - Requires STANDARD [32] user permissions as specified in the Tenable.io API documentation.
options:
  wizard_uuid:
    description:
      - The UUID for the template to get details from.
    required: true
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan_templates
"""

EXAMPLES = r"""
- name: Get scanner details
  get_template_details:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    type: "scan"
    wizard_uuid: "12345789"

- name: Get scanner details using enviroment keys
  get_template_details:
    scanner_id: 11111
    type: "remediation"
    wizard_uuid: "987654"
"""

RETURN = r"""
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "type", "wizard_uuid")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if module.params["type"] == "scan":
        endpoint = f"editor/scan/templates/{module.params['wizard_uuid']}"
    if module.params["type"] == "policy":
        endpoint = f"editor/policy/templates/{module.params['wizard_uuid']}"
    if module.params["type"] == "remediation":
        endpoint = f"editor/remediation/templates/{module.params['wizard_uuid']}"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
