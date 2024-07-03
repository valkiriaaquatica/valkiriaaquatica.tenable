# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_attributes
short_description: Returns a list of custom asset attributes.
version_added: "0.0.1"
description:
  - This module returns a list of custom asset attributes.
  - Requires BASIC [16] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/io-v3-asset-attributes-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all attributes in Tenable
  list_attributes:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
- name: List all attributes in Tenable using envirometn credentials
  list_attributes:
"""

RETURN = r"""
attributes:
  description: A list of custom asset attributes.
  returned: always
  type: list
  elements: dict
  contains:
    id:
      description: The unique identifier for the custom asset attribute.
      type: str
    name:
      description: The name of the custom asset attribute.
      type: str
    description:
      description: A description of the custom asset attribute.
      type: str
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = "api/v3/assets/attributes"
    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
