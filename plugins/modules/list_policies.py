# (c) 2024, @valkiriaaquatica (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_policies
short_description: Returns a list of policies (scan templates).
version_added: "0.0.1"
description:
  - This module returns a list of policies (scan templates).
  - Note Policies are referred to as scan templates in the new interface
  -  The term policy is only used in the classic interface.
  - Requires STANDARD [32] user permissions as specified in the Tenable.io API documentation.
  - Module made from https://developer.tenable.com/reference/policies-list docs.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
"""

EXAMPLES = r"""
- name: List all policies in Tenable
  list_policies:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
- name: List all policies in Tenable using envirometn credentials
  list_policies:
"""

RETURN = r"""

"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = "policies"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
