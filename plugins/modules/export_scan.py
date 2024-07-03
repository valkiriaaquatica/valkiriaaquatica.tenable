# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: export_scan
short_description: Export the specified scan.
description:
  - This module exports a specified scan in Tenable using the scan ID and export options.
  - To see the status of the requested export, check_scan_export_status.
  - Requires SCAN OPERATOR [24] user permissions and CAN VIEW [16] scan permissions.
version_added: "0.0.1"
options:
  history_id:
    description:
      - The unique identifier of the historical data that you want Tenable Vulnerability Management to export.
      - This identifier corresponds to the history.id attribute of the response message from the get_scan_history module.
      - Note Unlike other export formats, the Nessus file format includes individual open port findings.
      - This ensures you can still view open port findings in Tenable Security Center if your organization integrates
        Tenable Vulnerability Management with Tenable Security Center.
      - Note If you request a scan export in the nessus file format, but do not specify filters
        for the export, Tenable Vulnerability Management truncates the plugins output data in
        the export file at 5 MB or 5,000,000 characters, and appends TRUNCATED (bracketed by
        three asterisks) at the end of the output in the export file. You can obtain the full
        plugins output by exporting the scan in any other file format than nessus.
      - Note Vulnerability findings with a first_observed date within the last 14 days are
        marked in the exported results as being in the New state. Vulnerability findings with a
        first_observed date older than 14 days are marked in the exported results as being in the Active state.
      - The module is made from https://developer.tenable.com/reference/scans-export-request  docs.
      - Requires SCAN OPERATOR [24] user permissions and CAN VIEW [16] scan permissions as specified
        in the Tenable.io API documentation.
    required: false
    type: str
  format:
    description:
      - The file format to use (Nessus, PDF, or CSV).
      - You can export scans in PDF format for up to 60 days. For scans that are older than 60 days,
        only the Nessus and CSV formats are supported.
      - Unlike other export formats, the Nessus file format includes individual open port findings.
      - This ensures you can still view open port findings in Tenable Security Center if your organization integrates
        Tenable Vulnerability Management with Tenable Security Center
    required: true
    type: str
    choices:
      - nessus
      - pdf
      - csv
  chapters:
    description:
      - The chapters to include in the export.
      - This parameter accepts a semi-colon delimited string comprised of some combination of the following options
        vuln_hosts_summary, vuln_by_host, compliance_exec, remediations, vuln_by_plugin, compliance).
      - Note This parameter is required for the PDF file format.
    required: false
    type: str
  filters:
    description:
      - The name of the filter to apply to the exported scan report.
      - You can find available filters by using the list_vulnerability_filters module.
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
  asset_id:
    description:
      - The ID of the asset scanned.
    required: false
    type: str
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan
  - valkiriaaquatica.tenable.filter_search_type
"""

EXAMPLES = r"""
- name: Export a scan with filters
  valkiriaaquatica.tenable.export_scan:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    scan_id: "1234"
    history_id: 54321
    format: "nessus"
    chapters: "1"
    filter_search_type: "and"
    filters:
      - property: "plugin.id"
        operator: "eq"
        value: 12345
    asset_id: "123456789"
  tags: export_scan
"""

RETURN = r"""
api_response:
  description: The full API response from Tenable.
  returned: success
  type: dict
  sample:
    status_code: 200
    data:
      uuid: "e122345"
"""

from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.api import TenableAPI
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.exceptions import TenableAPIError

from ansible.module_utils.basic import AnsibleModule


def build_export_scan_payload(params):
    payload = {
        "format": params.get("format"),
        "chapters": params.get("chapters"),
        "filter.search_type": params.get("filter_search_type"),
        "asset_id": params.get("asset_id"),
    }

    filters = params.get("filters")
    if filters:
        for idx, filter_ in enumerate(filters):
            prefix = f"filter.{idx}"
            payload[f"{prefix}.filter"] = filter_["property"]
            payload[f"{prefix}.quality"] = filter_["operator"]
            payload[f"{prefix}.value"] = filter_["value"]
    return payload


def main():
    common_spec = get_spec("access_key", "secret_key", "scan_id", "history_id", "filter_search_type")
    specific_spec = {
        "format": {"required": True, "type": "str", "choices": ["nessus", "pdf", "csv"]},
        "chapters": {"required": False, "type": "str"},
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
        "asset_id": {"required": False, "type": "str"},
    }
    argument_spec = {**common_spec, **specific_spec}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    scan_id = module.params["scan_id"]
    history_id = module.params.get("history_id")
    endpoint = f"scans/{scan_id}/export"
    if history_id:
        endpoint += f"?history_id={history_id}"

    payload = build_export_scan_payload(module.params)

    try:
        tenable_api = TenableAPI(module)
        response = tenable_api.request("POST", endpoint, data=payload)

        module.exit_json(changed=True, api_response=response)
    except TenableAPIError as e:
        module.fail_json(msg=str(e), status_code=getattr(e, "status_code", "Unknown"))


if __name__ == "__main__":
    main()
