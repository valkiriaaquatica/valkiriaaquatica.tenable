# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  last_modification_date:
    description:
      - Limit the results to those scans that have run since the specified time.
      - This parameter does not represent the date on which the scan configuration was last modified.
      - Must be in Unix time format.
    required: false
    type: int
"""
