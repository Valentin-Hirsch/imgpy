# imgpy.ps1

$ROOT = $PSScriptRoot

Push-Location $ROOT

src/.venv/Scripts/Activate.ps1

python -m src $args

deactivate

Pop-Location


#<file:end>
