import subprocess

# Run secara bersamaan
backend = subprocess.Popen(["fastapi", "dev", "src/backend/main.py"])
frontend = subprocess.Popen(["flet", "run", "src/frontend"])

backend.wait()
frontend.wait()