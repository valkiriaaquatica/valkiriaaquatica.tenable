# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  filters:
    description:
      - A list of filters to apply to the asset search. Each filter is a dictionary that includes 'type', 'operator', and 'value'.
      - For agent filters use the list_agent_filters module or check https://developer.tenable.com/reference/io-filters-agents-list .
      - For asset filters use the list_asset_filters module or check https://developer.tenable.com/reference/io-filters-assets-list .
      - For asset filters with filtering capabilities check https://developer.tenable.com/reference/io-filters-assets-list-v2 .
      - For credential filters use the list_credential_filters module or check https://developer.tenable.com/reference/io-filters-credentials-list .
      - For report filters use the list_report_filters module or check https://developer.tenable.com/reference/vm-filters-reports-list .
      - For scan filters use the list_scan_filters module or check https://developer.tenable.com/reference/io-filters-scan-list.
      - For scan history filters use list_scan_history_filters module or check https://developer.tenable.com/reference/io-filters-scan-history-list .
      - For vulnerability filters use list_vulnerability_filters module or
        check https://developer.tenable.com/reference/io-filters-vulnerabilities-workbench-list .
    type: list
    elements: dict
    required: false
    suboptions:
      type:
        description:
          - The type of filter to apply.
          - This is the host.id, name, uuid, plugin.attributes.bid all the name parameters returned.
        required: true
        type: str
      operator:
        description:
          - The operator for the filter.
          - Equal is eq.
          - Not equal is neq.
          - Match is match.
          - Not match  nmatch.
          - For date equal to, date-eq.
          - For date not equal to, date-neq.
          - For a date before , date-lt
          - For a date after, date-gt
          - To check if contains some value, set-has.
          - Opposite to To check if contains some value, set-hasnot
          - set-hasonly
          - For greatehr than, gt.
          - For less than, lt.
        required: true
        type: str
      value:
        description:
          - The specific value for the applied filter.
        required: true
        type: str
"""
