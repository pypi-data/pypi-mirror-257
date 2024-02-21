@echo off
setlocal

SET PYTHONPATH=%~dp0\src;%PYTHONPATH%
SET AZ_INSTALLER=PIP

IF EXIST "%~dp0\python.exe" (
  "%~dp0\python.exe" -m foundationallm.cli %*
) ELSE (
  python -m foundationallm.cli %*
)
