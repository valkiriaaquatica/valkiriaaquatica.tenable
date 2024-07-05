# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: unlink_agent_linux
short_description: Unlink nessus agent from Linux server.
version_added: "0.0.1"
description:
  - This module unlinks the nessus agent relation that has a server with Tenable IO.
  - No macOS module yet.
author:
  - Fernando Mendieta Ovejero (@valkiriaaquatica)
"""


EXAMPLES = r"""
- name: Unlink the Nessus Agent on the target machine
  unlink_agent_linux:
  become: true
"""

RETURN = r"""
msg:
  description: Message about the result of the unlink operation.
  returned: on success
  type: str
  sample: "Nessus Agent unlinked successfully"
"""


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def unlink_nessus_agent(module):
    command = "/opt/nessus_agent/sbin/nessuscli agent unlink"
    rc, stdout, stderr = module.run_command(command, use_unsafe_shell=True)
    stdout = to_native(stdout)
    stderr = to_native(stderr)
    if rc != 0:
        module.fail_json(changed=False, stdout=stdout, stderr=stderr, rc=rc)
    return True, stdout, stderr, rc


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )

    is_unlinked, stdout, stderr, rc = unlink_nessus_agent(module)
    if is_unlinked:
        module.exit_json(changed=True, stdout=stdout, stderr=stderr, rc=rc)


if __name__ == "__main__":
    main()
