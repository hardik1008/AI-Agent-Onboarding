@echo off
title PolicyNest Enterprise AI-First POSP Platform
cd /d "%~dp0"
echo ========================================================
echo   POLICYNEST ENTERPRISE AI-FIRST POSP ONBOARDING SUITE
echo   IRDAI Direct Broker (Life ^& General) - Production Engine
echo ========================================================
echo.
echo Launching Production Server at http://localhost:8000 ...
start "" "http://localhost:8000"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
