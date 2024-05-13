@echo off

SCHTASKS /CREATE /SC MINUTE /MO 5 /TN "E1-CoreMonitor" /TR "\"C:\e1-buoy-main\Instrument Management and Control\software\scripts\run_core_monitor.bat"" /ST 09:00
