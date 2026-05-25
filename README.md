# 🚀 Global Job Search Aggregator Platform

A high-performance, premium global job search aggregator platform. It automatically crawls developer, design, and marketing roles worldwide using high-speed async scrapers and provides advanced filtering, search history logs, weighted content similarity recommendations, and conversational **Natural Language AI Search** in real-time.

---

## 🏗️ Architectural Overview

```mermaid
graph TD
    %% Scraper Layer
    subgraph Scrapers [Async Crawling Engine]
        WWR[WeWorkRemotely XML Parser]
        ROK[RemoteOK API Crawler]
        MOCK[High-Fidelity Backup Seeder]
    end

    %% Backend Layer
    subgraph FastAPI [Python FastAPI Application]
        Main[main.py Lifespan & CORS]
        Limiter[Custom Rate-Limiting Middleware]
        API[REST API /api Router]
        AI[Conversational AI Search NLP Parser]
        Rec[Content Similarity Recommender]
        Alerts[Telegram & Email Dispatch alerts]
    end

    %% Database Layer
    subgraph Database [Relational Database]
        Engine[(SQLAlchemy Engine)]
        Postgres[(PostgreSQL Production)]
        SQLite[(SQLite Fallback DB)]
    end

    %% Frontend Layer
    subgraph Frontend [Web Clients / Premium UI]
        Home[index.html Home Page]
        Search[search.html Advanced Filters]
        Detail[details.html Specs & Recommendations]
        Saved[saved.html Bookmark Panel]
        AI_Page[ai.html Chat Console]
        Dash[dashboard.html Platform Analytics]
    end

    %% Data Connections
    WWR -->|Save Job| Engine
    ROK -->|Save Job| Engine
    MOCK -->|Seed Jobs| Engine
    
    Engine -->|Primary Database| Postgres
    Engine -->|Local Resilience| SQLite
    
    API -->|Query/Update| Engine
    AI -->|Regex Heuristic Query| API
    Rec -->|Cosine-like overlap| API
    Alerts -->|Dispatches| API
    
    Home <-->|Async JSON| API
    Search <-->|Async JSON| API
    Detail <-->|Async JSON| API
    Saved <-->|Local Cache + Sync| API
    AI_Page <-->|Prompt Dispatch| API
    Dash <-->|Auditing Stats| API
```

---

## 📁 Project Directory Structure

```text
job finder/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── jobs.py             # Paginated queries, filters, stats, & AI prompt routes
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── base_scraper.py     # Headers rotation, retries, duplicate checks, db commits
│   │   ├── weworkremotely.py   # WWR RSS XML scraper
│   │   ├── remoteok.py         # RemoteOK API parser with Cloudflare resilience
│   │   ├── mock_scraper.py     # Pre-seeds DB with gorgeous tech jobs on first run
│   │   └── scheduler.py        # Background task scheduled every 60 minutes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_search.py        # Conversational NLP heuristic query parser
│   │   ├── recommendations.py  # Weighted content similarity recommender
│   │   └── notifications.py    # Console, SMTP email, and Telegram alerts manager
│   ├── __init__.py
│   ├── config.py               # Settings schemas and rate-limit controls
│   ├── database.py             # DB connection hooks & SQLite fallback triggers
│   ├── models.py               # DB tables: jobs, companies, countries, saved, history
│   ├── schemas.py              # Pydantic validation & response structures
│   └── main.py                 # FastAPI application and rate limiting middleware
├── frontend/
│   ├── css/
│   │   └── style.css           # Premium Silicon Valley dark-mode glassmorphic CSS
│   ├── js/
│   │   ├── app.js              # Coordinator, template card renderer, home bootstrapper
│   │   └── saved_jobs.js       # LocalStorage + backend hybrid sync manager
│   ├── pages/
│   │   ├── search.html         # Sidebar search filter board
│   │   ├── details.html        # Specs card and similarity recommendation list
│   │   ├── saved.html          # Dynamic bookmarks viewer
│   │   ├── remote.html         # Work from anywhere index
│   │   ├── countries.html      # Country aggregations layout
│   │   ├── ai.html             # Conversational AI console
│   │   └── dashboard.html      # Auditing graphs & crawler stats panel
│   └── index.html              # Main homepage entry
├── .env.example                # Configuration parameters template
├── requirements.txt            # Python FastAPI backend & crawling library dependencies
└── README.md                   # This instruction manual
```

