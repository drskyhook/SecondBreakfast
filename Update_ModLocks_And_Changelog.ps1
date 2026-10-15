$Date = Get-Date -Format "yyyy-MM-dd"
$Changelog = ".\CHANGELOG.md"

$Locks = @(
    @{
        Label = "Server Mods"
        ModsPath = ".\SERVER\mods"
        LockPath = "SERVER/mods/mods.lock.txt"
    },
    @{
        Label = "Client Mods"
        ModsPath = ".\CLIENT\mods"
        LockPath = "CLIENT/mods/mods.lock.txt"
    }
)

# Normalize auto-generated Java Properties timestamps
$configPath = Join-Path $PSScriptRoot "SERVER\config"

Get-ChildItem $configPath -Filter "*.properties" -Recurse -File |
    ForEach-Object {
        $file = $_.FullName
        $content = [System.IO.File]::ReadAllText($file)

        $normalized = [regex]::Replace(
            $content,
            '(?m)^#[A-Z][a-z]{2} [A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2} [A-Za-z0-9:+-]+ \d{4}(?=\r?$)',
            '# Generated configuration'
        )

        if ($normalized -ne $content) {
            [System.IO.File]::WriteAllText($file, $normalized)
            Write-Host "Normalized: $file"
        }
    }

    
function Get-PreviousFile($path) {
    git show "HEAD:$path" 2>$null
}

function Get-CurrentFile($path) {
    if (Test-Path $path) { Get-Content $path } else { @() }
}

function Get-SameDateBodies($lines, $pattern) {
    $bodies = @()
    $currentBody = @()
    $inSection = $false

    foreach ($line in $lines) {
        if ($line -match $pattern) {
            if ($inSection) {
                $bodies += ($currentBody -join "`n").Trim()
                $currentBody = @()
            }
            $inSection = $true
            continue
        }

        if ($inSection) {
            if ($line -match '^# ') {
                $bodies += ($currentBody -join "`n").Trim()
                $currentBody = @()
                $inSection = $false
            } else {
                $currentBody += $line
            }
        }
    }

    if ($inSection) {
        $bodies += ($currentBody -join "`n").Trim()
    }

    return $bodies
}

$existingChangelog = if (Test-Path $Changelog) { Get-Content $Changelog } else { @() }
$headerPattern = "^# $Date(?: #\d+)?$"
$existingCount = ($existingChangelog | Where-Object { $_ -match $headerPattern }).Count

if ($existingCount -gt 0) {
    $counter = 0
    $rewritten = $existingChangelog | ForEach-Object {
        if ($_ -match $headerPattern) {
            $counter++
            "# $Date #$counter"
        } else {
            $_
        }
    }

    Set-Content $Changelog $rewritten

    $entryHeader = "# $Date #$($existingCount + 1)"
} else {
    $entryHeader = "# $Date"
}

$entry = "`n$entryHeader`n"
$hasChanges = $false

foreach ($lock in $Locks) {
    $old = @(Get-PreviousFile $lock.LockPath)

    Get-ChildItem $lock.ModsPath -File -Filter "*.jar" |
        Sort-Object Name |
        ForEach-Object { $_.Name } |
        Set-Content $lock.LockPath

    $new = @(Get-CurrentFile $lock.LockPath)

    $added = $new | Where-Object { $_ -and ($_ -notin $old) }
    $removed = $old | Where-Object { $_ -and ($_ -notin $new) }

    if ($added.Count -gt 0 -or $removed.Count -gt 0) {
        $hasChanges = $true
        $entry += "`n## $($lock.Label)`n"

        if ($added.Count -gt 0) {
            $entry += "`n### Added`n"
            foreach ($m in $added) { $entry += "- $m`n" }
        }

        if ($removed.Count -gt 0) {
            $entry += "`n### Removed`n"
            foreach ($m in $removed) { $entry += "- $m`n" }
        }
    }
}

if ($hasChanges) {
    $entryLines = $entry -split "`n"
    $entryBody = if ($entryLines.Length -gt 1) { ($entryLines[1..($entryLines.Length - 1)] -join "`n").Trim() } else { "" }
    $existingBodies = Get-SameDateBodies $existingChangelog $headerPattern

    if ($existingBodies -contains $entryBody) {
        Write-Host "No new unique changelog entry; identical update already recorded."
    } else {
        Add-Content $Changelog $entry
        Write-Host "Changelog updated."
    }
} else {
    Write-Host "No mod changes detected."
}