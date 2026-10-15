# FoodFlow — Online Food Order Processing System

A student mini-project demonstrating FIFO queue processing for food orders. The root `index.html` is a GitHub Pages-compatible interactive demo; the Flask/SQLite backend is in `app.py` and is run locally with Python.

## Run Flask version

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. See `REPORT_TEMPLATE.md` for the report outline. GitHub Pages serves static files only, so its demo saves data in the current browser and is not shared with other visitors.