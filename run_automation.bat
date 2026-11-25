
@echo off

cd /d "D:\DataAnalyticsProjects\Ecommerce_Sales_Analytics_BI"

echo Starting Ecommerce ETL Pipeline...

".venv\Scripts\python.exe" "scripts\run_product_pipeline.py" >> "logs\automation.log" 2>&1

echo Pipeline execution finished.

exit /b %ERRORLEVEL%
