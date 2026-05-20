# 🃏 GitHub Dev Card Generator

> An AI-powered web app that generates beautiful, personalized developer identity cards from any public GitHub profile — powered by **Gemini AI** and the **GitHub REST API**.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Real GitHub Data** | Fetches repos, stars, followers, languages live |
| **AI Analysis** | Gemini 1.5 Flash analyzes your coding personality |
| **5 Unique Themes** | Hacker · Builder · Researcher · Designer · OSS Hero |
| **Instant Preview** | See your card rendered in the browser |
| **Download** | Save as standalone HTML |
| **Share** | Copy direct card URL |

---

## 🚀 Quick Start (Local — VSCode / Terminal)

### Step 1 — Get API Keys

1. **Google Gemini API Key** (free): [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. **GitHub Token** (optional, but recommended): [github.com/settings/tokens](https://github.com/settings/tokens) — no scopes needed

### Step 2 — Set Up Environment

```bash
cd github-dev-card-generator/backend

# Copy .env template
cp ../.env.example .env

# Edit .env and paste your keys:
#   GOOGLE_API_KEY=AIza...
#   GITHUB_TOKEN=ghp_...  (optional)
```

### Step 3 — Install Dependencies

```bash
# From the backend folder:
pip install -r requirements.txt
```

> Using a virtualenv? Run first:
> ```bash
> python -m venv .venv
> # Windows:
> .venv\Scripts\activate
> # macOS / Linux:
> source .venv/bin/activate
> ```

### Step 4 — Start the Backend

```bash
# Still inside backend/
uvicorn main:app --reload --port 8080
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

### Step 5 — Open the Frontend

Simply open `frontend/index.html` in your browser:
- Double-click the file in Explorer, OR
- In VSCode: right-click → **Open with Live Server**, OR
- In terminal: `start frontend/index.html` (Windows) / `open frontend/index.html` (Mac)

### Step 6 — Generate!

Type any public GitHub username and click **Generate Card** ✨

---

## 📁 Project Structure

```
github-dev-card-generator/
├── backend/
│   ├── main.py            ← FastAPI app (all routes)
│   ├── github_api.py      ← GitHub REST API client
│   ├── gemini_api.py      ← Gemini AI analysis
│   ├── card_generator.py  ← HTML card themes & rendering
│   ├── requirements.txt
│   ├── .env               ← Your API keys (create from .env.example)
│   └── static/
│       └── cards/         ← Saved card HTML files
├── frontend/
│   └── index.html         ← Single-page UI (no build step)
├── .env.example
└── README.md
```

---

## 🎨 Card Themes

| Theme | Trigger | Style |
|---|---|---|
| 🖥️ **Hacker** | Low-level C / Rust / Assembly experts | Dark terminal, green matrix |
| 🔨 **Builder** | Prolific app builders, high repo count | Dark blue, professional |
| 🔬 **Researcher** | Python / R / ML / academia | Purple, elegant |
| 🎨 **Designer** | CSS / Figma / UI-focused | Pink/purple gradient |
| 🦸 **OSS Hero** | 5k+ stars, active community | GitHub green |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/generate` | Generate card for `{"username": "..."}` |
| `GET` | `/card/{username}` | Serve saved card as HTML page |
| `GET` | `/api/github/{username}` | Raw GitHub profile data (debug) |
| `GET` | `/health` | Health check → `{"status":"ok"}` |

---

## 🛠 Troubleshooting

### "Cannot connect to backend"
→ Make sure `uvicorn main:app --reload --port 8080` is running in the `backend/` directory.

### "GOOGLE_API_KEY is not set"
→ Create a `.env` file in the `backend/` folder with your key.

### "GitHub user not found"
→ The username is wrong or the profile is private.

### "GitHub API rate limit hit"
→ Add a `GITHUB_TOKEN` in your `.env` (free, no permissions needed).

### Gemini quota exceeded
→ The app falls back gracefully to pre-computed analysis. Try again in a minute.

---

## 🧑‍💻 Tech Stack

- **Backend**: FastAPI + Uvicorn + httpx
- **AI**: Google Gemini 1.5 Flash
- **Data**: GitHub REST API v3
- **Frontend**: Vanilla HTML/CSS/JS (no build tools)
- **Card Format**: Self-contained HTML with inline CSS

---

Built with ❤️ for the Google Build with AI — Agent Builder Camp (GFG × Google, May 2026)
