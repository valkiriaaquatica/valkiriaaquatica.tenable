# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  scan_id:
    description:
      - The unique identifier of the scan.
      - The name starts with 'template-...'.
      - This identifier can be either the scans.schedule_uuid or the scans.id using list_scans module.
      - Tenable recommends that you use scans.schedule_uuid.
    required: true
    type: str
"""
