@echo off
call C:\Anaconda3\Scripts\activate.bat

python gen_elan_sync.py %*
python gen_elan_merge.py %*
pause
