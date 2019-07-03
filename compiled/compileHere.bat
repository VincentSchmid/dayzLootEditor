SET PATH_TO_PROJECT=%~dp0..

call "%PATH_TO_PROJECT%\compiled\installer.bat"
rmdir /Q/S "%PATH_TO_PROJECT%\compiled\build"
DEL /Q  "%PATH_TO_PROJECT%\compiled\*.spec"
DEL /Q  "%PATH_TO_PROJECT%\compiled\*.7z"
rmdir /Q/S "%PATH_TO_PROJECT%\application\__pycache__"
DEL /Q "%PATH_TO_PROJECT%\compiled\release *\*.exe"
copy "%PATH_TO_PROJECT%\compiled\*.exe %PATH_TO_PROJECT%\compiled\release *\bin"
