drivebd/
├── app.py                     # Application entry point & UI
├── requirements.txt           # Python dependency list
├── .streamlit/                # Configuration files
│   └── config.toml            # Theme and UI settings
├── utils/                     # Backend logic
│   ├── db.py                  # SQLAlchemy models & database session
│   ├── auth.py                # Login logic, RBAC, and password hashing
│   ├── seed.py                # Faker data generation & seeding
│   └── pdf_utils.py           # ReportLab logic for receipts
├── pages/                     # Streamlit multi-page modules
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
└── data/                      # Generated CSV exports
