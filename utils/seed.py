"""
DriveBD - Mock data generator.
Generates realistic, relational Bangladesh-style CSV data and seeds the SQLite DB.
Run directly: python -m utils.seed
"""
import os
import random
import datetime as dt
import pandas as pd
from faker import Faker

from utils.db import (
    init_db, get_session, User, Vehicle, Violation, Payment, Document,
    ServiceHistory, Notification, Appeal, ActivityLog, Setting, Base, engine
)
from utils.auth import hash_password

fake = Faker()
random.seed(42)
Faker.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

BD_FIRST_NAMES_M = ["Abdul", "Mohammad", "Rafiq", "Kamal", "Jahangir", "Shahidul", "Anisur",
                    "Habibur", "Nazrul", "Aminul", "Rakibul", "Shakil", "Tanvir", "Imran",
                    "Fahim", "Rezaul", "Golam", "Delwar", "Mizanur", "Saiful"]
BD_FIRST_NAMES_F = ["Fatema", "Rashida", "Nasrin", "Salma", "Shirin", "Rehana", "Taslima",
                    "Ayesha", "Farzana", "Sultana", "Rubina", "Nasima", "Shahnaz", "Roksana",
                    "Jesmin", "Mahmuda", "Parvin", "Lutfa", "Kamrun", "Halima"]
BD_LAST_NAMES = ["Islam", "Rahman", "Hossain", "Ahmed", "Khan", "Chowdhury", "Uddin", "Akter",
                 "Miah", "Talukder", "Sarkar", "Molla", "Bhuiyan", "Sheikh", "Mia", "Kazi"]

BD_DISTRICTS = [
    ("Dhaka", 23.8103, 90.4125), ("Chattogram", 22.3569, 91.7832), ("Khulna", 22.8456, 89.5403),
    ("Rajshahi", 24.3745, 88.6042), ("Sylhet", 24.8949, 91.8687), ("Barishal", 22.7010, 90.3535),
    ("Rangpur", 25.7439, 89.2752), ("Mymensingh", 24.7471, 90.4203), ("Comilla", 23.4607, 91.1809),
    ("Gazipur", 23.9999, 90.4203),
]

VEHICLE_MAKES = {
    "Car": ["Toyota", "Honda", "Hyundai", "Mitsubishi", "Suzuki"],
    "Motorcycle": ["Yamaha", "Honda", "Bajaj", "TVS", "Hero"],
    "Bus": ["Ashok Leyland", "Tata", "Hino"],
    "Truck": ["Tata", "Isuzu", "Hino"],
    "CNG": ["Bajaj RE"],
}
VEHICLE_MODELS = {
    "Toyota": ["Corolla", "Axio", "Premio", "Hiace"], "Honda": ["Civic", "City", "CB Shine"],
    "Hyundai": ["Elantra", "Tucson"], "Mitsubishi": ["Lancer", "Pajero"], "Suzuki": ["Alto", "Swift"],
    "Yamaha": ["FZ", "R15"], "Bajaj": ["Pulsar", "Discover", "RE"], "TVS": ["Apache"],
    "Hero": ["Splendor", "Hunk"], "Ashok Leyland": ["Viking"], "Tata": ["LPT 1613", "Ace"],
    "Hino": ["Ranger"], "Isuzu": ["Elf"],
}
VIOLATION_TYPES = [
    ("No Helmet", 500), ("Signal Breaking", 1000), ("Over Speeding", 2000),
    ("No Valid License", 3000), ("Illegal Parking", 800), ("Fitness Certificate Expired", 2500),
    ("Route Permit Violation", 3500), ("Overloading", 5000), ("Using Mobile While Driving", 1500),
    ("Fake Registration Plate", 10000), ("Tax Token Expired", 2000), ("No Insurance", 2500),
]
DOC_TYPES = ["NID", "Driving License", "Vehicle Registration", "Fitness Certificate", "Tax Token", "Insurance"]
WORKSHOPS = ["Dhaka Auto Care", "Chattogram Motor Works", "City Service Center", "Speed Fix Garage",
             "Rangpur Vehicle Clinic", "Elite Auto Service"]
SERVICE_TYPES = ["Engine Oil Change", "Brake Service", "Tire Replacement", "General Servicing",
                 "AC Repair", "Battery Replacement", "Full Inspection"]


def bd_name():
    if random.random() < 0.5:
        first = random.choice(BD_FIRST_NAMES_M)
    else:
        first = random.choice(BD_FIRST_NAMES_F)
    return f"{first} {random.choice(BD_LAST_NAMES)}"


def bd_nid():
    return "".join(str(random.randint(0, 9)) for _ in range(10))


