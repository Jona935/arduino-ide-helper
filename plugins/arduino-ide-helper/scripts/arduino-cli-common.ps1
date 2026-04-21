Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ArduinoCli {
    if ($env:ARDUINO_CLI_PATH -and (Test-Path -LiteralPath $env:ARDUINO_CLI_PATH)) {
        return $env:ARDUINO_CLI_PATH
    }

    $command = Get-Command arduino-cli -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"),
        (Join-Path $env:ProgramFiles "Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"),
        (Join-Path $env:ProgramFiles(x86) "Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe")
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

    if ($candidates.Count -gt 0) {
        return $candidates[0]
    }

    throw "No encontre arduino-cli. Instala Arduino CLI o Arduino IDE 2.x, o define ARDUINO_CLI_PATH."
}

function Invoke-ArduinoCli {
    param(
        [Parameter(Mandatory = $true)]
        [string[]] $Arguments
    )

    $cliPath = Resolve-ArduinoCli
    & $cliPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "arduino-cli fallo con codigo $LASTEXITCODE."
    }
}
