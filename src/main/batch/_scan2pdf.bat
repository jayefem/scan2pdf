@echo off

set "SCAN2PDF_FOLDER=C:\path to this project"

REM Use python of venv in order to get the dependencies
%SCAN2PDF_FOLDER%\venv\Scripts\python.exe %SCAN2PDF_FOLDER%\src\main\python\scan2pdf.py --inputPath . --imagePrefix CCF --imageExt .png

echo.
pause