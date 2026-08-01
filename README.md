# 🚗 DriveBD — Smart Driver & Vehicle Owner Portal

A Streamlit web application simulating a national driver/vehicle-owner services portal for
Bangladesh: vehicle registration, traffic violations, fines/payments, document vault, service
history, notifications, appeals, an admin panel, reports, analytics, a mock BRTA API, and a
mock AI violation-detection demo.

> **Disclaimer:** This is a capstone/portfolio demo project. It is **not affiliated with,
> endorsed by, or connected to BRTA** (Bangladesh Road Transport Authority) or any government
> body. All data is synthetically generated and no real personal information is used.

---

## 1. Features

| Module | Description |
|---|---|
| Auth & RBAC | Email/password login, 3 roles: Driver, Owner, Admin |
| Dashboard | Role-aware summary metrics, recent activity |
| Vehicles | Register/view vehicles, update status |
| Violations | View/issue violations, map of violation locations |
| Payments | Pay fines (mock bKash/Nagad/Card/Bank), PDF receipt |
| Documents | Upload/track NID, License, Fitness Cert, Tax Token, Insurance with expiry status |
| Service History | Log and review vehicle servicing records |
| Notifications | In-app notification center |
| Appeals | File and track appeals against violations |
| Admin Panel | Manage users/roles, approve/reject appeals, view activity logs, edit settings |
| Reports | Export CSV/PDF reports for violations, payments, vehicles |
| Analytics | Charts: violations by type, status breakdown, trend over time, fines collected vs outstanding |
| Mock BRTA API | Simulated vehicle-fitness and license-verification lookups |
| AI Demo | Rule-based mock "violation detection" from an uploaded image (not real ML) |

---

## 2. Project Structure

```
drivebd/
├── app.py                     # Entry point: landing page + login/register
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Theme (blue/white)
├── utils/
│   ├── db.py                  # SQLAlchemy models + session
│   ├── auth.py                # Login, bcrypt hashing, RBAC helpers
│   ├── seed.py                # Generates CSVs + seeds the database
│   └── pdf_utils.py           # ReportLab PDF generation (receipts, reports)
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Vehicles.py
│   ├── 3_Violations.py
│   ├── 4_Payments.py
│   ├── 5_Documents.py
│   ├── 6_Service_History.py
│   ├── 7_Notifications.py
│   ├── 8_Appeals.py
│   ├── 9_Admin.py
│   ├── 10_Reports.py
│   ├── 11_Analytics.py
│   ├── 12_Mock_BRTA_API.py
│   └── 13_AI_Demo.py
└── data/                       # Generated CSVs (users, vehicles, violations, etc.)
```

The database itself is a single SQLite file, `drivebd.db`, created automatically on first run
in the project root (git-ignored — regenerate any time via the seed script).

---

## 3. Local Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone / unzip the project and enter it
cd drivebd

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate mock data + seed the database (creates drivebd.db and data/*.csv)
python -m utils.seed

# 5. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### Demo accounts (created by the seed script)

| Role | Email | Password |
|---|---|---|
| Admin | `admin@drivebd.gov.bd` | `Admin@123` |
| Owner | `demo@drivebd.gov.bd` | `Demo@123` |

48 additional random driver/owner accounts are also seeded, all using the password
`Password@123` (see `data/users.csv` for their emails).

### Re-seeding
Re-running `python -m utils.seed` wipes and regenerates all data — useful if you want a fresh
demo dataset. It is idempotent and safe to run repeatedly.

---

## 4. Deploying to Streamlit Community Cloud (free hosting)

1. **Push the project to GitHub.**
   Create a new repository (e.g. `drivebd`) and push this entire folder to it. Make sure
   `requirements.txt` is at the repo root.

   ```bash
   git init
   git add .
   git commit -m "Initial commit: DriveBD Streamlit app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/drivebd.git
   git push -u origin main
   ```

2. **Sign in to Streamlit Community Cloud.**
   Go to https://share.streamlit.io and sign in with your GitHub account.

3. **Create a new app.**
   - Click **"New app"**.
   - Select your repository, branch (`main`), and set the main file path to `app.py`.
   - Click **"Deploy"**.

4. **First-run database seeding.**
   Streamlit Cloud gives you an ephemeral filesystem, so `drivebd.db` won't exist yet. Either:
   - **Option A (simplest):** add this one-time snippet at the very top of `app.py` (already
     structured to support it) so the app seeds itself automatically if the DB is empty:
     ```python
     import os
     from utils.db import DB_PATH
     if not os.path.exists(DB_PATH):
         from utils.seed import generate
         generate()
     ```
     (Add this snippet right after the `init_db()` call in `app.py` if you want auto-seeding
     on Streamlit Cloud — it's omitted by default so local runs give you explicit control via
     `python -m utils.seed`.)
   - **Option B:** commit a pre-seeded `drivebd.db` file directly to the repo (simplest for a
     static demo, but data won't reset between deploys).

5. **Note on persistence.** Streamlit Community Cloud's filesystem is ephemeral — data written
   during a session (new users, payments, etc.) will not survive an app restart/redeploy. For a
   persistent production deployment, swap SQLite for a hosted Postgres database (e.g. Supabase,
   Neon, or Railway) by setting the `DATABASE_URL` environment variable in your Streamlit Cloud
   app's **Settings → Secrets**:
   ```toml
   DATABASE_URL = "postgresql://user:password@host:5432/dbname"
   ```
   `utils/db.py` already reads this environment variable automatically — no code changes needed.

6. **App is live** at `https://<your-app-name>.streamlit.app`.

---

## 5. Customization Notes

- **Theme colors** live in `.streamlit/config.toml` and the inline CSS block in `app.py`.
- **Add a new violation type / fine amount:** edit the `VIOLATION_TYPES` list in
  `utils/seed.py` (for seed data) and the `violation_type` selectbox in `pages/3_Violations.py`
  (for the live "Issue Violation" form).
- **Switch database engines:** set the `DATABASE_URL` environment variable (see above) — the
  SQLAlchemy models require no changes for Postgres/MySQL.
- **File uploads** (Documents module) currently store only a mock file path reference, not the
  actual file bytes, since Streamlit Cloud's filesystem is ephemeral. For real file storage,
  integrate an object store (e.g. Supabase Storage or AWS S3) inside `pages/5_Documents.py`.

---

## 6. Known Limitations (by design, as a demo)

- The "Mock BRTA API" and "AI Demo" pages are **simulations** — they do not call any real
  government system or computer-vision model.
- SQLite is used for simplicity; for concurrent multi-user production traffic, migrate to
  Postgres via `DATABASE_URL`.
- Document uploads are stored as path references only, not actual files.

---

## 7. License
This is a demo/capstone project provided as-is for educational and portfolio purposes.
