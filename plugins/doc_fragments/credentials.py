# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  access_key:
    description:
      - The access key required to authenticate with the Tenable.io API.
      - This key can be set as an environment variable named TENABLE_ACCESS_KEY or passed directly to the module.
    required: false
    type: str
  secret_key:
    description:
      - The secret key required to authenticate with the Tenable.io API.
      - This key can be set as an environment variable named TENABLE_SECRET_KEY or passed directly to the module.
    required: false
    type: str
"""
