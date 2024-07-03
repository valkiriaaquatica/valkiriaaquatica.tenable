# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: create_report
short_description: Creates a report in PDF format based on the specified template and filters.
version_added: "0.0.1"
description:
  - This module creates a report in PDF format based on the specified template and filters.
  - Note Tenable Vulnerability Management limits the number of findings that can be included in a single report to 10,000.
  - If you have more than 10,000 findings, Tenable recommends that you narrow the findings included in the report with a
    filter or generate multiple reports.
  - This module is made from https://developer.tenable.com/reference/vm-reports-create docs.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
options:
  name:
    description:
      - A name for the report. If omitted, a default name with a timestamp will be used.
    required: false
    type: str
  template_name:
    description:
      - The type of template to use for the report.
    required: true
    type: str
    choices:
      - host_vulns_summary
      - host_vulns_by_plugins
      - host_vulns_by_assets
  filters:
    description:
      - A set of filters to apply to the report. Filters can be used to narrow the vulnerabilities or assets included in the report.
    required: false
    type: list
    elements: dict
    suboptions:
      property:
        description:
          - The property to filter the results by.
        required: true
        type: str
      operator:
        description:
          - The comparison operator to apply to the filter. For example, eq, neq, gt, etc.
        required: true
        type: str
      value:
        description:
          - The value to compare the given property to using the specified operator.
        required: true
        type: raw
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""


EXAMPLES = r"""
- name: Create report with a plugin and enviroment vars
  create_report:
    name: "report_test"
    template_name: "host_vulns_summary"
    filters:
      - property: "plugin_id"
        operator: "eq"
        value: [12345]

- name: Create report using plugin.id and source filters
  create_report:
    name: "report_test"
    template_name: "host_vulns_summary"
    filters:
      - property: "plugin_id"
        operator: "eq"
        value: [12345]
      - property: "source"
        operator: "eq"
        value: ["AWS"]
"""

RETURN = r"""
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.parameter_actions import build_payload
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    common_spec = get_spec("access_key", "secret_key")
    specific_spec = {
        "name": {"required": False, "type": "str"},
        "template_name": {
            "required": True,
            "type": "str",
            "choices": ["host_vulns_summary", "host_vulns_by_plugins", "host_vulns_by_assets"],
        },
        "filters": {
            "required": False,
            "type": "list",
            "elements": "dict",
            "options": {
                "property": {"required": True, "type": "str"},
                "operator": {"required": True, "type": "str"},
                "value": {"required": True, "type": "raw"},
            },
        },
    }
    argument_spec = {**common_spec, **specific_spec}
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "reports/export"
    payload_keys = ["name", "template_name", "filters"]
    payload = build_payload(module, payload_keys)
    run_module(module, endpoint, method="POST", data=payload)


if __name__ == "__main__":
    main()
