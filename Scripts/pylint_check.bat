@echo off
setlocal

REM Start from repository root (parent of the Scripts folder)
pushd "%~dp0.."

set "PYLINT_RC=%CD%\Scripts\pylint.rc"
set "VENV_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment not found at "%VENV_PYTHON%"
    echo Create it first with: py -m venv .venv
    popd
    exit /b 1
)

if not exist "%PYLINT_RC%" (
    echo ERROR: Pylint config not found at "%PYLINT_RC%"
    popd
    exit /b 1
)

"%VENV_PYTHON%" -m pylint --rcfile="%PYLINT_RC%" espeasyflasher.py
if errorlevel 1 set "EXIT_CODE=1"

"%VENV_PYTHON%" -m pylint --rcfile="%PYLINT_RC%" .\eef_modules
if errorlevel 1 set "EXIT_CODE=1"

"%VENV_PYTHON%" -m pylint --rcfile="%PYLINT_RC%" .\tests
if errorlevel 1 set "EXIT_CODE=1"

"%VENV_PYTHON%" -m pylint --rcfile="%PYLINT_RC%" .\Scripts\build_info.py
if errorlevel 1 set "EXIT_CODE=1"

if not defined EXIT_CODE set "EXIT_CODE=0"

echo.
echo Pylint finished with exit code %EXIT_CODE%.

popd
pause
exit /b %EXIT_CODE%
