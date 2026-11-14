@echo off
REM ============================================================
REM  Deploy Job Tracker ATS to Vercel (project: job-tracker-ats)
REM ============================================================
setlocal

cd /d "%~dp0"

echo [1/3] Building project...
call npm run build
if errorlevel 1 (
  echo Build failed. Aborting deploy.
  exit /b 1
)

echo [2/3] Ensuring Vercel CLI is available...
where vercel >nul 2>nul
if errorlevel 1 (
  echo Vercel CLI not found. Installing globally...
  call npm install -g vercel
)

echo [3/3] Deploying to Vercel (production)...
call vercel --prod --yes
if errorlevel 1 (
  echo Deploy failed. You may need to run "vercel login" first.
  exit /b 1
)

echo Deploy complete.
endlocal