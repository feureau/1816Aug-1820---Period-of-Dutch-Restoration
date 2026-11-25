@echo off
setlocal
title Dutch Restoration Archives (1816-1820) - Local Server
cd /d "%~dp0"

where python >nul 2>&1
if %errorlevel%==0 (
    python scripts\serve.py %*
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        py -3 scripts\serve.py %*
    ) else (
        echo Python 3 was not found in PATH. Install Python 3 to launch the local archive viewer.
        pause
        exit /b 1
    )
)

if errorlevel 1 (
    echo.
    echo Server exited with an error. See details above.
    pause
)
