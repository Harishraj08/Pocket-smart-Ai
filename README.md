# PocketSmart AI

Full-stack budget and recommendation assistant implementing the supplied project documentation:
Home Interior, Party, and Jewelry planners; FastAPI; Jinja2/HTML/CSS/JS; Gemini multimodal AI; auth/session handling; history; and simulated third-party vendor sourcing.

## Setup
Python 3.11+ is recommended.

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

### AI
The app runs immediately in `AI_MODE=mock`. To enable Gemini, put your API key in `.env` and set:
```env
AI_MODE=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```
The original document names Gemini 1.5 Flash Pro; the model is configurable because model availability changes over time.

### Tests
```bash
pytest -q
```
API docs: http://127.0.0.1:8000/docs

### Structure
```text
PocketSmartAI/
├── app/
│   ├── main.py config.py database.py models.py schemas.py auth.py gemini_utils.py vendor_catalog.py
│   ├── routes/{pages.py,auth.py,planners.py}
│   ├── services/recommendation_service.py
│   ├── templates/{base.html,index.html,login.html,register.html,history.html}
│   └── static/{css/styles.css,js/app.js}
├── tests/test_api.py
├── data/.gitkeep
├── requirements.txt
├── .env.example
└── README.md
```

Vendor entries are intentionally simulated rather than live scraped inventory. Replace `vendor_catalog.py` with approved partner/affiliate APIs for production.
