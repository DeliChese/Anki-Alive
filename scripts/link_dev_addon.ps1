$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$addonsRoot = Join-Path $env:APPDATA "Anki2\addons21"
$target = Join-Path $addonsRoot "anki_alive_dev"

New-Item -ItemType Directory -Force -Path $addonsRoot | Out-Null

if (Test-Path $target) {
    $item = Get-Item $target -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Remove-Item $target -Force
    } else {
        throw "Refusing to replace existing non-link folder: $target"
    }
}

New-Item -ItemType Junction -Path $target -Target $repoRoot | Out-Null
Write-Host "Anki Alive dev link created:"
Write-Host "  $target -> $repoRoot"
Write-Host "Restart Anki. Future Git pulls update the linked add-on automatically."
