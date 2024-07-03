# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: list_templates
short_description: Lists Tenable-provided scan templates
version_added: "0.0.1"
description:
  - This module lists Tenable-provided scan templates
  - Tenable provides a number of scan templates to facilitate the creation of scans and scan policies.
  - The module is made from  https://developer.tenable.com/reference/editor-list-templates docs.
  - Requires STANDARD [32] user permissions as specified in the Tenable.io API documentation.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
extends_documentation_fragment:
  - valkiriaaquatica.tenable.credentials
  - valkiriaaquatica.tenable.scan_templates
"""

EXAMPLES = r"""
- name: List scan templates
  list_templates:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    type: "scan"

- name: List policy templates usnig enviroment creds
  list_templates:
    type: "policy"

- name: List remediation templates
  list_templates:
    access_key: "{{ tenable_access_key }}"
    secret_key: "{{ tenable_secret_key }}"
    type: "remediation"
"""

RETURN = r"""
api_response:
  description:  Detailed information about the response.
  type: dict
  returned: on success
  contains:
    data:
      description: Contains detailed information about the templates.
      type: dict
      contains:
        templates:
          description: A list of template details.
          type: list
          elements: dict
          contains:
            cloud_only:
              description: Indicates if the template is exclusively for cloud environments.
              type: bool
              returned: always
              sample: false
            desc:
              description: Description of the template.
              type: str
              returned: always
              sample: "desc"
            icon:
              description: Icon representation of the template.
              type: str
              returned: always
              sample: "P"
            is_agent:
              description: Specifies whether the template is meant for agent-based scans.
              type: bool
              returned: always
              sample: null
            is_was:
              description: Specifies whether the template is meant for web application scanning.
              type: bool
              returned: always
              sample: null
            manager_only:
              description: Indicates if the template is restricted to manager-level users only.
              type: bool
              returned: always
              sample: false
            name:
              description: Name of the template.
              type: str
              returned: always
              sample: "advanced"
            order:
              description: Display order of the template in listings.
              type: int
              returned: always
              sample: 2
            subscription_only:
              description: Indicates if the template is available only to subscribed users.
              type: bool
              returned: always
              sample: false
            title:
              description: Title of the template.
              type: str
              returned: always
              sample: "title"
            unsupported:
              description: Indicates if the template is unsupported.
              type: bool
              returned: always
              sample: false
            uuid:
              description: UUID of the template.
              type: str
              returned: always
              sample: "123456"
    status_code:
      description: HTTP status code returned by the API.
      type: int
      returned: always
      sample: 200
"""


from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.arguments import get_spec
from ansible_collections.valkiriaaquatica.tenable.plugins.module_utils.simple_requests import run_module

from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = get_spec("access_key", "secret_key", "type")
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if module.params["type"] == "scan":
        endpoint = "editor/scan/templates"
    if module.params["type"] == "policy":
        endpoint = "editor/policy/templates"
    if module.params["type"] == "remediation":
        endpoint = "editor/remediation/templates"

    run_module(module, endpoint, method="GET")


if __name__ == "__main__":
    main()
