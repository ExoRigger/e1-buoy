@echo off

SCHTASKS /CREATE /SC HOURLY /TN "E1-CoreMonitor" /TR "C:\e1-buoy-main\Instrument Management and Control\software\scripts\run_core_monitor.bat" /ST 06:00