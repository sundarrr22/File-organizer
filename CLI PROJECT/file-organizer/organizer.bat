@echo off
REM File Organizer CLI - Windows Wrapper Script
REM 
REM Usage:
REM   organizer.bat <directory> [options]
REM
REM Examples:
REM   organizer.bat .
REM   organizer.bat C:\Downloads --recursive
REM   organizer.bat "C:\My Documents" --dry-run
REM   organizer.bat . --recursive --dry-run

setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    exit /b 1
)

REM Run the CLI
python cli.py %*

endlocal
exit /b %errorlevel%
