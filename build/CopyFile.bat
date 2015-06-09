cd /d %~dp0
del /Q ..\Manager\Cpp\rtcd_p\Release\*
copy /Y rtcd_p\Release\rtcd_p.exe ..\Manager\Cpp\rtcd_p\Release\rtcd_p.exe

del /Q ..\rtcdControl\src\Release\*
copy /Y rtcdControl\src\Release\rtcdControlComp.exe ..\rtcdControl\src\Release\rtcdControlComp.exe
