@echo off
REM =====================================================================
REM  Test Plan Agent - launch the Streamlit UI (SOP_trigger T6)
REM
REM  Opens the interactive UI at http://localhost:8501
REM  Press Ctrl+C in this window to stop the server.
REM =====================================================================

setlocal
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

if not exist ".env" (
    echo [ERROR] .env not found. Copy .env.example to .env and fill in your credentials.
    exit /b 1
)

echo Starting Test Plan Agent UI...
echo Open http://localhost:8501 in your browser. Press Ctrl+C to stop.
echo.

py -m streamlit run app.py

endlocal
