
@echo off

cd /d "D:\DataAnalyticsProjects\Ecommerce_Sales_Analytics_BI"

".venv\Scripts\python.exe" "scripts\generate_live_orders.py" >> "logs\live_orders.log" 2>&1

exit /b %ERRORLEVEL%
