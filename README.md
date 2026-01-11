# YAREU - Your Action to Reuse & Unite

## Menjalankan Aplikasi (Development)

1. **Buat virtual environment**

   - Windows
     ```powershell
     python -m venv .venv
     ```
   - macOS
     ```bash
     python3 -m venv .venv
     ```

2. **Aktifkan virtual environment**

   - Windows
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS
     ```bash
     source .venv/bin/activate
     ```

3. **Jalankan backend FastAPI**
   - Windows
     ```powershell
     python src/begin.py
     ```
   - macOS
     ```bash
     python3 src/begin.py
     ```

## Command Lainnya

Untuk memperbarui [requirements.txt](requirements.txt) setelah meng-install dependencies baru:

```bash
pip freeze > requirements.txt
```
