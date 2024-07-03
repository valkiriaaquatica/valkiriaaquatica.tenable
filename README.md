# First of All :)
- This is not developed from a Tenable or RedHat employee, just someone who in his daily work found the necessity to develop it to improve his daily tasks in system administration, devops and security and his teams work also.
- This collection is very usefull for applying quick responses to vulnerbailities, applied devops metodology quickly with secure pipelines and administrate machines that have nessus agent installed.
- That's why maybe you found errors or not "common standard Ansible" ideas, but I tried to follow them :).
- Writing documentation is not my best sorry.
- Testing has been made in Jenkins  and in GitHub actions, so if someone wants to help developing Jenkins shared libraries to  include in pipelines I will be happy.

# Ansible collection for Tenable Nessus Agent
[![Doc](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ansible.com/ansible/latest/collections/azure/azcollection/index.html)
[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

This collection provides a series of Ansible modules and plugins for interact with the Tenable Nessus Agent API.

https://developer.tenable.com/reference/navigate and installation and linking modules.

Documentation of individual modules is yet not available as ansible-galaxy official collection.

## Installation

It is recommended to run ansible in [Virtualenv](https://virtualenv.pypa.io/en/latest/).

To install it from Ansible-Galaxy. First Way.
```bash
ansible-galaxy collection install valkiriaaquatica.tenable
```

Install dependencies required by the collection (adjust path to collection if necessary):

```bash
pip3 install -r ~/.ansible/collections/ansible_collections/valkiriaaquatica/tenable/requirements.txt
```

To install it from source code of this GitHub repository. Second way.

```bash
https://github.com/valkiriaaquatica/valkiriaaquatica.tenable_dev.git
```
Then on the root directory of the collection.
```bash
ansible-galaxy collection build
```
Then after the valkiriaaquatica.tenable-{version}.tar.gz is created install it.
```bash
ansible-galaxy collection install valkiriaaquatica.tenable-{version}.tar.gz
```

## Requirements

- ansible version >= 2.14
- Install python dependancies of the requirements.txt file.


### Playbooks

To use a module from Tenable collection, please reference the full namespace, collection name, and modules name that you want to use:

```yaml
---
- name: Using Tenable collection
  hosts: localhost
  tasks:
    - valkiriaaquatica.tenable.list_assets:
        access_key: "your_access_key"
        secret_key: "your_secret_key"
        filters:
          - type: network_id
            operator: eq
            value: "123456789"
```


### Roles

For existing Ansible roles, please also reference the full namespace, collection name, and modules name which used in tasks instead of just modules name.

### Plugins like Inventory

To use a plugin from Tenable collection, please reference the full namespace, collection name, and plugins name that you want to use:

```yaml
---
plugin: valkiriaaquatica.tenable.tenable
full_info: true
include_filters:
  - type: "tag.Cloud Provider"
    operator: set-has
    value: "Google Cloud"
compose:
  asset_id_host: "'asset' + id"
  hash_id: id | md5
```

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, improvements or issues.
- Review source code changes.
- Review the documentation and make pull requests for anything from typos to new content
- If you are interested in fixing issues and contributing directly to the code base, please see the [CONTRIBUTING](CONTRIBUTING.md) document
- Check "Blessed Contributions on Pending Developments" in the file [CONTRIBUTING](CONTRIBUTING.md) to see ideas to help dn develop

## License

GNU General Public License v3.0

See [LICENSE](LICENSE) to see the full text.



# Just for own development issues
ansible-test integration --exclude add_agent_to_group --exclude create_report --exclude get_agent_details  --exclude get_asset_activity_log   --exclude get_asset_information  --exclude get_asset_vulnerability_details  --exclude get_report_status   --exclude list_agents_by_group  --exclude list_asset_vulnerabilities  --exclude list_asset_vulnerabilities_for_plugin  --exclude list_tags_for_an_asset  --exclude rename_agent  --exclude update_agent_group_name  --exclude upload_file  --exclude get_scanner_details --exclude launch_scan --exclude list_agents --exclude stop_scan --exclude update_scan --exclude add_or_remove_asset_tags --exclude get_asset_details --exclude create_network --exclude delete_network  --exclude get_network_details --exclude list_networks  --exclude update_network --exclude list_assignable_scanners  --exclude move_assets  --docker -v 
