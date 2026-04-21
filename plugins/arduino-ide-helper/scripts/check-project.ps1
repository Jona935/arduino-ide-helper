. "$PSScriptRoot\arduino-cli-common.ps1"

param(
    [Parameter(Mandatory = $true)]
    [string] $ProjectPath,
    [string] $Fqbn
)

$resolvedProjectPath = Resolve-Path -LiteralPath $ProjectPath
$projectDirectory = $resolvedProjectPath.Path

if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
    throw "La ruta indicada no es una carpeta: $ProjectPath"
}

$inoFiles = Get-ChildItem -LiteralPath $projectDirectory -Filter *.ino -File
if (-not $inoFiles) {
    throw "No encontre archivos .ino en $projectDirectory"
}

Write-Host "Sketches encontrados:"
$inoFiles | ForEach-Object { Write-Host "- $($_.Name)" }

$sourceFiles = Get-ChildItem -LiteralPath $projectDirectory -Recurse -File -Include *.ino,*.pde,*.h,*.hpp,*.c,*.cpp
$includeNames = foreach ($file in $sourceFiles) {
    $matches = Select-String -Path $file.FullName -Pattern '^\s*#include\s*[<"]([^">]+)[">]' -AllMatches
    foreach ($match in $matches) {
        foreach ($group in $match.Matches.Groups) {
            if ($group.Name -eq "1" -and $group.Value) {
                $group.Value
            }
        }
    }
}

$uniqueIncludes = $includeNames | Sort-Object -Unique
if ($uniqueIncludes) {
    Write-Host ""
    Write-Host "Includes detectados:"
    $uniqueIncludes | ForEach-Object { Write-Host "- $_" }
}

if ($Fqbn) {
    Write-Host ""
    Write-Host "Compilando proyecto con FQBN $Fqbn..."
    Invoke-ArduinoCli -Arguments @("compile", "--fqbn", $Fqbn, $projectDirectory)
    Write-Host "Revision completa: el proyecto compilo correctamente."
}
else {
    Write-Host ""
    Write-Warning "No se proporciono FQBN. Solo hice una revision estructural."
    Write-Host "Para compilar, vuelve a ejecutar con -Fqbn, por ejemplo: arduino:avr:uno"
}
