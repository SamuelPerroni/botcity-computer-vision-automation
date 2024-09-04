$exclude = @("venv", "contosoFaturas.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "contosoFaturas.zip" -Force