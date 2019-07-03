cd "%PATH_TO_PROJECT%\compiled"

pyinstaller --clean --noupx --hidden-import decimal --name DayZ_LootEditor --distpath "%PATH_TO_PROJECT%\compiled" --path "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64" --onefile "%PATH_TO_PROJECT%\application\frontend.py"

