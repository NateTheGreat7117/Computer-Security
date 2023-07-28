@echo off
cd /d C:/Users/Natha/protocol4
echo Running code...
set "flag1=%~1"
set "flag2=%~2"
set "flag3=%~3"
python main.py --type="%flag1%" --time="%flag2%" --volume="%flag3%"
pause