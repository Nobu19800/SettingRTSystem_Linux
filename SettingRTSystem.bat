cd /d %~dp0
cmd /c rtexit /localhost/rtcConfSetReq0.rtc
cmd /c python startNamingService.py
dist\SettingRTSystem