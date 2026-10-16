@echo off
REM =====================================================================
REM  Test Plan Agent - scheduled trigger entry point (SOP_trigger T4)
REM
REM  Generates a test plan for every issue in a Jira project and writes a
REM  timestamped log to .tmp\. Register with Windows Task Scheduler, e.g.:
REM
REM    schtasks /Create /TN "TestPlanAgent" /TR "<path>\trigger.bat" ^
REM             /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 08:00
REM
REM  Exit code 0 = all plans generated, 1 = one or more failed.
REM =====================================================================

setlocal

REM Resolve the directory this script lives in, so it works from any cwd.
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM --- Configuration: override via environment variables if desired ---
if "%JIRA_PROJECT%"=="" set "JIRA_PROJECT=SAM1"
if "%PLAN_LIMIT%"==""   set "PLAN_LIMIT=10"

REM --- Timestamped log (PowerShell for a locale-independent timestamp) ---
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"`) do set "DATESTAMP=%%i"
if "%DATESTAMP%"=="" set "DATESTAMP=run"
if not exist ".tmp" mkdir ".tmp"
set "LOGFILE=.tmp\trigger_%DATESTAMP%.log"

echo ===================================================================== >> "%LOGFILE%"
echo Test Plan Agent trigger - %DATE% %TIME% >> "%LOGFILE%"
echo Project: %JIRA_PROJECT%   Limit: %PLAN_LIMIT% >> "%LOGFILE%"
echo ===================================================================== >> "%LOGFILE%"

REM --- Run the pipeline for the whole project ---
py tools\run.py --project %JIRA_PROJECT% --limit %PLAN_LIMIT% >> "%LOGFILE%" 2>&1
set "EXITCODE=%ERRORLEVEL%"

echo. >> "%LOGFILE%"
echo Exit code: %EXITCODE% >> "%LOGFILE%"

if %EXITCODE%==0 (
    echo [OK] Test plan generation completed. See %LOGFILE%
) else (
    echo [ERROR] Test plan generation reported failures. See %LOGFILE%
)

endlocal & exit /b %EXITCODE%
