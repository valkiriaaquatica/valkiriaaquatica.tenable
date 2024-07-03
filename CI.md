# CI

## Tenable Nessus Agent Collections

GitHub Actions are used to run the Continuous Integration for valkiriaaquatica.tenable collection. The workflows used for the CI can be found in the /.github/workflow/ directory. These workflows include jobs to run the  integration tests, sanity tests, linters, check and doc related checks. The following table lists the python and ansible versions against which these jobs are run.

| Jobs | Description | Python Versions | Ansible Versions |
| ------ |-------| ------ | -----------|
| Linters | Runs 'black', 'flake8','isort','ansible-linter' on plugins and tests
| Unit tests | Executes the unit test cases | 3.9, 3.10, 3.11.0, 3.12.0 | Stable-2.15+ |
| Integration tests | Executes the integration test suites. To run them, it is necessary to adjust in the integration_config.yml file the credentials or if it is run on GitHub actions defined them as secret variables | 3.9, 3.10, 3.11.0, 3.12.0 | Stable-2.15+ |
