# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: list_aws_scan_targets
short_description: Retrieves the key of the requested scanner.
version_added: "0.0.1"
description:
  - This module retrieves the key of the requested scanner.
  - ists AWS scan targets if the requested scanner is an Amazon Web Services scanner.
  - The module is made from  https://developer.tenable.com/reference/scanners-get-aws-targets  docs.
  - Requires SCAN MANAGER [40] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scanner
"""

EXAMPLES = r"""
- name: List aws scan targets
  list_aws_scan_targets:
    access_key: "your_access_key"
    secret_key: "your_secret_key"
    scanner_id: 11111

- name: List aws scan targets using enviroment keys
  list_aws_scan_targets:
    scanner_id: 11111
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable API.
  type: dict
  returned: on success
  contains:
    object:
      description: The targets
      type: dict
      returned: on success
      sample:
        object: "aws-target"
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "scanner_id")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    endpoint = f"scanners/{module.params['scanner_id']}/aws-targets"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