def bd_license():
    return f"DL-{random.choice(['DHK','CTG','KHL','RAJ','SYL'])}-{random.randint(100000,999999)}"


def bd_reg_number():
    dist_code = random.choice(["DHAKA METRO", "CHATTOGRAM METRO", "SYLHET", "KHULNA", "RAJSHAHI"])
    letter = random.choice(["GA", "KA", "KHA", "GHA", "CHA"])
    return f"{dist_code}-{letter}-{random.randint(10,99)}-{random.randint(1000,9999)}"


def random_date(start_year=2022, end_year=2026):
    start = dt.date(start_year, 1, 1)
    end = dt.date(end_year, 7, 31)
    delta = (end - start).days
    return start + dt.timedelta(days=random.randint(0, delta))


def clear_tables(db):
    """Safely clear all tables in reverse dependency order."""
    try:
        # Delete in reverse order of dependencies
        db.query(ActivityLog).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Appeal).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Notification).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(ServiceHistory).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Document).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Payment).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Violation).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Vehicle).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(User).delete()
        db.commit()
    except:
        db.rollback()
    try:
        db.query(Setting).delete()
        db.commit()
    except:
        db.rollback()


def generate():
    # Create tables if they don't exist
    init_db()
    
    db = get_session()
    
    # Safe clear of existing data
    clear_tables(db)

    users_rows, vehicles_rows, violations_rows = [], [], []
    payments_rows, documents_rows, service_rows = [], [], []
    notifications_rows, appeals_rows, logs_rows = [], [], []

    # --- Admin account ---
    admin = User(name="System Admin", email="admin@drivebd.gov.bd",
                 password_hash=hash_password("Admin@123"), role="admin",
                 nid=bd_nid(), phone="01700000000")
    db.add(admin)
    db.flush()
    users_rows.append([admin.id, admin.name, admin.email, "admin", admin.nid, admin.phone, "", str(dt.date.today())])

    # --- Demo driver/owner account for easy login ---
    demo = User(name="Rafiq Islam (Demo)", email="demo@drivebd.gov.bd",
                password_hash=hash_password("Demo@123"), role="owner",
                nid=bd_nid(), phone="01711111111", license_no=bd_license())
    db.add(demo)
    db.flush()
    users_rows.append([demo.id, demo.name, demo.email, "owner", demo.nid, demo.phone, demo.license_no, str(dt.date.today())])

    all_users = [admin, demo]

    # --- 48 more regular users (drivers/owners) ---
    for _ in range(48):
        name = bd_name()
        email = f"{name.lower().replace(' ', '.')}{random.randint(1,999)}@example.com"
        role = random.choice(["driver", "owner", "owner", "driver"])
        u = User(
            name=name, email=email, password_hash=hash_password("Password@123"), role=role,
            nid=bd_nid(), phone=f"01{random.randint(300000000,999999999)}",
            license_no=bd_license() if role in ("driver", "owner") else "",
            created_at=dt.datetime.combine(random_date(2022, 2025), dt.time())
        )
        db.add(u)
        db.flush()
        all_users.append(u)
        users_rows.append([u.id, u.name, u.email, u.role, u.nid, u.phone, u.license_no, str(u.created_at.date())])

    db.commit()

    owner_like_users = [u for u in all_users if u.role in ("owner", "driver")]

    # --- 150 vehicles ---
    all_vehicles = []
    for _ in range(150):
        owner = random.choice(owner_like_users)
        vtype = random.choice(list(VEHICLE_MAKES.keys()))
        make = random.choice(VEHICLE_MAKES[vtype])
        model = random.choice(VEHICLE_MODELS.get(make, ["Standard"]))
        v = Vehicle(
            owner_id=owner.id, reg_number=bd_reg_number() + f"-{random.randint(1,9999)}",
            make=make, model=model, year=random.randint(2008, 2025), vehicle_type=vtype,
            engine_no=fake.bothify(text="ENG-########").upper(),
            chassis_no=fake.bothify(text="CHS-##########").upper(),
            status=random.choices(["active", "suspended", "scrapped"], weights=[85, 10, 5])[0],
            registered_on=random_date(2015, 2025),
        )
        db.add(v)
        db.flush()
        all_vehicles.append(v)
        vehicles_rows.append([v.id, v.owner_id, v.reg_number, v.make, v.model, v.year,
                              v.vehicle_type, v.engine_no, v.chassis_no, v.status, str(v.registered_on)])
    db.commit()

    # --- 300 violations ---
    all_violations = []
    for _ in range(300):
        vehicle = random.choice(all_vehicles)
        vtype, fine = random.choice(VIOLATION_TYPES)
        district, lat, lon = random.choice(BD_DISTRICTS)
        status = random.choices(["unpaid", "paid", "appealed", "waived"], weights=[35, 45, 15, 5])[0]
        viol = Violation(
            vehicle_id=vehicle.id, violation_type=vtype, date=random_date(2023, 2026),
            location=f"{district} - {fake.street_name()}",
            latitude=lat + random.uniform(-0.05, 0.05), longitude=lon + random.uniform(-0.05, 0.05),
            fine_amount=fine, status=status, officer_name=f"Officer {bd_name()}",
            notes=random.choice(["", "First offense", "Repeat offense", "Issued via mobile court",
                                 "Vehicle impounded briefly"])
        )
        db.add(viol)
        db.flush()
        all_violations.append(viol)
        violations_rows.append([viol.id, viol.vehicle_id, viol.violation_type, str(viol.date),
                                viol.location, viol.latitude, viol.longitude, viol.fine_amount,
                                viol.status, viol.officer_name, viol.notes])
    db.commit()

    # --- Payments (for paid violations) ---
    ref_counter = 100000
    for viol in all_violations:
        if viol.status == "paid":
            owner = viol.vehicle.owner_id
            ref_counter += 1
            p = Payment(
                violation_id=viol.id, user_id=owner, amount=viol.fine_amount,
                method=random.choice(["bKash", "Nagad", "Card", "Bank Transfer", "Rocket"]),
                date=viol.date + dt.timedelta(days=random.randint(0, 20)),
                status="completed", reference_no=f"TXN{ref_counter}"
            )
            db.add(p)
            db.flush()
            payments_rows.append([p.id, p.violation_id, p.user_id, p.amount, p.method,
                                  str(p.date), p.status, p.reference_no])
    db.commit()

    # --- Documents ---
    doc_id_counter = 0
    for owner in owner_like_users:
        owner_vehicles = [v for v in all_vehicles if v.owner_id == owner.id]
        num_docs = random.randint(1, 4)
        for _ in range(num_docs):
            doc_type = random.choice(DOC_TYPES)
            linked_vehicle = random.choice(owner_vehicles).id if owner_vehicles and doc_type != "NID" and doc_type != "Driving License" else None
            expiry = random_date(2025, 2027) if doc_type in ("Fitness Certificate", "Tax Token", "Insurance") else None
            status = "valid"
            if expiry:
                if expiry < dt.date.today():
                    status = "expired"
                elif (expiry - dt.date.today()).days < 60:
                    status = "expiring"
            d = Document(
                user_id=owner.id, vehicle_id=linked_vehicle, doc_type=doc_type,
                file_path=f"/documents/{owner.id}_{doc_type.replace(' ', '_')}.pdf",
                expiry_date=expiry, status=status, uploaded_on=random_date(2023, 2026)
            )
            db.add(d)
            db.flush()
            doc_id_counter += 1
            documents_rows.append([d.id, d.user_id, d.vehicle_id, d.doc_type, d.file_path,
                                   str(d.expiry_date) if d.expiry_date else "", d.status, str(d.uploaded_on)])
    db.commit()

    # --- Service history ---
    for vehicle in all_vehicles:
        if random.random() < 0.7:
            for _ in range(random.randint(1, 4)):
                s = ServiceHistory(
                    vehicle_id=vehicle.id, service_date=random_date(2023, 2026),
                    service_type=random.choice(SERVICE_TYPES), cost=random.randint(500, 15000),
                    workshop=random.choice(WORKSHOPS), mileage_km=random.randint(1000, 150000),
                    notes=random.choice(["", "Routine check", "Customer requested", "Under warranty"])
                )
                db.add(s)
                db.flush()
                service_rows.append([s.id, s.vehicle_id, str(s.service_date), s.service_type,
                                     s.cost, s.workshop, s.mileage_km, s.notes])
    db.commit()

    # --- Notifications ---
    notif_templates = [
        ("info", "Your document {doc} is due for renewal soon."),
        ("warning", "You have an unpaid fine of BDT {amt}."),
        ("alert", "Your vehicle fitness certificate has expired."),
        ("info", "Payment of BDT {amt} received successfully."),
        ("info", "Your appeal has been submitted for review."),
    ]
    for owner in owner_like_users:
        for _ in range(random.randint(1, 5)):
            cat, template = random.choice(notif_templates)
            msg = template.format(doc=random.choice(DOC_TYPES), amt=random.randint(500, 5000))
            n = Notification(
                user_id=owner.id, message=msg, category=cat,
                date=dt.datetime.combine(random_date(2024, 2026), dt.time(random.randint(0,23), random.randint(0,59))),
                is_read=random.choice([True, False])
            )
            db.add(n)
            db.flush()
            notifications_rows.append([n.id, n.user_id, n.message, n.category, str(n.date), n.is_read])
    db.commit()

    # --- Appeals (for appealed violations) ---
    for viol in all_violations:
        if viol.status == "appealed":
            a = Appeal(
                violation_id=viol.id, user_id=viol.vehicle.owner_id,
                reason=random.choice([
                    "I was not driving the vehicle at the time of the alleged violation.",
                    "The signage at the location was not clearly visible.",
                    "This fine was issued in error; documents were valid.",
                    "Vehicle was under authorized repair at the time.",
                ]),
                status=random.choices(["pending", "approved", "rejected"], weights=[50, 25, 25])[0],
                date=viol.date + dt.timedelta(days=random.randint(1, 15)),
                admin_comment=""
            )
            db.add(a)
            db.flush()
            appeals_rows.append([a.id, a.violation_id, a.user_id, a.reason, a.status,
                                 str(a.date), a.admin_comment])
    db.commit()

    # --- Activity logs ---
    for u in all_users[:30]:
        for _ in range(random.randint(1, 3)):
            log = ActivityLog(
                user_id=u.id, action=random.choice(["Logged in", "Updated profile", "Viewed vehicle",
                                                    "Made payment", "Uploaded document"]),
                timestamp=dt.datetime.combine(random_date(2024, 2026), dt.time())
            )
            db.add(log)
            db.flush()
            logs_rows.append([log.id, log.user_id, log.action, str(log.timestamp)])
    db.commit()

    # --- Settings ---
    default_settings = {
        "site_name": "DriveBD - Smart Driver & Vehicle Owner Portal",
        "support_email": "support@drivebd.gov.bd",
        "fine_grace_period_days": "15",
        "maintenance_mode": "false",
    }
    for k, v in default_settings.items():
        db.add(Setting(key=k, value=v))
    db.commit()
    db.close()

    # --- Write CSVs ---
    pd.DataFrame(users_rows, columns=["id", "name", "email", "role", "nid", "phone", "license_no", "created_at"]
                 ).to_csv(f"{DATA_DIR}/users.csv", index=False)
    pd.DataFrame(vehicles_rows, columns=["id", "owner_id", "reg_number", "make", "model", "year",
                 "vehicle_type", "engine_no", "chassis_no", "status", "registered_on"]
                 ).to_csv(f"{DATA_DIR}/vehicles.csv", index=False)
    pd.DataFrame(violations_rows, columns=["id", "vehicle_id", "violation_type", "date", "location",
                 "latitude", "longitude", "fine_amount", "status", "officer_name", "notes"]
                 ).to_csv(f"{DATA_DIR}/violations.csv", index=False)
    pd.DataFrame(payments_rows, columns=["id", "violation_id", "user_id", "amount", "method",
                 "date", "status", "reference_no"]).to_csv(f"{DATA_DIR}/payments.csv", index=False)
    pd.DataFrame(documents_rows, columns=["id", "user_id", "vehicle_id", "doc_type", "file_path",
                 "expiry_date", "status", "uploaded_on"]).to_csv(f"{DATA_DIR}/documents.csv", index=False)
    pd.DataFrame(service_rows, columns=["id", "vehicle_id", "service_date", "service_type", "cost",
                 "workshop", "mileage_km", "notes"]).to_csv(f"{DATA_DIR}/service_history.csv", index=False)
    pd.DataFrame(notifications_rows, columns=["id", "user_id", "message", "category", "date", "is_read"]
                 ).to_csv(f"{DATA_DIR}/notifications.csv", index=False)
    pd.DataFrame(appeals_rows, columns=["id", "violation_id", "user_id", "reason", "status", "date",
                 "admin_comment"]).to_csv(f"{DATA_DIR}/appeals.csv", index=False)
    pd.DataFrame(logs_rows, columns=["id", "user_id", "action", "timestamp"]
                 ).to_csv(f"{DATA_DIR}/activity_logs.csv", index=False)
    pd.DataFrame(list(default_settings.items()), columns=["key", "value"]
                 ).to_csv(f"{DATA_DIR}/settings.csv", index=False)

    print("Seed complete.")
    print(f"Users: {len(users_rows)} | Vehicles: {len(vehicles_rows)} | Violations: {len(violations_rows)}")
    print(f"Payments: {len(payments_rows)} | Documents: {len(documents_rows)} | Service records: {len(service_rows)}")
    print(f"Notifications: {len(notifications_rows)} | Appeals: {len(appeals_rows)} | Logs: {len(logs_rows)}")
    print("\nDemo login -> email: demo@drivebd.gov.bd | password: Demo@123")
    print("Admin login -> email: admin@drivebd.gov.bd | password: Admin@123")


if __name__ == "__main__":
    generate()
