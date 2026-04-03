# uninstall-context-menu.ps1
# Removes the "Convert to Markdown" context menu entries.
# Does NOT require administrator privileges.

$extensions = @(".docx", ".pdf")

foreach ($ext in $extensions) {
    $basePath = "HKCU:\Software\Classes\SystemFileAssociations\$ext\shell\ConvertToMarkdown"
    if (Test-Path $basePath) {
        Remove-Item -Path $basePath -Recurse -Force
        Write-Host "Removed context menu entry for $ext"
    } else {
        Write-Host "No context menu entry found for $ext (already clean)"
    }
}

Write-Host ""
Write-Host "Done. Restart Explorer for changes to take effect."
