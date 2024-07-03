# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  name:
    description:
      - The name of the network object.
      - Must be unique within your Tenable.io instance and cannot duplicate the name of a previously deleted network or be named 'default'.
    required: true
    type: str
  description:
    description:
      - The description of the network object.
    required: false
    type: str
  assets_ttl_days:
    description:
      - The number of days to wait before assets age out.
      - Assets will be permanently deleted if they are not seen on a scan within the specified number of days.
      - Minimum value 14
      - Maximum value 365
      - Warning Enabling this option will immediately delete assets in the specified network that have not been seen for the specified number of days.
      - All asset records and associated vulnerabilities are deleted and cannot be recovered. The deleted assets no longer count towards your license.
    required: false
    type: int
"""
