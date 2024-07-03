# Contributing

## Tenable Nessus Agent Collection


### valkiriaaquatica.tenable
Contains most of the interactions that can be donde with Tenable.IO API usefull for the nessus agent.


## Submitting Issues

For any new module idea, code review, change or whatever please pr on this repository on a new patch branch.
Also any issue can be open to improve, delete, change or any idea sbmitted on any part of the collection.

## Writing New Code and Testing (recommended but not mandatory)

Please follow the Ansible Documentation on [these instructions](https://docs.ansible.com/ansible/latest/community/create_pr_quick_start.html) 
for developing the new code for the collection.
Also any Documentation can be change or improve.

It is recommended to execute this on a python virtual enviroment.
1. Create the virtual enviroment (recommended)
```
python3 -m venv env
```
2. Install testing requirements
```
pip install -r test-requirements.txt
```
3. Write your code and your tests (recommended but not mandatory)

- Sanity tests:
```
ansible-test sanity --docker -v
```

- Unit tests:
```
ansible-test unit --docker -v
```

- Integration tests:
```
ansible-test integration name_of_the_test_module --docker -v
```

If you get stuck with any of this tests, when the PR is sbmitted it will automatically test for sanity and unit tests.

## Check for pending Tests to be done 
In the collection directory there is the check_pending_tests.sh file.
Follow this steps to output the pending and done tests.
```
chmod +x check_pending_tests.sh
```

```
./check_pending_tests.sh
```

## Blessed Contributions on Pending Developments
- Add macOS integration for modules: download_nessus_agent, future not made link_agent_macos
- Tests: not all modules have integration tests written, feel free to try.
- Not all plugins/modules have the RETURN specified, feel free to complete.
- Docs: there are nod docs written for reading the collection outside GitHub, feel free to help documenting.
- Recheck CI: i'm working on a recheck option to actual execute all_green CI when a recheck or RECHECK is written on a pull request.
  (As a Jenkins user GitHub actions is a bit new for me)
- Help a shared library for Jenkins to implement the actual GitHub actions like sanity, units or linter but with Jenkins.
- Folder with roles or playbook examples integrating differente modules to solve real daily problems like patching, inventory, vulnerability detection, scanning.
- AWX / AAP examples with inventories creating constructed and smart inventories mixing with other inventoies like cloud or service now.. to make bigger and more powerfull inventories.

## More information about contributing

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).


For general information on running the integration tests see
[this page](https://docs.ansible.com/ansible/latest/community/collection_contributors/test_index.html) and
[Integration Tests page of the Module Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/testing_integration.html#non-destructive-tests).
Ignore the part about `source hacking/env-setup`. That's only applicable for working on `ansible-core`.
You should be able to use the `ansible-test` that's installed with Ansible generally.
Look at [the section on configuration for cloud tests](https://docs.ansible.com/ansible/devel/dev_guide/testing_integration.html#other-configuration-for-cloud-tests).

- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly



### Communication
At the moment there is no communication channel, I'm sorry for that :(
