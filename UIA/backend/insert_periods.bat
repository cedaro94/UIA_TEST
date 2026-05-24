@echo off

echo ==========================
echo INSERTANDO PERIODOS
echo ==========================

docker cp insert_periods.py odoo_app:/insert_periods.py

docker exec -it odoo_app odoo shell -d odoo < insert_periods.py

pause