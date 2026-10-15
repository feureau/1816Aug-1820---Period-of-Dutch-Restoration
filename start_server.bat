@echo off
title Dutch Restoration Local Server (http://localhost:8000)
echo ===================================================
echo   Dutch Restoration Project - Local Web Server
echo ===================================================
echo.
echo Server running at: http://localhost:8000
echo.
echo Keep this window open while editing and viewing the site.
echo Press Ctrl+C or close this window to stop the server.
echo.
python -m http.server 8000
pause
