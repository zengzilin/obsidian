<#
.SYNOPSIS
Checks TCP ports on a list of hosts and runs a docker restart command when any port is unreachable.

.DESCRIPTION
The script probes 10.21.104.13/14/15 on ports 9092 and 9200 by default.
If one or more ports fail on a host, the script runs one restart command for that host.

.EXAMPLE
.\check_ports_and_restart_docker.ps1 -DryRun

.EXAMPLE
.\check_ports_and_restart_docker.ps1 -RestartCommandTemplate 'ssh root@{ip} "sudo systemctl restart docker"'

.EXAMPLE
.\check_ports_and_restart_docker.ps1 -RestartCommandTemplate 'Invoke-Command -ComputerName {ip} -ScriptBlock { Restart-Service -Name docker -Force }'
#>

[CmdletBinding()]
param(
    [string[]]$TargetIps = @(
        '10.21.104.13',
        '10.21.104.14',
        '10.21.104.15'
    ),

    [int[]]$Ports = @(
        9092,
        9200
    ),

    [int]$ConnectTimeoutMs = 3000,

    [int]$RetryCount = 2,

    [int]$RetryIntervalSeconds = 2,

    [string]$RestartCommandTemplate = 'ssh root@{ip} "sudo systemctl restart docker"',

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Log {
    param(
        [string]$Level,
        [string]$Message
    )

    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$timestamp] [$Level] $Message"
}

function Test-TcpPort {
    param(
        [string]$Ip,
        [int]$Port,
        [int]$TimeoutMs
    )

    $client = [System.Net.Sockets.TcpClient]::new()
    $connectAsync = $null

    try {
        $connectAsync = $client.BeginConnect($Ip, $Port, $null, $null)
        if (-not $connectAsync.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {
            return $false
        }

        $null = $client.EndConnect($connectAsync)
        return $true
    } catch {
        return $false
    } finally {
        if ($connectAsync -and $connectAsync.AsyncWaitHandle) {
            $connectAsync.AsyncWaitHandle.Close()
        }
        $client.Close()
        $client.Dispose()
    }
}

function Invoke-RestartCommand {
    param(
        [string]$Ip,
        [int[]]$FailedPorts,
        [string]$CommandTemplate,
        [switch]$IsDryRun
    )

    $failedPortText = $FailedPorts -join ','
    $command = $CommandTemplate.Replace('{ip}', $Ip).Replace('{ports}', $failedPortText)

    if ($IsDryRun) {
        Write-Log 'WARN' "DryRun enabled. Would execute for $Ip: $command"
        return
    }

    Write-Log 'WARN' "Executing restart command for $Ip because ports [$failedPortText] are unreachable."
    Invoke-Expression $command
    Write-Log 'INFO' "Restart command finished for $Ip."
}

$restartTriggered = 0
$restartFailed = $false

Write-Log 'INFO' "Starting port check. Targets: $($TargetIps -join ', ') | Ports: $($Ports -join ', ')"

foreach ($ip in $TargetIps) {
    $failedPorts = New-Object System.Collections.Generic.List[int]

    foreach ($port in $Ports) {
        $isReachable = $false

        for ($attempt = 1; $attempt -le $RetryCount; $attempt++) {
            if (Test-TcpPort -Ip $ip -Port $port -TimeoutMs $ConnectTimeoutMs) {
                $isReachable = $true
                break
            }

            if ($attempt -lt $RetryCount) {
                Start-Sleep -Seconds $RetryIntervalSeconds
            }
        }

        if ($isReachable) {
            Write-Log 'INFO' "$ip:$port is reachable."
        } else {
            Write-Log 'ERROR' "$ip:$port is unreachable after $RetryCount attempt(s)."
            $failedPorts.Add($port)
        }
    }

    if ($failedPorts.Count -gt 0) {
        $restartTriggered++

        try {
            Invoke-RestartCommand -Ip $ip -FailedPorts $failedPorts.ToArray() -CommandTemplate $RestartCommandTemplate -IsDryRun:$DryRun
        } catch {
            $restartFailed = $true
            Write-Log 'ERROR' "Restart command failed for $ip. $($_.Exception.Message)"
        }
    } else {
        Write-Log 'INFO' "All monitored ports are healthy on $ip."
    }
}

if ($restartFailed) {
    Write-Log 'ERROR' 'Completed with restart command failures.'
    exit 2
}

if ($restartTriggered -gt 0) {
    Write-Log 'WARN' "Completed with $restartTriggered host(s) requiring restart handling."
    exit 1
}

Write-Log 'INFO' 'Completed successfully. All monitored ports are healthy.'
exit 0
