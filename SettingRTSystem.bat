cd /d %~dp0
cmd /c rtexit /localhost/rtcConfSetReq0.rtc
start python startNamingService.py
dist\SettingRTSystem