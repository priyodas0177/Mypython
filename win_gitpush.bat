@echo off

:ask
set /p msg=Enter commit message: 

if "%msg%"=="" (
    echo Commit message cannot be empty!
    goto ask
)

git add .
git commit -m "%msg%"
git push origin main

pause
