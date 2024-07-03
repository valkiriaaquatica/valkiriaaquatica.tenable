// this file when collection is public made will not be present. tis is also a PR test
// this needs to integrate shared libraries because pipeline takes soooo many time
pipeline {
    agent none
    stages {
        stage('Matrix Build') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.9.0', '3.10.0', '3.11.0', '3.12.0'
                    }
                    axis {
                        name 'ANSIBLE_VERSION'
                        values 'stable-2.15', 'stable-2.16', 'stable-2.17', 'devel', 'milestone'
                    }
                }
                stages {
                    stage('Check Exclusions and Setup Environment') {
                        agent {
                            docker {
                                image 'fermendy/tenable_dependencias:latest'
                                args '-u root:root'
                            }
                        }
                        environment {
                            EXCLUSIONS = "3.9.0:stable-2.16,3.9.0:stable-2.17,3.9.0:devel,3.9.0:milestone,3.12.0:stable-2.15,3.12.0:milestone"
                        }
                        stages {
                            stage('Check Exclusions') {
                                steps {
                                    script {
                                        def exclusions = EXCLUSIONS.split(",").collect { it.trim() }
                                        def currentCombination = "${PYTHON_VERSION}:${ANSIBLE_VERSION}"
                                        echo "Verifying exclusion for combination: ${currentCombination}"
                                        if (exclusions.any { it == currentCombination }) {
                                            echo "Skipping detected not posible combination: Python ${PYTHON_VERSION} y Ansible ${ANSIBLE_VERSION}"
                                            error "Exclusion detected. Stopping the build for this combination."
                                        }
                                    }
                                }
                            }
                            stage('Setup Environment') {
                                steps {
                                    echo "Setting up environment for Python ${PYTHON_VERSION} and Ansible ${ANSIBLE_VERSION}"
                                }
                            }
                            stage('Clean Previous Builds') {
                                steps {
                                    sh '''
                                    find ${WORKSPACE} -name 'valkiriaaquatica-tenable-*.tar.gz' -exec rm {} \\; || true
                                    find ${WORKSPACE} -name 'venv_*' -exec rm -rf {} \\; || true
                                    '''
                                }
                            }
                            stage('Clean Workspace and Checkout') {
                                steps {
                                    sh 'rm -rf *'
                                    checkout scm
                                    sh 'ls -la'
                                }
                            }
                            stage('Install System Dependencies and Pyenv') {
                                steps {
                                    script {
                                        installPyenv("${PYTHON_VERSION}")
                                    }
                                }
                            }
                            stage('Setup Ansible and Virtualenv') {
                                steps {
                                    script {
                                        setupAnsibleEnv("${PYTHON_VERSION}", "${ANSIBLE_VERSION}")
                                    }
                                }
                            }
                            stage('Extract Galaxy Metadata') {
                                steps {
                                    script {
                                        extractGalaxyMetadata()
                                    }
                                }
                            }
                            stage('Build and Install Collection') {
                                steps {
                                    script {
                                        buildAndInstallCollection("${PYTHON_VERSION}", "${ANSIBLE_VERSION}")
                                    }
                                }
                            }
                            stage('Run Tox Ansible-Lint Testing') {
                                steps {
                                    script {
                                        runToxTesting("${PYTHON_VERSION}", "${ANSIBLE_VERSION}")
                                    }
                                }
                            }
                            stage('Run Ansible Sanity Test') {
                                steps {
                                    script {
                                        runAnsibleSanityTest("${PYTHON_VERSION}")
                                    }
                                }
                            }
                            stage('Run Ansible Unit Tests') {
                                steps {
                                    script {
                                        runAnsibleUnitTest("${PYTHON_VERSION}")
                                    }
                                }
                                post {
                                    always {
                                        junit 'results.xml'
                                    }
                                }
                            }
                            stage('Run Ansible Integration Test') {
                                steps {
                                    script {
                                        runAnsibleIntegrationTest("${PYTHON_VERSION}")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWorkspace()
        }
    }
}

def installPyenv(pythonVersion) {
    sh """
    curl https://pyenv.run | bash
    echo 'export PYENV_ROOT="\$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="\$PYENV_ROOT/bin:\$PATH"' >> ~/.bashrc
    echo 'eval "\$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "\$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "\$(pyenv virtualenv-init -)"' >> ~/.bashrc
    export PYENV_ROOT="\$HOME/.pyenv"
    export PATH="\$PYENV_ROOT/bin:\$PATH"
    eval "\$(pyenv init --path)"
    eval "\$(pyenv init -)"
    eval "\$(pyenv virtualenv-init -)"
    pyenv install -s ${pythonVersion}
    pyenv global ${pythonVersion}
    python -m pip install --upgrade pip
    python --version
    """
}

def setupAnsibleEnv(pythonVersion, ansibleVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${ansibleVersion.replace('.', '_')}"
    sh """
    export PYENV_ROOT="/root/.pyenv"
    export PATH="\$PYENV_ROOT/bin:\$PATH"
    eval "\$(pyenv init --path)"
    eval "\$(pyenv init -)"
    eval "\$(pyenv virtualenv-init -)"
    pyenv global ${pythonVersion}
    python -m venv ${venvName}
    . ${venvName}/bin/activate
    python -m pip install https://github.com/ansible/ansible/archive/${ansibleVersion}.tar.gz
    pip install -r test-requirements.txt
    apt-get install jq -y
    pip install yq
    """
}


def extractGalaxyMetadata() {
    def venvName = "/tmp/venv_${env.PYTHON_VERSION}_${env.ANSIBLE_VERSION.replace('.', '_')}"
    def envVars = sh(script: """
    . ${venvName}/bin/activate
    NAMESPACE=\$(yq -r '.namespace' galaxy.yml)
    COLLECTION_NAME=\$(yq -r '.name' galaxy.yml)
    VERSION=\$(yq -r '.version' galaxy.yml)
    echo "NAMESPACE=\$NAMESPACE"
    echo "COLLECTION_NAME=\$COLLECTION_NAME"
    echo "VERSION=\$VERSION"
    echo "NAMESPACE=\$NAMESPACE" > \$WORKSPACE/metadata.env
    echo "COLLECTION_NAME=\$COLLECTION_NAME" >> \$WORKSPACE/metadata.env
    echo "VERSION=\$VERSION" >> \$WORKSPACE/metadata.env
    cat \$WORKSPACE/metadata.env
    """, returnStdout: true).trim()

    def props = readFile("${env.WORKSPACE}/metadata.env").split('\n')
    env.NAMESPACE = props[0].split('=')[1].trim()
    env.COLLECTION_NAME = props[1].split('=')[1].trim()
    env.VERSION = props[2].split('=')[1].trim()

    echo "NAMESPACE=${env.NAMESPACE}"
    echo "COLLECTION_NAME=${env.COLLECTION_NAME}"
    echo "VERSION=${env.VERSION}"
}

def buildAndInstallCollection(pythonVersion, ansibleVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${ansibleVersion.replace('.', '_')}"
    def tarFileName = "${env.NAMESPACE}-${env.COLLECTION_NAME}-${env.VERSION}.tar.gz"
    sh """
    export PYENV_ROOT="\$HOME/.pyenv"
    export PATH="\$PYENV_ROOT/bin:\$PATH"
    eval "\$(pyenv init --path)"
    eval "\$(pyenv init -)"
    eval "\$(pyenv virtualenv-init -)"
    pyenv global ${pythonVersion}
    . ${venvName}/bin/activate
    ansible-galaxy collection build -vvv 
    tar -tzf ${tarFileName}
    ansible-galaxy collection install ${tarFileName} -vvv
    cp galaxy.yml /root/.ansible/collections/ansible_collections/valkiriaaquatica/tenable/galaxy.yml
    """
}


def runToxTesting(pythonVersion, ansibleVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${ansibleVersion.replace('.', '_')}"
    sh """
    . ${venvName}/bin/activate
    cd /root/.ansible/collections/ansible_collections/valkiriaaquatica/tenable/
    rm -rf MANIFEST.json
    ls -la
    tox  -m lint -vv --skip-missing-interpreters=false
    rm -rf .tox
    """
}

def runAnsibleSanityTest(pythonVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${env.ANSIBLE_VERSION.replace('.', '_')}"
    def shortPythonVersion = pythonVersion.replaceAll(/\\.\\d+$/, '')
    sh """
    . ${venvName}/bin/activateS
    echo "Using Python version: ${shortPythonVersion}"
    cd /root/.ansible/collections/ansible_collections/valkiriaaquatica/tenable/
    ls -la
    ansible-test sanity --requirements --color --python default
    """
}

def runAnsibleUnitTest(pythonVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${env.ANSIBLE_VERSION.replace('.', '_')}"
    sh """
    . ${venvName}/bin/activate
    ls -la
    python -m pytest tests/unit --junitxml=results.xml --showlocals
    """
}

def runAnsibleIntegrationTest(pythonVersion) {
    def venvName = "/tmp/venv_${pythonVersion}_${env.ANSIBLE_VERSION.replace('.', '_')}"
    def excludeList = [
        "add_agent_to_group/",
        "create_report/",
        "get_agent_details/",
        "get_asset_activity_log/",
        "get_asset_information/",
        "get_asset_vulnerability_details/",
        "get_report_status/",
        "list_agents_by_group/",
        "list_asset_vulnerabilities/",
        "list_asset_vulnerabilities_for_plugin/",
        "list_tags_for_an_asset/",
        "rename_agent/",
        "update_agent_group_name/",
        "upload_file/",
        "get_scanner_details/",
        "launch_scan/",
        "list_agents/",
        "stop_scan/",
        "update_scan/",
        "add_or_remove_asset_tags/",
        "get_asset_details/",
        "create_network/",
        "delete_network/",
        "get_network_asset_count/",
        "get_network_details/",
        "list_networks/",
        "list_network_scanners/",
        "list_assignable_scanners",
        "update_network/",
    ]
    def excludeArgs = excludeList.collect { "--exclude ${it}" }.join(" ")
    sh """
    . ${venvName}/bin/activate
    cd tests/integration/
    ls -la
    cat <<EOF > integration_config.yml
    tenable_access_key: ${env.TENABLE_ACCESS_KEY}
    tenable_secret_key: ${env.TENABLE_SECRET_KEY}
    EOF
    ls -la
    cd ../../..
    ls -la
    ansible-test integration ${excludeArgs} -v
    """
}
 //ansible-test integration ${excludeArgs}

def cleanWorkspace() {
    node('master_node') {
        cleanWs()
        sh '''
        find ${WORKSPACE} -name '*.tar.gz' -exec rm {} \\;
        find ${WORKSPACE} -name 'venv_*' -exec rm -rf {} \\;
        '''
    }
}
