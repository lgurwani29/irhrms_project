# IRHRMS Integrated Prototype (IRHRMS + IPAS + PRS) – SECR Bilaspur (EDPM)

Author: Lavanya Guruwani · BIT Raipur

This package contains a working Flask prototype for:
- IRHRMS (Employee CRUD)
- IPAS (Payroll CRUD)
- PRS (Reservations CRUD)

## Quick start (macOS / VS Code)
```bash
# 1. open terminal and go to project folder
cd ~/Downloads/secr_irhrms_project_final_full   # or wherever you extracted it

# 2. create and activate venv
python3 -m venv venv
source venv/bin/activate

# 3. install dependencies
pip install -r requirements.txt

# 4. run the app
python3 app.py

# 5. open browser at
http://127.0.0.1:5000/
```

## Files
- app.py — Flask backend, routes for all modules
- irhrms.db — SQLite database preloaded with sample data
- templates/ — Bootstrap templates (base, index, employees, payroll, reservations, forms)
- static/ — CSS and logos
- modules/ — helper (database.py)
- presentation/ppt vt 2.pptx — your uploaded PPT
- presentation/screenshots/ — drop your screenshots here for packaging

## Deploy to Render.com
1. Push repo to GitHub.
2. Create new Web Service on Render, link repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python3 app.py`

Note: For production, consider gunicorn and proper environment settings.
