# install-context-menu.ps1
# Registers "Convert to Markdown" in the right-click context menu for .docx and .pdf files.
# Run from the environment where convert-to-md is installed.
# Does NOT require administrator privileges (writes to HKCU).

param(
    [string]$ExePath  # Optional: explicit path to convert-to-md.exe
)

# Locate the convert-to-md executable
if (-not $ExePath) {
    $cmd = Get-Command convert-to-md -ErrorAction SilentlyContinue
    if ($cmd) {
        $ExePath = $cmd.Source
    } else {
        # Fallback: try python -m
        $py = Get-Command python -ErrorAction SilentlyContinue
        if (-not $py) {
            Write-Error "Cannot find 'convert-to-md' or 'python' on PATH. Install the package first or pass -ExePath."
            exit 1
        }
        $ExePath = "`"$($py.Source)`" -m convert_to_md"
        Write-Host "Using fallback: $ExePath"
    }
}

# Ensure the path is quoted if it's a single executable
if ($ExePath -notmatch '^"' -and $ExePath -notmatch ' -m ') {
    $ExePath = "`"$ExePath`""
}

$menuLabel = "Convert to &Markdown"
$extensions = @(".docx", ".pdf")

foreach ($ext in $extensions) {
    $basePath = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\ConvertToMarkdown"

    # Create the verb key
    New-Item -Path $basePath -Force | Out-Null
    Set-ItemProperty -Path $basePath -Name "(Default)" -Value $menuLabel

    # Create the command key
    $cmdPath = "$basePath\command"
    New-Item -Path $cmdPath -Force | Out-Null
    Set-ItemProperty -Path $cmdPath -Name "(Default)" -Value "$ExePath --overwrite `"%1`""

    Write-Host "Registered context menu for $ext"
}

Write-Host ""
Write-Host "Done. 'Convert to Markdown' is now available when you right-click .docx and .pdf files."
Write-Host "On Windows 11, look under 'Show more options'."
Write-Host "You may need to restart Explorer for changes to take effect."
