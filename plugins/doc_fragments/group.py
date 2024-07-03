# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  group_id:
    description:
      - ID of the group.
      - Use the list_groups module to retrieve the groups in your organization.
      - Is you need the group_id of a scanner, use the list_scanner_groups module.
    required: true
    type: str
"""
