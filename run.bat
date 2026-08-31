@echo off

title Student Management System

echo ========================================
echo    STUDENT MANAGEMENT SYSTEM
echo ========================================
echo.

cd /d "%~dp0backend"

echo Starting Django server...
echo.

venv\Scripts\python.exe manage.py runserver

pause