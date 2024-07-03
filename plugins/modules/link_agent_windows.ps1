#!powershell
# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic

#Requires -Module Ansible.ModuleUtils.Legacy

$spec = @{
    options = @{
        linking_key = @{ type = 'str'; required = $true; no_log = $true }
        name = @{ type = 'str'; required = $true }
        groups = @{ type = 'str'; required = $true }
        network = @{ type = 'str'; required = $true }
        host = @{ type = 'str'; required = $true }
        port = @{ type = 'int'; required = $true }
    }
    supports_check_mode = $false
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$linking_key = $module.Params.linking_key
$name = $module.Params.name
$groups = $module.Params.groups
$network = $module.Params.network
$tenable_host = $module.Params.host
$port = $module.Params.port

$nessuscliPath = 'C:\Program Files\Tenable\Nessus Agent\nessuscli.exe'
$arguments = "agent link --key=`"$linking_key`" --name=`"$name`" --groups=`"$groups`" --network=`"$network`" --host=$tenable_host --port=$port"

try {
    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = $nessuscliPath
    $processInfo.RedirectStandardError = $true
    $processInfo.RedirectStandardOutput = $true
    $processInfo.UseShellExecute = $false
    $processInfo.Arguments = $arguments
    $processInfo.CreateNoWindow = $true

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo
    $process.Start() | Out-Null
    $process.WaitForExit()

    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()

    $maskedArguments = $arguments -replace "--key=`"$linking_key`"", "--key=******"

    $module.Result['command_output'] = $stdout
    $module.Result['command_error'] = $stderr
    $module.Result['command'] = $maskedArguments

    if ($stdout -like "*Link fail*") {
        $module.Result['changed'] = $false
        $module.Result['failed'] = $true
        $module.Result['msg'] = "An error occurred executing the command: $stderr"
    }
    else {
        $module.Result['changed'] = $true
        $module.Result['msg'] = $stdout
    }
}
catch {
    $module.FailJson("Error linking the agent to Tenable.IO: $_")
}

$module.ExitJson()
