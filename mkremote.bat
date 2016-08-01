@echo off

REM target  : python2.7
REM require : requets pyinstaller

cd scripts
pyinstaller -n raspi-signage-remote --onefile -c remote.py

