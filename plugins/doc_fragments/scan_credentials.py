# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  credentials:
    description:
      - Credentials object that specifies parameters for the scan.
    required: false
    type: dict
    suboptions:
      add:
        description:
          - A credentials object to add to the scan.
        required: false
        type: dict
        suboptions:
          Host:
            description:
              - Host credentials.
            required: false
            type: dict
            suboptions:
              Windows:
                description:
                  - Windows credentials.
                required: false
                type: list
                elements: dict
                suboptions:
                  domain:
                    description:
                      - The Windows domain to which the username belongs.
                    required: false
                    type: str
                  username:
                    description:
                      - The username on the target system.
                    required: false
                    type: str
                  auth_method:
                    description:
                      - The name for the authentication method.
                    required: false
                    type: str
                  password:
                    description:
                      - The user password on the target system.
                    required: false
                    type: str
"""
