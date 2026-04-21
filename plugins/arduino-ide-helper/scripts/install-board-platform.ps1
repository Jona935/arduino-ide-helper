. "$PSScriptRoot\arduino-cli-common.ps1"

param(
    [Parameter(Mandatory = $true)]
    [string] $Platform
)

Write-Host "Actualizando indice de plataformas..."
Invoke-ArduinoCli -Arguments @("core", "update-index")

Write-Host "Instalando plataforma $Platform..."
Invoke-ArduinoCli -Arguments @("core", "install", $Platform)
Write-Host "Plataforma instalada correctamente."
