@echo off
REM QA Buddy AI - Automated Startup Script for Windows
REM This script starts all required services and opens the UI
REM Author: QA Buddy AI Team
REM Date: 2026-10-10

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  QA Buddy AI - Multi-source Hybrid RAG System
echo ============================================================
echo.

REM Get the project root directory
set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

echo [*] Project root: %PROJECT_ROOT%
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo.
    echo Please create .env first:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and add your GROQ_API_KEY and Qdrant settings
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [✓] .env file found
echo.

REM Check Python
echo [*] Checking Python 3.13...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found or not on PATH
    echo Please install Python 3.13 from https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [✓] Python %PYTHON_VERSION% found
echo.

REM Check Ollama
echo [*] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Ollama not found or not on PATH
    echo Please install Ollama from https://ollama.com/download
    pause
    exit /b 1
)
echo [✓] Ollama installed
echo.

REM Check if embedding model is pulled
echo [*] Checking if Qwen3-Embedding model is downloaded...
ollama list | findstr qwen3-embedding >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Qwen3-Embedding not found locally
    echo.
    echo Would you like to download it now? This is a one-time ~500MB download.
    set /p PULL_MODEL="Download qwen3-embedding:0.6b? (y/n): "
    if /i "!PULL_MODEL!"=="y" (
        echo [*] Downloading qwen3-embedding:0.6b...
        ollama pull qwen3-embedding:0.6b
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to download model
            pause
            exit /b 1
        )
        echo [✓] Model downloaded successfully
    ) else (
        echo [ERROR] Qwen3-Embedding is required. Please download it first:
        echo   ollama pull qwen3-embedding:0.6b
        pause
        exit /b 1
    )
) else (
    echo [✓] Qwen3-Embedding model is downloaded
)
echo.

REM Check if UI is built
echo [*] Checking if UI is built...
if not exist "ui\dist" (
    echo [WARNING] UI not built yet
    set /p BUILD_UI="Build UI now? (y/n): "
    if /i "!BUILD_UI!"=="y" (
        echo [*] Building UI...
        cd ui
        call npm install
        call npm run build
        if %errorlevel% neq 0 (
            echo [ERROR] UI build failed
            cd /d "%PROJECT_ROOT%"
            pause
            exit /b 1
        )
        echo [✓] UI built successfully
        cd /d "%PROJECT_ROOT%"
    ) else (
        echo [ERROR] UI must be built. Run: cd ui ^&^& npm run build
        cd /d "%PROJECT_ROOT%"
        pause
        exit /b 1
    )
) else (
    echo [✓] UI is already built
)
echo.

echo ============================================================
echo  Starting Services...
echo ============================================================
echo.

REM Check and start Qdrant
echo [*] Checking Qdrant...
curl.exe -s http://localhost:6333/ >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Qdrant not running.
    echo.
    echo OPTION 1: Use Qdrant Cloud (recommended for beginners)
    echo   - Set QDRANT_URL and QDRANT_API_KEY in .env
    echo   - Then run this script again
    echo.
    echo OPTION 2: Start local Qdrant
    echo   - Open PowerShell and run:
    echo     cd .qdrant-win
    echo     .\qdrant.exe
    echo.
    echo Press any key to continue when Qdrant is ready...
    pause

    echo [*] Retrying Qdrant connection...
    timeout /t 2 >nul
    curl.exe -s http://localhost:6333/ >nul 2>&1
    if %errorlevel% neq 0 (
        echo [WARNING] Qdrant still not reachable - using configured endpoint
        echo If this fails, check your QDRANT_URL in .env
    ) else (
        echo [✓] Qdrant is reachable
    )
) else (
    echo [✓] Qdrant is running
)
echo.

REM Check Ollama is running
echo [*] Verifying Ollama is running...
curl.exe -s http://localhost:11434/api/version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama not running at http://localhost:11434
    echo.
    echo Would you like to start Ollama now? (requires separate terminal)
    set /p START_OLLAMA="Start Ollama? (y/n): "
    if /i "!START_OLLAMA!"=="y" (
        echo [*] Starting Ollama in new window...
        start "Ollama" cmd /k "ollama serve"
        echo [*] Waiting for Ollama to start...
        timeout /t 5 >nul
        echo [*] Retrying connection...
        curl.exe -s http://localhost:11434/api/version >nul 2>&1
        if %errorlevel% neq 0 (
            echo [ERROR] Ollama failed to start
            pause
            exit /b 1
        )
        echo [✓] Ollama started successfully
    ) else (
        echo [ERROR] Ollama is required. Start it with: ollama serve
        pause
        exit /b 1
    )
) else (
    echo [✓] Ollama is running
)
echo.

REM Ingest data if needed
echo [*] Checking if data needs to be ingested...
if not exist ".ingested" (
    echo [INFO] This appears to be first run - data needs to be indexed
    set /p RUN_INGEST="Run 'python -m qabuddy ingest' now? (y/n): "
    if /i "!RUN_INGEST!"=="y" (
        echo [*] Ingesting data - this may take 5-10 minutes on first run...
        python -m qabuddy ingest
        if %errorlevel% neq 0 (
            echo [ERROR] Ingestion failed
            pause
            exit /b 1
        )
        echo [✓] Data ingested successfully
        echo. > .ingested
    ) else (
        echo [WARNING] Data ingestion skipped. Run 'python -m qabuddy ingest' manually when ready.
    )
) else (
    echo [✓] Data already ingested (run 'python -m qabuddy ingest' to update)
)
echo.

echo ============================================================
echo  Starting QA Buddy API...
echo ============================================================
echo.
echo [*] Starting the application at http://localhost:8300
echo [*] Press Ctrl+C to stop the server
echo.

REM Start Python application
python -m qabuddy serve

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] API failed to start
    echo Check the error messages above
    pause
    exit /b 1
)

REM This won't be reached unless the API stops
echo.
echo [*] API stopped
pause
