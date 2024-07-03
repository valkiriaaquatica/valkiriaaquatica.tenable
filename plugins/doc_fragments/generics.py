# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  limit:
    description:
      - The number of records to retrieve.
      - Default is 50, minimum is 1, and maximum is 5000.
    type: int
    required: false
  offset:
    description:
      - The starting record to retrieve.
      - Default is 0.
    type: int
    required: false
  sort:
    description:
      - List of fields and order to sort the results.
      - Specify fields and order separated by a colon (asc or desc).
    type: str
    required: false
"""
