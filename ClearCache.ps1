Get-ChildItem -Path AspireTUI -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
