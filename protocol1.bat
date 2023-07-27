@echo off
cd /d C:/Users/Natha/protocol1
echo Running code...
set "flag=%~1"
IF "%flag%" == "" (
	python main.py
) ELSE (
	python main.py --type=%flag%
)

pause