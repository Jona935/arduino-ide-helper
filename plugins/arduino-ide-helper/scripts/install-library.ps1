. "$PSScriptRoot\arduino-cli-common.ps1"

param(
    [Parameter(Mandatory = $true)]
    [string] $LibraryName,
    [string] $Version
)

Write-Host "Actualizando indice de librerias..."
Invoke-ArduinoCli -Arguments @("lib", "update-index")

$arguments = @("lib", "install", $LibraryName)
if ($Version) {
    $arguments += @("--version", $Version)
}

Write-Host "Instalando libreria $LibraryName..."
Invoke-ArduinoCli -Arguments $arguments
Write-Host "Libreria instalada correctamente."