---

## 🛠️ Complete Installation Guide

### Prerequisites
1. **Python 3.10+** installed on your workstation.
2. **PostgreSQL** database service (Optional - the backend features a robust SQLite local database fallback for automatic out-of-the-box development and testing).

### Step 1: Clone or Copy Project Files
Ensure all project folders (`backend/`, `frontend/`) are placed inside your workspace directory, e.g., `f:\job finder\`.

### Step 2: Set Up Virtual Environment & Dependencies
Open your command terminal inside the project directory and run:

```bash
# 1. Create Python virtual environment
python -m venv venv

# 2. Activate Virtual Environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# 3. Install core libraries
pip install -r requirements.txt
```

### Step 3: Environment Setup
Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open `.env` in your text editor. If you are using PostgreSQL, configure the credentials:
```text
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/YOUR_DB_NAME
```
If left unconfigured, the server will automatically launch using a localized high-performance SQLite database `jobs.db` in your root folder.

---

## 🚀 Running the Aggregator Server Locally

With your virtual environment active, launch the ASGI server:

```bash
python backend/main.py
```
*Alternatively:*
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Server Diagnostics:
- **FastAPI API Server active:** `http://127.0.0.1:8000`
- **Interactive Documentation Portal:** `http://127.0.0.1:8000/docs`
- **Bootstrap Trigger:** On initial startup, if the database is detected as empty, a seeder immediately deploys 45+ high-fidelity mock jobs and pulls active WeWorkRemotely XML feeds so your web boards are instantly loaded and functional.
- **Background Cron:** The scheduler runs every 60 minutes to crawl for fresh listings in the background.

---

## 💻 Running and Previewing the Premium Frontend

Because our client calls the backend asynchronously via `fetch` requests, you can double-click and open the HTML files directly in your web browser, or launch a simple local development server.

To host the client locally, run in your terminal:
```bash
# If using Python
python -m http.server 3000
```
Then navigate to: `http://localhost:3000/frontend/index.html` to preview the breathtaking glassmorphic dark-theme board!

---

## 🔌 Core REST API Endpoint Documentation

| Method | Endpoint | Description |
|---|---|---|
| **GET** | `/` | System health audit diagnostics. |
| **GET** | `/api/jobs` | Paginated listings with search parameters (`keyword`, `country`, `is_remote`, `visa_sponsorship`, `min_salary`). |
| **GET** | `/api/latest` | Real-time live feed of the 8 newest aggregated jobs. |
| **GET** | `/api/trending` | Top 6 tech tags and 5 popular job titles calculated dynamically. |
| **GET** | `/api/countries` | Country aggregates indicating open hiring counts and ISO flags. |
| **GET** | `/api/job/{id}` | Detailed specifications for a specific job listing. |
| **GET** | `/api/job/{id}/similar` | Content-based recommendations matching the target job using NLP weights. |
| **GET** | `/api/ai-search` | Conversational prompt parser, records search history, and queries database. |
| **GET** | `/api/analytics` | Core metrics (total counts, sources ratio) for the dashboard. |
| **POST** | `/api/saved` | Sync bookmark save actions to the database. |
| **DELETE**| `/api/saved/{id}` | Remove bookmarked saves from the database. |

---

## 🤖 Conversational AI NLP Heuristic Engine

The AI Search page (`frontend/pages/ai.html`) utilizes our custom NLP prompt parser.
When a user types: **`"Remote Python jobs in Japan under $3000"`**, the backend parses this prompt through:
1. **Work Style Identifiers:** Detects `remote`/`wfh` and filters `is_remote = True`.
2. **Geography Mapping:** Parses the keyword `"in Japan"`, querying for jobs matching country names or locations.
3. **Compensation Threshold:** Scans phrases like `"under $3000"`, identifying a value of `$3000`. Recognizes the small number as a monthly limit (junior roles) and sets bounds.
4. **Core Tech Overlap:** Discards common stopwords (`jobs`, `in`, `under`, `at`) and flags `"Python"` as a skill/title search criteria.

This provides an extremely high-performance, robust, and zero-latency conversational search mechanism without requiring external paid third-party API keys!
