# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: delete_managed_credential
short_description: Deletes the specified managed credential object.
version_added: "0.0.1"
description:
  - This module deletes the specified managed credential object.
  - When you delete a managed credential object, Tenable Vulnerability Management also
    removes the credential from any scan that uses the credential.
  - The module is made from https://developer.tenable.com/reference/credentials-delete  docs.
  - Requires  CAN EDIT [64] credential permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.credential
"""

EXAMPLES = r"""
- name: Deletes a manage credential using enviroment creds
  delete_managed_credential:
    credential_uuid: 12346

- name: Deletes a manage credential passing creds as vars
  delete_managed_credential:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    credential_uuid: 12346
"""

RETURN = r"""
api_response:
  description: Response returned by the Tenable api.
  returned: always when a request is made, independent if it correct or incorrect.
  type: complex
  contains:
    status_code:
      description: The HTTP status code returned by the API if an error occurred.
      type: int
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "credential_uuid")

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    endpoint = f"credentials/{module.params['credential_uuid']}"

    run_module(module, endpoint, method="DELETE")


if __name__ == "__main__":
    main()
