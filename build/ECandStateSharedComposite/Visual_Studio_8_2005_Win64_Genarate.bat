cd /d %~dp0
cmake ../../Composite/ECandStateSharedComposite/ -G "Visual Studio 8 2005 Win64" -D CMAKE_INSTALL_PREFIX="C:/OpenRTM-aist" ../../Composite/ECandStateSharedComposite/
copy ..\..\Composite\ECandStateSharedComposite\RTC.xml RTC.xml
