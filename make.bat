@echo on
set PY_FILE=text_editor.py
set PROJECT_NAME=PES4_WE8_Text_Editor
set VERSION=1.0.0
set FILE_VERSION=file_version_info.txt
set EXTRA_ARG=--add-data=resources/*;resources/ 
set ICO_DIR=resources/pes_indie.ico

pyinstaller --onefile --window "%PY_FILE%" --icon="%ICO_DIR%" --name "%PROJECT_NAME%_%VERSION%"  %EXTRA_ARG% --version-file "%FILE_VERSION%"

Rem This command below is just specific for this script

Xcopy /E ".\config\" ".\dist\config\"

Rem end of extra command

cd dist
tar -acvf "%PROJECT_NAME%_%VERSION%.zip" * config
pause
