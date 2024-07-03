#!powershell
# (c) 2024, Fernando Mendieta (fernandomendietaovejero@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#AnsibleRequires -CSharpUtil Ansible.Basic
# Tested on PowerShell v5.1 and higher on Windows Server 2016 and higher;

#Requires -Module Ansible.ModuleUtils.Legacy

$spec = @{
    supports_check_mode = $false
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$nessuscliPath = 'C:\Program Files\Tenable\Nessus Agent\nessuscli.exe'
$arguments = "agent unlink"

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

    $module.Result['command_output'] = $stdout
    $module.Result['command_error'] = $stderr
    $module.Result['command'] = $arguments

    if ($stdout -like "*is not linked*") {
        $module.Result['changed'] = $false
        $module.Result['msg'] = "The agent is not linked, no changes are required."
    }
    elseif ($stdout -like "*Successfully unlinked*") {
        $module.Result['changed'] = $true
        $module.Result['msg'] = "Agent unlinked successfully."
    }
    else {
        $module.Result['changed'] = $false
        $module.FailJson("An unexpected error occurred during the unlink operation: $stdout")
    }
}
catch {
    $module.FailJson("Error unlinking the agent from Tenable: $_")
}

$module.ExitJson()

