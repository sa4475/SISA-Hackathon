## AI Security Hackathon Demos

Intentionally vulnerable web demos (XSS, SSTI, SQLi) and supporting scripts for showcasing risks and defenses.

## Prerequisites
- Python 3.10 or newer
- Windows PowerShell

## Setup
```powershell
cd C:\Users\arjun\Desktop\Ai_hackahton
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the web app (Flask)
```powershell
python webapp\app.py
```
Open `http://127.0.0.1:5000`.

Quick links:
- XSS: `http://127.0.0.1:5000/xss?payload=%3Csvg%20onload%3Dalert(1)%3E`
- SSTI: `http://127.0.0.1:5000/ssti?template={{7*7}}`
- SQLi: `http://127.0.0.1:5000/sqli?q=%27%20OR%20%271%27%3D%271%27%20--`

Change port (optional):
```powershell
$env:PORT=5001; python webapp\app.py
```

## Alternative: zero-dependency demo server
Run a pure-stdlib HTTP server on port 8000:
```powershell
python webapp\simple_server.py
```
Open `http://127.0.0.1:8000`.

## Helper scripts
- `run_all.ps1`: runs all demos and saves outputs in `out/`
- `recon_ai.py`, `exploit_ai.py`, `defense_anomaly.py`, `attack_chain_sim.py`
- `credential_theft_sim.py`, `openai_prompt_injection.py`, `data_poisoning_demo.py`, `model_extraction_sim.py`
- `adversarial_input_demo.py`, `dos_attack_sim.py`, `privacy_leakage_test.py`, `social_engineering_demo.py`

Run all:
```powershell
./run_all.ps1
```

## Project layout
- `webapp/app.py`: Flask app and vulnerable routes
- `webapp/templates/`: Jinja templates (`base.html`, `index.html`, `xss.html`, `ssti.html`, `sqli.html`)
- `webapp/static/styles.css`: modernized UI styling

## Troubleshooting
- Connection refused: ensure the server is running; check `netstat -ano | findstr :5000`
- Try a different port: `$env:PORT=5001; python webapp\app.py`
- Logs (if started detached): `out\flask_stdout.txt`, `out\flask_stderr.txt`

## Security note
These pages are intentionally vulnerable for local demo use only. Do not deploy publicly.


