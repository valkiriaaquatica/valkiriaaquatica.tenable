# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# use in create_an_exclusion and update_an_exclusion

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  schedule:
    description:
      - The schedule parameters for the exclusion.
    type: dict
    suboptions:
      enabled:
        description:
          - If true, the exclusion schedule is active.
        type: bool
        required: false
      starttime:
        description:
          - The start time of the exclusion formatted as YYYY-MM-DD HH:MM:SS.
        type: str
        required: false
      endtime:
        description:
          - The end time of the exclusion formatted as YYYY-MM-DD HH:MM:SS.
        type: str
        required: false
      timezone:
        description:
          - The timezone for the exclusion as returned by scans timezones.
        type: str
        required: false
      rrules:
        description:
          - The recurrence rules for the exclusion.
        type: dict
        suboptions:
          freq:
            description:
              - The frequency of the rule (ONETIME, DAILY, WEEKLY, MONTHLY, YEARLY).
            type: str
            required: false
          interval:
            description:
              - The interval of the rule.
            type: int
            required: false
          byweekday:
            description:
              - A comma-separated string of days to repeat a WEEKLY frequency rule on.
            type: str
            required: false
          bymonthday:
            description:
              - The day of the month to repeat a MONTHLY frequency rule on.
            type: int
            required: false
"""
