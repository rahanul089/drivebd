import streamlit as st
import pandas as pd
import random
import re
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="DriveBD - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

def nav_label(en, key=None):
    """English label for sidebar/nav buttons."""
    return en

# ================= MOCK DATABASE =================
class DriveDB:
    def __init__(self):
        self.users = []
        self.vehicles = []
        self.violations = []
        self.payments = []
        self.notifications = []
        self.documents = []
        self.service = []
        self.appeals = []
        self.activity = []
        self.seq = 1000
        self._seed_data()
    
    def _nid(self, prefix='u'):
        self.seq += 1
        return f"{prefix}{self.seq}"
    
    def _rand(self, arr):
        return arr[random.randint(0, len(arr)-1)]
    
    def _rand_int(self, a, b):
        return random.randint(a, b)
    
    def _fmt_date(self, d):
        return d.strftime("%Y-%m-%d")
    
    def _days_from_now(self, n):
        return datetime.now() + timedelta(days=n)
    
    def _money(self, n):
        return f"৳{n:,}"
    
    def _seed_data(self):
        # Users
        self.users.append({
            'id': 'u1', 'name': 'Rafiq Ahmed', 'email': 'driver@drivebd.gov.bd', 
            'password': 'Demo@123', 'role': 'driver', 'phone': '01711223344',
            'license': 'DHA-0234567', 'nid': '1995123456789', 
            'address': 'House 12, Road 5, Dhanmondi, Dhaka',
            'emergency': '01899887766', 'avatar': 'RA', 'status': 'active',
            'joined': '2025-02-10'
        })
        self.users.append({
            'id': 'u2', 'name': 'Nasrin Sultana', 'email': 'owner@drivebd.gov.bd',
            'password': 'Demo@123', 'role': 'owner', 'phone': '01822334455',
            'license': 'DHA-0987654', 'nid': '1990654321987',
            'address': 'Flat 4B, Gulshan Avenue, Dhaka',
            'emergency': '01911223344', 'avatar': 'NS', 'status': 'active',
            'joined': '2025-04-22'
        })
        self.users.append({
            'id': 'u3', 'name': 'System Admin', 'email': 'admin@drivebd.gov.bd',
            'password': 'Admin@123', 'role': 'admin', 'phone': '01700000000',
            'license': '—', 'nid': '—',
            'address': 'DriveBD HQ, Dhaka', 'emergency': '—',
            'avatar': 'SA', 'status': 'active', 'joined': '2024-11-01'
        })
        
        roles = ['driver', 'owner']
        for i in range(4, 15):
            r = self._rand(roles)
            self.users.append({
                'id': f'u{i}', 'name': f'User {i}', 
                'email': f'user{i}@mail.com', 'password': 'Demo@123',
                'role': r, 'phone': f"017{self._rand_int(10000000, 99999999)}",
                'license': f"DHA-0{self._rand_int(100000, 999999)}",
                'nid': str(self._rand_int(1000000000000, 9999999999999)),
                'address': 'Sample Address, Dhaka',
                'emergency': f"018{self._rand_int(10000000, 99999999)}",
                'avatar': f'U{i}', 'status': 'active' if random.random() > 0.9 else 'suspended',
                'joined': f"2025-0{self._rand_int(1,9)}-1{self._rand_int(0,9)}"
            })
        
        # Vehicles
        vi = ['DHAKA METRO GA 11-2481', 'DHAKA METRO HA 15-7723', 
              'CHATTOGRAM METRO KHA 22-0091', 'DHAKA METRO GA 33-5567',
              'SYLHET METRO GA 09-1234', 'DHAKA METRO LA 44-8890']
        vt = ['Private Car', 'Motorcycle', 'Private Car', 'Bus', 'Truck', 'Motorcycle']
        vo = ['u1', 'u1', 'u2', 'u2', 'u4', 'u5']
        man = ['Toyota', 'Yamaha', 'Toyota', 'Ashok Leyland', 'Tata', 'Bajaj']
        mod = ['Corolla Axio', 'X-Blade', 'Premio', 'Hino300', 'Isuzu', 'Pulsar']
        
        for i in range(6):
            self.vehicles.append({
                'id': f'v{i+1}', 'ownerId': vo[i], 'regNo': vi[i],
                'type': vt[i], 'manufacturer': man[i], 'model': mod[i],
                'engine': f'ENG{self._rand_int(100000, 999999)}',
                'chassis': f'CHS{self._rand_int(100000, 999999)}',
                'fuel': self._rand(['Petrol', 'Octane', 'Diesel', 'CNG']),
                'regDate': f"2022-0{self._rand_int(1,9)}-1{self._rand_int(0,9)}",
                'regExpiry': self._fmt_date(self._days_from_now(self._rand_int(-10, 700))),
                'taxExpiry': self._fmt_date(self._days_from_now(self._rand_int(-15, 120))),
                'fitnessExpiry': self._fmt_date(self._days_from_now(self._rand_int(-5, 90))),
                'insuranceExpiry': self._fmt_date(self._days_from_now(self._rand_int(10, 400))),
                'color': self._rand(['White', 'Black', 'Silver', 'Red', 'Blue']),
                'image': None, 'status': 'active',
                'mileage': self._rand_int(5000, 80000),
                'safety': self._rand_int(62, 98),
                'lastService': self._fmt_date(self._days_from_now(-self._rand_int(30, 180))),
                'serviceInterval': self._rand_int(3000, 8000)
            })
        
        # Violations - create more pending ones
        vtypes = ["Red Light Crossing", "Speeding", "Wrong Lane", "Illegal Parking",
                  "Helmet Violation", "Seat Belt Violation", "Wrong Direction", "Signal Violation"]
        locs = ["Gulshan Circle 1, Dhaka", "Mirpur 10, Dhaka", "Motijheel C/A, Dhaka",
                "Uttara Sector 7, Dhaka", "GEC Circle, Chattogram", "Zindabazar, Sylhet",
                "Shahbagh, Dhaka", "Farmgate, Dhaka"]
        officers = ["Insp. M. Karim", "Sgt. F. Rahman", "Insp. S. Hossain", "Sgt. A. Islam"]
        
        for i in range(30):  # More violations
            veh = self._rand(self.vehicles)
            # More pending violations
            status = self._rand(['pending', 'pending', 'pending', 'paid'])
            self.violations.append({
                'id': f'vi{i}', 'violationNo': f'VLN-2026-{1000+i}',
                'vehicleId': veh['id'], 'vehicleNo': veh['regNo'],
                'driverName': next((u['name'] for u in self.users if u['id'] == veh['ownerId']), 'Unknown'),
                'type': self._rand(vtypes),
                'date': self._fmt_date(self._days_from_now(-self._rand_int(1, 90))),
                'time': f"{self._rand_int(6,22)}:{str(self._rand_int(0,59)).zfill(2)}",
                'location': self._rand(locs),
                'lat': f"{23.7 + random.random() * 0.15:.4f}",
                'lng': f"{90.35 + random.random() * 0.15:.4f}",
                'evidence': None,
                'description': 'Detected via traffic monitoring camera at checkpoint.',
                'fine': self._rand([500, 1000, 1500, 2000, 3000]),
                'officer': self._rand(officers),
                'status': status
            })
        
        # Payments
        paid_violations = [v for v in self.violations if v['status'] == 'paid']
        for i, v in enumerate(paid_violations[:15]):  # More payments
            self.payments.append({
                'id': f'p{i}', 'violationId': v['id'],
                'violationNo': v['violationNo'],
                'method': self._rand(['bKash', 'Nagad', 'Card', 'Cash']),
                'amount': v['fine'],
                'date': self._fmt_date(self._days_from_now(-self._rand_int(1, 60))),
                'status': 'completed',
                'receiptNo': f'RCPT-{self._rand_int(100000, 999999)}',
                'transactionId': f'TXN-{self._rand_int(100000, 999999)}',
                'paymentMethod': self._rand(['bKash', 'Nagad', 'Card', 'Cash'])
            })
        
        # Notifications
        notifs = [
            ('reminder', 'Road tax expiring soon',
             'Your vehicle DHAKA METRO GA 11-2481 road tax expires in 12 days.'),
            ('violation', 'New violation recorded',
             'A speeding violation was recorded against DHAKA METRO HA 15-7723.'),
            ('payment', 'Payment received',
             'Your payment of ৳1500 for VLN-2026-1004 was confirmed.'),
            ('reminder', 'Fitness certificate due',
             'Fitness certificate for CHATTOGRAM METRO KHA 22-0091 expires soon.'),
            ('system', 'Welcome to DriveBD',
             'Your account has been created successfully.'),
            ('reminder', 'Insurance renewal',
             'Insurance for DHAKA METRO GA 33-5567 renews in 30 days.'),
            ('violation', 'Appeal update',
             'Your appeal for VLN-2026-1002 is under review.'),
            ('payment', 'Receipt available',
             'Download your receipt for RCPT payment anytime from Payments.'),
            ('reminder', 'Service due', 
             'Your vehicle DHAKA METRO GA 11-2481 is due for servicing.'),
            ('violation', 'New violation recorded',
             'A parking violation was recorded against DHAKA METRO LA 44-8890.'),
            ('system', 'Document reminder',
             'Your insurance document for DHAKA METRO GA 33-5567 is expiring soon.'),
        ]
        owner_notifs = [
            ('reminder', 'Fitness certificate due',
             'Fitness certificate for one of your vehicles expires soon.'),
            ('payment', 'Payment received',
             'A fine payment on your fleet was confirmed.'),
            ('system', 'Welcome to DriveBD',
             'Your account has been created successfully.'),
        ]
        admin_notifs = [
            ('system', 'New appeal submitted',
             'A driver has submitted an appeal that needs review.'),
            ('system', 'New account registered',
             'A new driver/owner account was created on the platform.'),
            ('system', 'Welcome to DriveBD',
             'Your admin account is ready.'),
        ]
        n_id = 0
        for uid, notif_set in (('u1', notifs), ('u2', owner_notifs), ('u3', admin_notifs)):
            for i, n in enumerate(notif_set):
                self.notifications.append({
                    'id': f'n{n_id}', 'userId': uid, 'category': n[0],
                    'title': n[1], 'message': n[2],
                    'read': i > 6,
                    'date': self._fmt_date(self._days_from_now(-i * 2))
                })
                n_id += 1
        
        # Service history
        for i in range(15):
            veh = self._rand(self.vehicles)
            service_types = ['Oil Change', 'Engine Service', 'Tyre Change',
                           'Battery Replacement', 'Brake Service', 'Full Service',
                           'Wheel Alignment', 'AC Service', 'Transmission Service']
            service_type = self._rand(service_types)
            service_date = self._days_from_now(-self._rand_int(10, 200))
            current_mileage = veh.get('mileage', 5000) + self._rand_int(-2000, 2000)
            
            cost_map = {
                'Oil Change': (800, 1500),
                'Engine Service': (3000, 6000),
                'Tyre Change': (4000, 8000),
                'Battery Replacement': (2000, 3500),
                'Brake Service': (1500, 3000),
                'Full Service': (5000, 10000),
                'Wheel Alignment': (1000, 2000),
                'AC Service': (1500, 3000),
                'Transmission Service': (4000, 8000)
            }
            min_cost, max_cost = cost_map.get(service_type, (500, 3000))
            
            self.service.append({
                'id': f's{i}', 'vehicleId': veh['id'],
                'vehicleNo': veh['regNo'],
                'type': service_type,
                'date': self._fmt_date(service_date),
                'mileage': max(0, current_mileage),
                'cost': self._rand_int(min_cost, max_cost),
                'notes': self._rand([
                    'Routine maintenance completed at authorized service center.',
                    'Parts replaced with genuine components.',
                    'Service completed with inspection report.',
                    'Recommended next service in 5000 km.',
                    'All systems checked and operating normally.'
                ]),
                'serviceCenter': self._rand([
                    'Toyota Service Center, Dhaka',
                    'Yamaha Service Center, Dhaka',
                    'Auto Care Workshop, Chattogram',
                    'Mechanic Pro, Sylhet',
                    'Car Service BD, Dhaka'
                ])
            })
        
        # Activity
        self.activity = [
            {'icon': '🚗', 'text': 'Vehicle DHAKA METRO GA 11-2481 added to your account',
             'time': '2 days ago'},
            {'icon': '🧾', 'text': 'Violation VLN-2026-1004 marked as paid',
             'time': '4 days ago'},
            {'icon': '📄', 'text': 'Insurance document uploaded for HA 15-7723',
             'time': '6 days ago'},
            {'icon': '🔔', 'text': 'Reminder sent: road tax expiring in 12 days',
             'time': '1 week ago'},
            {'icon': '🔧', 'text': 'Service record added for DHAKA METRO GA 11-2481',
             'time': '2 weeks ago'},
        ]

# ================= DATABASE INSTANCE =================
@st.cache_resource
def get_db():
    return DriveDB()

db = get_db()

# ================= AUTH FUNCTIONS =================
def _normalize_email(email):
    return (email or "").strip().lower()

def login_user(email, password):
    email = _normalize_email(email)
    user = next((u for u in db.users if u['email'].lower() == email), None)
    if not user:
        return False, "No account found with that email."
    if user['password'] != password:
        return False, "Incorrect password."
    if user['status'] != 'active':
        return False, "This account has been suspended. Contact an administrator."
    st.session_state.user = user
    return True, "Logged in successfully!"

def logout_user():
    st.session_state.user = None
    st.session_state.page = 'landing'
    st.rerun()

def register_user(name, email, password, role, phone='', nid=''):
    email = _normalize_email(email)
    if not email:
        return False, "A valid email is required."
    if any(u['email'].lower() == email for u in db.users):
        return False, "An account with this email already exists"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    user = {
        'id': db._nid('u'), 'name': name.strip(), 'email': email,
        'password': password, 'role': role, 'phone': phone or '',
        'license': 'PENDING', 'nid': nid or 'PENDING',
        'address': '', 'emergency': '',
        'avatar': ''.join([s[0] for s in name.split()])[:2].upper() if name.strip() else 'U',
        'status': 'active',
        'joined': db._fmt_date(datetime.now())
    }
    db.users.append(user)
    st.session_state.user = user
    return True, "Account created successfully!"

def current_user():
    return st.session_state.get('user')

def is_logged_in():
    return st.session_state.get('user') is not None

def make_admin(user_id):
    """Make a user an admin"""
    user = next((u for u in db.users if u['id'] == user_id), None)
    if user:
        user['role'] = 'admin'
        db.notifications.append({
            'id': db._nid('n'),
            'userId': user['id'],
            'category': 'system',
            'title': 'Admin Privileges Granted',
            'message': 'You have been promoted to Admin. You can now manage users, appeals, and system settings.',
            'read': False,
            'date': db._fmt_date(datetime.now())
        })
        return True
    return False

# ================= HELPER FUNCTIONS =================
def get_my_vehicles():
    user = current_user()
    if user['role'] == 'admin':
        return db.vehicles
    return [v for v in db.vehicles if v['ownerId'] == user['id']]

def get_vehicle_ids():
    return [v['id'] for v in get_my_vehicles()]

def get_my_violations():
    user = current_user()
    if user['role'] == 'admin':
        return db.violations
    ids = get_vehicle_ids()
    return [v for v in db.violations if v['vehicleId'] in ids]

def get_my_payments():
    vids = [v['id'] for v in get_my_violations()]
    if current_user()['role'] == 'admin':
        return db.payments
    return [p for p in db.payments if p['violationId'] in vids]

def get_my_documents():
    ids = get_vehicle_ids()
    if current_user()['role'] == 'admin':
        return db.documents
    return [d for d in db.documents if d['vehicleId'] in ids]

def get_my_service():
    ids = get_vehicle_ids()
    if current_user()['role'] == 'admin':
        return db.service
    return [s for s in db.service if s['vehicleId'] in ids]

def get_my_appeals():
    vios = [v['id'] for v in get_my_violations()]
    return [a for a in db.appeals if a['violationId'] in vios]

def owner_name(veh_id):
    v = next((v for v in db.vehicles if v['id'] == veh_id), None)
    if v:
        u = next((u for u in db.users if u['id'] == v['ownerId']), None)
        return u['name'] if u else 'Unknown'
    return 'Unknown'

def status_badge(status):
    colors = {
        'pending': 'badge-amber',
        'paid': 'badge-green',
        'appealed': 'badge-navy',
        'waived': 'badge-green',
        'approved': 'badge-green',
        'rejected': 'badge-red',
        'processing': 'badge-blue'
    }
    return f'<span class="badge {colors.get(status, "badge-navy")}">{status}</span>'

def exp_badge(date_str):
    try:
        days = (datetime.strptime(date_str, "%Y-%m-%d") - datetime.now()).days
        if days < 0:
            return '<span class="badge badge-red">Expired</span>'
        if days < 30:
            return f'<span class="badge badge-amber">{days}d left</span>'
        return '<span class="badge badge-green">OK</span>'
    except:
        return '<span class="badge badge-navy">N/A</span>'

# ================= COLORFUL CSS =================
def load_css():
    st.markdown("""
    <style>
    /* ============ TOKENS ============ */
    :root {
      --navy: #0B2545;
      --navy-2: #123063;
      --green: #046A38;
      --green-l: #0C8A4C;
      --red: #C8102E;
      --amber: #B4740E;
      --paper: #F6F7F5;
      --card: #FFFFFF;
      --ink: #16233A;
      --muted: #5B6B82;
      --border: #E2E6EA;
      --radius: 14px;
      --shadow: 0 1px 2px rgba(11,37,69,.06), 0 8px 24px -12px rgba(11,37,69,.18);
      --font-d: 'Sora', sans-serif;
      --font-b: 'Inter', sans-serif;
      --font-m: 'JetBrains Mono', monospace;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    /* ============ SIDEBAR STYLING ============ */
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #0B2545 0%, #1a3a6b 60%, #2d5a8e 100%);
    }
    
    [data-testid="stSidebar"] .stButton button {
      background: rgba(255,255,255,0.08) !important;
      border: 1px solid rgba(255,255,255,0.12) !important;
      color: rgba(255,255,255,0.85) !important;
      border-radius: 10px !important;
      transition: all 0.3s ease !important;
      font-weight: 500 !important;
      padding: 10px 14px !important;
      margin: 2px 0 !important;
      text-align: left !important;
      justify-content: flex-start !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
      background: rgba(255,255,255,0.18) !important;
      border-color: rgba(255,255,255,0.3) !important;
      transform: translateX(4px) !important;
    }
    
    [data-testid="stSidebar"] .stButton button[data-baseweb="button"] {
      background: rgba(255,255,255,0.15) !important;
      border-color: rgba(255,255,255,0.25) !important;
      color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
      color: rgba(255,255,255,0.6) !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      margin-top: 12px !important;
      padding: 0 4px !important;
    }
    
    .sidebar-profile {
      text-align: center;
      padding: 20px 0 16px 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      margin-bottom: 8px;
    }
    
    .sidebar-profile .avatar {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 10px;
      font-size: 24px;
      font-weight: 700;
      border: 3px solid rgba(255,255,255,0.2);
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .sidebar-profile .name {
      color: #FFFFFF;
      font-weight: 600;
      font-size: 16px;
    }
    
    .sidebar-profile .role {
      color: rgba(255,255,255,0.6);
      font-size: 12px;
    }
    
    .logout-btn {
      margin-top: 20px !important;
    }
    .logout-btn button {
      background: rgba(200,16,46,0.2) !important;
      border-color: rgba(200,16,46,0.3) !important;
      color: #ff6b6b !important;
    }
    .logout-btn button:hover {
      background: rgba(200,16,46,0.35) !important;
      border-color: rgba(200,16,46,0.5) !important;
    }
    
    .main-header { font-size: 2.4rem; font-weight: 700; color: var(--navy); margin-bottom: 0; font-family: 'Sora', sans-serif; }
    .sub-header { color: #555; font-size: 1.05rem; margin-top: 0; }
    
    /* ============ COLORFUL METRIC CARDS - DARKER SHADES ============ */
    .metric-card {
      padding: 20px 18px;
      border-radius: 16px;
      border: none;
      color: white;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.3s ease;
      min-height: 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .metric-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 16px 48px rgba(0,0,0,0.2);
    }
    .metric-card .metric-icon {
      font-size: 32px;
      opacity: 0.2;
      position: absolute;
      right: 16px;
      bottom: 12px;
    }
    .metric-card .metric-value {
      font-size: 32px;
      font-weight: 700;
      font-family: 'Sora', sans-serif;
      display: block;
      margin-top: 4px;
      letter-spacing: -0.5px;
    }
    .metric-card .metric-label {
      font-size: 13px;
      opacity: 0.85;
      font-weight: 500;
      letter-spacing: 0.3px;
    }
    /* Darker shades for metric cards */
    .metric-card-green-dark { 
      background: linear-gradient(135deg, #0d5c3e 0%, #1a8a5a 100%); 
      box-shadow: 0 4px 16px rgba(13,92,62,0.4);
    }
    .metric-card-blue-dark { 
      background: linear-gradient(135deg, #1a3a7a 0%, #4a6fa5 100%); 
      box-shadow: 0 4px 16px rgba(26,58,122,0.4);
    }
    .metric-card-orange-dark { 
      background: linear-gradient(135deg, #8b2f4a 0%, #c0395a 100%); 
      box-shadow: 0 4px 16px rgba(139,47,74,0.4);
    }
    .metric-card-purple-dark { 
      background: linear-gradient(135deg, #4a2a7a 0%, #7a5aaa 100%); 
      box-shadow: 0 4px 16px rgba(74,42,122,0.4);
    }
    .metric-card-teal-dark { 
      background: linear-gradient(135deg, #0d4a5a 0%, #1a7a8a 100%); 
      box-shadow: 0 4px 16px rgba(13,74,90,0.4);
    }
    .metric-card-pink-dark { 
      background: linear-gradient(135deg, #7a2a4a 0%, #b84a6a 100%); 
      box-shadow: 0 4px 16px rgba(122,42,74,0.4);
    }
    .metric-card-red-dark { 
      background: linear-gradient(135deg, #7a1a2a 0%, #b82a3a 100%); 
      box-shadow: 0 4px 16px rgba(122,26,42,0.4);
    }
    .metric-card-navy-dark { 
      background: linear-gradient(135deg, #0a1a3a 0%, #1a3a6a 100%); 
      box-shadow: 0 4px 16px rgba(10,26,58,0.4);
    }
    
    /* Grid for metric cards with proper spacing */
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }
    
    /* ============ WELCOME BANNER ============ */
    .welcome-banner {
      background: linear-gradient(135deg, #0B2545 0%, #1a3a6b 50%, #2d5a8e 100%);
      border-radius: 16px;
      padding: 30px 40px;
      color: white;
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 8px 32px rgba(11,37,69,0.3);
    }
    .welcome-banner::before {
      content: '🚗';
      position: absolute;
      right: 40px;
      bottom: -20px;
      font-size: 120px;
      opacity: 0.08;
    }
    .welcome-banner h2 {
      font-family: 'Sora', sans-serif;
      font-size: 28px;
      font-weight: 700;
    }
    .welcome-banner p {
      opacity: 0.85;
      font-size: 15px;
      margin-top: 4px;
    }
    
    /* ============ QUICK ACTION GRID ============ */
    .quick-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin: 16px 0 24px 0;
    }
    .quick-item {
      background: white;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 10px;
      text-align: center;
      transition: all 0.3s ease;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      color: var(--ink);
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .quick-item:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 32px rgba(0,0,0,0.1);
      border-color: var(--green);
    }
    .quick-item .qi-icon {
      font-size: 28px;
      display: block;
      margin-bottom: 6px;
    }
    .quick-item.qi-green { border-left: 4px solid var(--green); }
    .quick-item.qi-blue { border-left: 4px solid #667eea; }
    .quick-item.qi-orange { border-left: 4px solid #f5576c; }
    .quick-item.qi-purple { border-left: 4px solid #a18cd1; }
    .quick-item.qi-teal { border-left: 4px solid #4facfe; }
    .quick-item.qi-pink { border-left: 4px solid #fa709a; }
    
    /* ============ BADGES ============ */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 12px;
      border-radius: 100px;
      font-size: 11.5px;
      font-weight: 600;
    }
    .badge-green { background: rgba(4,106,56,.12); color: var(--green); }
    .badge-red { background: rgba(200,16,46,.12); color: var(--red); }
    .badge-amber { background: rgba(180,116,14,.14); color: var(--amber); }
    .badge-navy { background: rgba(11,37,69,.1); color: var(--navy); }
    .badge-blue { background: rgba(102,126,234,.12); color: #667eea; }
    .badge-purple { background: rgba(161,140,209,.15); color: #764ba2; }
    
    /* ============ STAT CARDS ============ */
    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      background: white;
      transition: all 0.2s ease;
    }
    .stat-card:hover {
      box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    
    .mono { font-family: 'JetBrains Mono', monospace; }
    
    .panel {
      background: white;
      border: 1px solid #E2E6EA;
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 20px;
      transition: all 0.2s ease;
    }
    .panel:hover {
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    
    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    
    .panel-head h3 { font-size: 15.5px; margin: 0; }
    
    .page-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 22px;
      flex-wrap: wrap;
      gap: 12px;
    }
    
    .page-head h2 { font-size: 23px; margin: 0; }
    .page-head p { color: var(--muted); font-size: 13.5px; margin-top: 4px; }
    
    .page-help {
      background: rgba(4,106,56,.05);
      border-left: 3px solid var(--green);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 20px;
      font-size: 13.5px;
      line-height: 1.55;
      color: var(--ink);
    }
    .page-help b { color: var(--navy); }
    .page-help ul { margin: 6px 0 0 18px; padding: 0; }
    .page-help li { margin-bottom: 3px; }
    
    .empty {
      text-align: center;
      padding: 50px 20px;
      color: var(--muted);
    }
    
    .vcard {
      width: 100%;
      max-width: 400px;
      aspect-ratio: 1.58/1;
      margin: 0 auto;
      position: relative;
      border-radius: 18px;
      padding: 22px;
      background: linear-gradient(135deg, #0F3D66, #0B2545 60%, #052A44);
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    
    .vcard .chip {
      width: 38px;
      height: 28px;
      border-radius: 6px;
      background: linear-gradient(135deg, #E8C36A, #B8933D);
    }
    
    .vcard .num {
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 3px;
      font-size: 19px;
      margin-top: 18px;
    }
    
    .vcard .row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #9FB2CC;
      text-transform: uppercase;
      letter-spacing: .5px;
    }
    
    .vcard .row b {
      display: block;
      color: #fff;
      font-size: 13px;
      text-transform: none;
      font-family: 'Sora', sans-serif;
      margin-top: 2px;
    }
    
    .vcard .top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    
    .s-ic {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .stat-card b {
      display: block;
      font-size: 24px;
      font-family: 'Sora', sans-serif;
      margin-top: 10px;
    }
    .stat-card span { font-size: 12.5px; color: var(--muted); }
    
    .doc-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }
    
    .doc-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      text-align: center;
      background: white;
    }
    
    .doc-card .thumb {
      height: 90px;
      border-radius: 8px;
      background: var(--paper);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      overflow: hidden;
    }
    
    .doc-card b { font-size: 12.5px; display: block; }
    .doc-card span { font-size: 11px; color: var(--muted); }
    .doc-actions { display: flex; gap: 6px; margin-top: 10px; justify-content: center; }
    
    .notif-item {
      display: flex;
      gap: 12px;
      padding: 14px 6px;
      border-bottom: 1px solid var(--border);
      align-items: flex-start;
    }
    
    .notif-item.unread { background: rgba(4,106,56,.04); }
    
    .notif-ic {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    
    .notif-item b { font-size: 13.5px; display: block; }
    .notif-item p { font-size: 12.5px; color: var(--muted); margin-top: 2px; }
    .notif-item .time { font-size: 11px; color: var(--muted); margin-left: auto; white-space: nowrap; }
    
    .timeline {
      list-style: none;
      padding-left: 0;
    }
    
    .timeline li {
      position: relative;
      padding-left: 28px;
      padding-bottom: 20px;
      border-left: 2px solid var(--border);
      margin-left: 8px;
    }
    
    .timeline li:last-child { border-color: transparent; padding-bottom: 0; }
    
    .timeline li::before {
      content: '';
      position: absolute;
      left: -7px;
      top: 0;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--green);
      border: 2px solid white;
    }
    
    .timeline b { font-size: 13px; display: block; }
    .timeline span { font-size: 12px; color: var(--muted); }
    
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }
    th {
      text-align: left;
      padding: 10px 12px;
      color: var(--muted);
      font-weight: 600;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: .4px;
      border-bottom: 1px solid var(--border);
    }
    td {
      padding: 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tbody tr:hover { background: rgba(4,106,56,.04); }
    
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    
    .field { margin-bottom: 16px; }
    .field label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 6px;
    }
    
    .field input, .field select, .field textarea {
      width: 100%;
      padding: 11px 13px;
      border: 1px solid var(--border);
      border-radius: 9px;
      background: var(--paper);
      color: var(--ink);
      font-family: 'Inter', sans-serif;
      font-size: 14px;
    }
    
    .field input:focus, .field select:focus, .field textarea:focus {
      outline: 2px solid var(--green);
      outline-offset: 1px;
    }
    
    .hero-stats {
      display: flex;
      gap: 34px;
      margin-top: 20px;
    }
    
    .hero-stats div b {
      display: block;
      font-family: 'Sora', sans-serif;
      font-size: 24px;
      color: var(--navy);
    }
    .hero-stats div span {
      font-size: 12.5px;
      color: var(--muted);
    }
    
    .service-card {
      border-left: 3px solid var(--green);
      padding-left: 12px;
      margin-bottom: 8px;
    }
    
    .service-card .cost {
      font-weight: 600;
      color: var(--green);
    }
    
    .payment-method {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
    }
    .payment-method.bkash { background: #E2175B22; color: #E2175B; }
    .payment-method.nagad { background: #FF6B0022; color: #FF6B00; }
    .payment-method.card { background: #667eea22; color: #667eea; }
    .payment-method.cash { background: #11998e22; color: #11998e; }
    
    /* ============ RESPONSIVE ============ */
    @media (max-width: 1000px) {
      .grid-cards { grid-template-columns: repeat(2, 1fr); }
      .two-col { grid-template-columns: 1fr; }
      .form-grid { grid-template-columns: 1fr; }
      .doc-grid { grid-template-columns: repeat(2, 1fr); }
      .quick-grid { grid-template-columns: repeat(2, 1fr); }
      .metric-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .quick-grid { grid-template-columns: repeat(2, 1fr); }
      .metric-card .metric-value { font-size: 22px; }
      .welcome-banner { padding: 20px; }
      .metric-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# ================= UI ROUTES =================
def render_landing():
    # [Landing page code - kept the same]
    st.markdown("""
    <div style="padding: 40px 0;">
        <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 60px; align-items: center; max-width: 1280px; margin: 0 auto;">
            <div>
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(4,106,56,.12); border: 1px solid rgba(12,138,76,.3); color: #046A38; font-size: 12.5px; font-weight: 600; padding: 6px 14px; border-radius: 100px; margin-bottom: 22px;">
                    ● Citizen platform · not affiliated with BRTA or Police
                </div>
                <h1 style="font-size: clamp(34px, 4.2vw, 54px); font-weight: 800; line-height: 1.08; letter-spacing: -0.5px; font-family: 'Sora', sans-serif;">
                    Your vehicle, your fines,<br>your papers — <span style="color: #046A38;">in one place.</span>
                </h1>
                <p style="margin-top: 14px; font-size: 17px; color: #5B6B82; max-width: 520px;">
                    DriveBD helps drivers and owners across Bangladesh track violations, store documents, 
                    catch renewal deadlines before they lapse, and pay fines without standing in a line.
                </p>
                <div style="display: flex; gap: 14px; margin-top: 34px; flex-wrap: wrap;">
                    <a href="#get-started" 
                       style="background: #046A38; color: white; border: none; border-radius: 10px; padding: 12px 24px; font-weight: 600; font-size: 14px; cursor: pointer; text-decoration: none; display: inline-block;">
                        Create free account
                    </a>
                </div>
                <div class="hero-stats">
                    <div><b class="mono">150+</b><span>Vehicles tracked</span></div>
                    <div><b class="mono">300+</b><span>Violations logged</span></div>
                    <div><b class="mono">৳12L+</b><span>Fines settled</span></div>
                </div>
            </div>
            <div>
                <div class="vcard">
                    <div class="top">
                        <div class="chip"></div>
                        <b style="font-size:11px; letter-spacing:2px;">DIGITAL VEHICLE CARD</b>
                    </div>
                    <div>
                        <div class="num">DHK · METRO · GA 11‑2481</div>
                        <div class="row" style="margin-top:16px;">
                            <span>Owner<b>Rafiq Ahmed</b></span>
                            <span>Type<b>Private Car</b></span>
                            <span>Valid till<b>Dec 2026</b></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 60px 0;">
        <div style="text-align: center; max-width: 640px; margin: 0 auto 56px;">
            <span style="color: #046A38; font-weight: 700; font-size: 12.5px; letter-spacing: 1.5px; text-transform: uppercase;">Features</span>
            <h2 style="font-size: clamp(26px, 3vw, 38px); margin-top: 10px; letter-spacing: -0.3px; font-family: 'Sora', sans-serif;">
                Everything a vehicle owner actually needs
            </h2>
            <p style="color: #5B6B82; margin-top: 14px; font-size: 15.5px;">
                Built around the paperwork and deadlines that pile up once you own a vehicle in Bangladesh.
            </p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; max-width: 1200px; margin: 0 auto;">
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">🚗</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Multi‑vehicle registry</h4>
                <p style="font-size: 14px; color: #5B6B82;">Register cars, motorcycles, buses and trucks with full document details in one place.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">⚠</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Violation tracking</h4>
                <p style="font-size: 14px; color: #5B6B82;">See every fine issued against your vehicles with evidence, location and officer details.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">💳</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Instant fine payment</h4>
                <p style="font-size: 14px; color: #5B6B82;">Pay via bKash, Nagad, card or cash and get a receipt immediately.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">📁</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Document vault</h4>
                <p style="font-size: 14px; color: #5B6B82;">Store your licence, registration, fitness and insurance papers securely.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">⏰</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Renewal reminders</h4>
                <p style="font-size: 14px; color: #5B6B82;">Automatic alerts before tax, fitness or insurance expiry dates.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">📊</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Service history</h4>
                <p style="font-size: 14px; color: #5B6B82;">Log every oil change, tyre swap and service visit against mileage.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 60px 0; background: #0B2545; color: white; border-radius: 14px; margin: 20px 0;">
        <div style="text-align: center; max-width: 640px; margin: 0 auto 56px;">
            <span style="color: #8CE0AE; font-weight: 700; font-size: 12.5px; letter-spacing: 1.5px; text-transform: uppercase;">Benefits</span>
            <h2 style="font-size: clamp(26px, 3vw, 38px); margin-top: 10px; letter-spacing: -0.3px; font-family: 'Sora', sans-serif; color: white;">
                Built for how people actually manage vehicles here
            </h2>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; max-width: 1200px; margin: 0 auto;">
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">No more paper folders</b>
                <span style="font-size: 13px; color: #AEBEDA;">Every document lives in one secure vault, accessible anywhere.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Never miss a deadline</b>
                <span style="font-size: 13px; color: #AEBEDA;">Reminders arrive weeks before expiry, not the day of.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Pay fines from your phone</b>
                <span style="font-size: 13px; color: #AEBEDA;">No queues — settle a fine in under a minute.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Built around local roads</b>
                <span style="font-size: 13px; color: #AEBEDA;">Violation types and locations reflect real Bangladesh traffic patterns.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    """Enhanced colorful dashboard with proper spacing and darker shades"""
    user = current_user()
    vehicles = get_my_vehicles()
    violations = get_my_violations()
    pending = [v for v in violations if v['status'] == 'pending']
    paid = [v for v in violations if v['status'] == 'paid']
    my_notifs = db.notifications if user['role'] == 'admin' else [n for n in db.notifications if n['userId'] == user['id']]
    notifs = [n for n in my_notifs if not n.get('read', False)]
    docs = get_my_documents()
    service_records = get_my_service()
    
    total_fine_value = sum(v['fine'] for v in pending)
    total_paid_value = sum(v['fine'] for v in paid)
    
    expiring_soon = []
    for v in vehicles:
        try:
            tax_days = (datetime.strptime(v['taxExpiry'], "%Y-%m-%d") - datetime.now()).days
            fitness_days = (datetime.strptime(v['fitnessExpiry'], "%Y-%m-%d") - datetime.now()).days
            insurance_days = (datetime.strptime(v['insuranceExpiry'], "%Y-%m-%d") - datetime.now()).days
            if tax_days < 30 or fitness_days < 30 or insurance_days < 30:
                expiring_soon.append(v)
        except:
            pass
    
    first_name = user['name'].split()[0] if user.get('name') else 'there'

    # Welcome Banner
    st.markdown(f"""
    <div class="welcome-banner">
        <div>
            <h2>👋 Hello, {first_name}!</h2>
            <p>Your unified digital gateway for vehicle management, violations tracking, and document storage.</p>
            <div style="display: flex; gap: 24px; margin-top: 14px; flex-wrap: wrap;">
                <div><span style="opacity:0.7;">Vehicles</span> <b style="font-size:20px;">{len(vehicles)}</b></div>
                <div><span style="opacity:0.7;">Pending Fines</span> <b style="font-size:20px; color:#ff6b6b;">{len(pending)}</b></div>
                <div><span style="opacity:0.7;">Documents</span> <b style="font-size:20px;">{len(docs)}</b></div>
                <div><span style="opacity:0.7;">Service Records</span> <b style="font-size:20px;">{len(service_records)}</b></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Actions Grid
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0 12px 0;">
        <h3 style="font-size: 16px; font-weight: 600; margin: 0;">🚀 Quick Actions & Services</h3>
    </div>
    <div class="quick-grid">
        <div class="quick-item qi-green" onclick="window.location.href='#vehicles'">
            <span class="qi-icon">🚗</span>
            My Vehicles
        </div>
        <div class="quick-item qi-blue" onclick="window.location.href='#violations'">
            <span class="qi-icon">⚠️</span>
            Violations
        </div>
        <div class="quick-item qi-orange" onclick="window.location.href='#payments'">
            <span class="qi-icon">💰</span>
            Bill & Payment
        </div>
        <div class="quick-item qi-purple" onclick="window.location.href='#documents'">
            <span class="qi-icon">📄</span>
            Documents
        </div>
        <div class="quick-item qi-teal" onclick="window.location.href='#service'">
            <span class="qi-icon">🔧</span>
            Service
        </div>
        <div class="quick-item qi-pink" onclick="window.location.href='#appeals'">
            <span class="qi-icon">📝</span>
            Appeals
        </div>
        <div class="quick-item qi-green" onclick="window.location.href='#brta'">
            <span class="qi-icon">🔎</span>
            BRTA Lookup
        </div>
        <div class="quick-item qi-blue" onclick="window.location.href='#notifications'">
            <span class="qi-icon">🔔</span>
            Notifications
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric Cards - Row 1 with proper spacing and darker shades
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-green-dark">
            <span class="metric-icon">🚗</span>
            <span class="metric-label">Total Vehicles</span>
            <span class="metric-value">{len(vehicles)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-orange-dark">
            <span class="metric-icon">⚠️</span>
            <span class="metric-label">Pending Fines</span>
            <span class="metric-value">{len(pending)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-blue-dark">
            <span class="metric-icon">✅</span>
            <span class="metric-label">Paid Fines</span>
            <span class="metric-value">{len(paid)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card metric-card-purple-dark">
            <span class="metric-icon">📄</span>
            <span class="metric-label">Documents</span>
            <span class="metric-value">{len(docs)}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Metric Cards - Row 2 with proper spacing and darker shades
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-teal-dark">
            <span class="metric-icon">🔔</span>
            <span class="metric-label">Notifications</span>
            <span class="metric-value">{len(notifs)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-pink-dark">
            <span class="metric-icon">⏰</span>
            <span class="metric-label">Expiring Soon</span>
            <span class="metric-value">{len(expiring_soon)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card metric-card-red-dark">
            <span class="metric-icon">🔧</span>
            <span class="metric-label">Service Records</span>
            <span class="metric-value">{len(service_records)}</span>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        total_value = total_paid_value + total_fine_value
        st.markdown(f"""
        <div class="metric-card metric-card-navy-dark">
            <span class="metric-icon">💰</span>
            <span class="metric-label">Total Fine Value</span>
            <span class="metric-value">৳{total_value:,}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Two Column Layout
    st.markdown('<div class="two-col">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown('<div class="panel"><div class="panel-head"><h3>📋 Recent Activity</h3></div>', unsafe_allow_html=True)
        for act in db.activity[:6]:
            st.markdown(f"""
            <div style="display:flex; gap:12px; padding:10px 0; border-bottom:1px solid #E2E6EA;">
                <span style="font-size:18px;">{act['icon']}</span>
                <div style="flex:1;">
                    <div style="font-size:13.5px;">{act['text']}</div>
                    <div style="font-size:11.5px; color:#5B6B82;">{act['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="panel"><div class="panel-head"><h3>⏰ Upcoming Expiries</h3></div>', unsafe_allow_html=True)
        if expiring_soon:
            for v in expiring_soon[:5]:
                expiring_items = []
                try:
                    if (datetime.strptime(v['taxExpiry'], "%Y-%m-%d") - datetime.now()).days < 30:
                        expiring_items.append("Tax")
                    if (datetime.strptime(v['fitnessExpiry'], "%Y-%m-%d") - datetime.now()).days < 30:
                        expiring_items.append("Fitness")
                    if (datetime.strptime(v['insuranceExpiry'], "%Y-%m-%d") - datetime.now()).days < 30:
                        expiring_items.append("Insurance")
                except:
                    pass
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #E2E6EA; font-size:13px;">
                    <span class="mono" style="font-weight:600;">{v['regNo']}</span>
                    <span class="badge badge-amber">{', '.join(expiring_items)}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty" style="padding:20px;">🎉 No upcoming expiries</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Violation Summary
    if violations:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-head"><h3>⚠️ Violation Summary</h3></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="text-align:center; padding:12px; background:#f8f9fa; border-radius:10px;">
                <div style="font-size:24px; font-weight:700; color:#B4740E;">{len(pending)}</div>
                <div style="font-size:12px; color:#5B6B82;">Pending</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align:center; padding:12px; background:#f8f9fa; border-radius:10px;">
                <div style="font-size:24px; font-weight:700; color:#046A38;">{len(paid)}</div>
                <div style="font-size:12px; color:#5B6B82;">Paid</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            appealed = [v for v in violations if v['status'] == 'appealed']
            st.markdown(f"""
            <div style="text-align:center; padding:12px; background:#f8f9fa; border-radius:10px;">
                <div style="font-size:24px; font-weight:700; color:#0B2545;">{len(appealed)}</div>
                <div style="font-size:12px; color:#5B6B82;">Appealed</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Keep all other render functions (render_vehicles, render_violations, render_payments, etc.)
# from the previous version - they remain unchanged

# ================= MAIN APP =================
def main():
    load_css()
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    if not is_logged_in():
        render_landing()
        
        st.divider()
        st.markdown('<p style="text-align:center; color: #5B6B82; font-size: 14px;">DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data</p>', unsafe_allow_html=True)

        st.markdown('<div id="get-started"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="page-head" style="display:block; margin-bottom: 6px;">
            <h2>Get started</h2>
            <p>Log in to an existing account, or create a free driver/owner account below. Registration takes less than a minute — no document upload is required to get started, and you can add vehicles once you're in.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔑 Need a quick demo login? Click here for test credentials"):
            st.markdown("""
            Use any of these to explore the portal without registering:

            | Role | Email | Password |
            |---|---|---|
            | Admin | `admin@drivebd.gov.bd` | `Admin@123` |
            | Driver | `driver@drivebd.gov.bd` | `Demo@123` |
            | Owner | `owner@drivebd.gov.bd` | `Demo@123` |

            Admin can manage users, review appeals, and adjust system settings. Driver and Owner accounts show the day-to-day citizen experience.
            """)

        tab1, tab2 = st.tabs(["Log In", "Create Account"])
        
        with tab1:
            st.markdown('<p style="color: var(--muted); font-size: 13.5px; margin-bottom: 10px;">Enter the email and password for your account. Use the demo credentials above if you just want to look around.</p>', unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Your password")
                if st.form_submit_button("Log In", use_container_width=True):
                    if not email.strip() or not password:
                        st.error("Please enter both your email and password.")
                    else:
                        ok, msg = login_user(email, password)
                        if ok:
                            st.session_state.page = 'dashboard'
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        
        with tab2:
            st.markdown('<p style="color: var(--muted); font-size: 13.5px; margin-bottom: 10px;">Create a free account as a <b>Driver</b> (you drive but may not own the vehicle) or an <b>Owner</b> (you own one or more vehicles). Admin accounts cannot be self-registered for security reasons.</p>', unsafe_allow_html=True)
            with st.form("register_form"):
                name = st.text_input("Full name", placeholder="e.g. Rafiq Ahmed")
                email = st.text_input("Email", placeholder="you@example.com")
                phone = st.text_input("Phone number", placeholder="e.g. 01712345678")
                nid = st.text_input("NID number", placeholder="10/13/17-digit National ID (optional)")
                role = st.selectbox("Account type", ["driver", "owner"], help="Driver: you operate a vehicle. Owner: you own one or more vehicles and manage their paperwork.")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    name = (name or "").strip()
                    email = (email or "").strip()
                    phone = (phone or "").strip()
                    nid = (nid or "").strip()
                    if not all([name, email, password]):
                        st.error("Name, email and password are required.")
                    elif "@" not in email or "." not in email.split("@")[-1]:
                        st.error("Please enter a valid email address.")
                    elif phone and not re.match(r'^01[3-9]\d{8}$', phone):
                        st.error("Please enter a valid Bangladeshi mobile number (e.g. 01712345678).")
                    elif nid and not re.match(r'^\d{10}$|^\d{13}$|^\d{17}$', nid):
                        st.error("NID should be 10, 13 or 17 digits, matching Bangladesh's NID formats.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif password != confirm_password:
                        st.error("Passwords do not match. Please re-type them.")
                    else:
                        ok, msg = register_user(name, email, password, role, phone, nid)
                        if ok:
                            st.session_state.page = 'dashboard'
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
    else:
        user = current_user()
        
        # Header
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.markdown(f'<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="sub-header">Smart Driver & Vehicle Owner Portal</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: right; padding-top: 8px;">
                <span style="font-weight: 600;">{user['name']}</span>
                <span style="color: #5B6B82; font-size: 12px; display: block;">{user['role'].title()}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Colorful Sidebar
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-profile">
                <div class="avatar">{user['avatar']}</div>
                <div class="name">{user['name']}</div>
                <div class="role">{user['role'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Overview")
            if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.page == 'dashboard' else "secondary"):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            st.markdown("### 🚗 Manage")
            if st.button("My Vehicles", use_container_width=True, type="primary" if st.session_state.page == 'vehicles' else "secondary"):
                st.session_state.page = 'vehicles'
                st.rerun()
            if st.button("⚠️ Violations", use_container_width=True, type="primary" if st.session_state.page == 'violations' else "secondary"):
                st.session_state.page = 'violations'
                st.rerun()
            if st.button("💰 Payments", use_container_width=True, type="primary" if st.session_state.page == 'payments' else "secondary"):
                st.session_state.page = 'payments'
                st.rerun()
            if st.button("📁 Documents", use_container_width=True, type="primary" if st.session_state.page == 'documents' else "secondary"):
                st.session_state.page = 'documents'
                st.rerun()
            if st.button("🔧 Service", use_container_width=True, type="primary" if st.session_state.page == 'service' else "secondary"):
                st.session_state.page = 'service'
                st.rerun()
            if st.button("📝 Appeals", use_container_width=True, type="primary" if st.session_state.page == 'appeals' else "secondary"):
                st.session_state.page = 'appeals'
                st.rerun()
            
            st.markdown("### 🛠️ Tools")
            if st.button("🔎 BRTA Lookup", use_container_width=True, type="primary" if st.session_state.page == 'brta' else "secondary"):
                st.session_state.page = 'brta'
                st.rerun()
            if st.button("✦ AI Demo", use_container_width=True, type="primary" if st.session_state.page == 'aidemo' else "secondary"):
                st.session_state.page = 'aidemo'
                st.rerun()
            if st.button("🔔 Notifications", use_container_width=True, type="primary" if st.session_state.page == 'notifications' else "secondary"):
                st.session_state.page = 'notifications'
                st.rerun()
            
            st.markdown("### 👤 Account")
            if st.button("⚙️ Profile", use_container_width=True, type="primary" if st.session_state.page == 'profile' else "secondary"):
                st.session_state.page = 'profile'
                st.rerun()
            
            if user['role'] == 'admin':
                st.markdown("### 🛡️ Administration")
                if st.button("Admin Panel", use_container_width=True, type="primary" if st.session_state.page == 'admin' else "secondary"):
                    st.session_state.page = 'admin'
                    st.rerun()
            
            st.divider()
            st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
            if st.button("🚪 Log out", use_container_width=True):
                logout_user()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Main content
        valid_pages = {'dashboard', 'vehicles', 'violations', 'payments', 'documents',
                       'service', 'appeals', 'brta', 'aidemo', 'notifications', 'profile', 'admin'}
        if st.session_state.page not in valid_pages or (
            st.session_state.page == 'admin' and user['role'] != 'admin'
        ):
            st.session_state.page = 'dashboard'

        if st.session_state.page == 'dashboard':
            render_dashboard()
        elif st.session_state.page == 'vehicles':
            render_vehicles()
        elif st.session_state.page == 'violations':
            render_violations()
        elif st.session_state.page == 'payments':
            render_payments()
        elif st.session_state.page == 'documents':
            render_documents()
        elif st.session_state.page == 'service':
            render_service()
        elif st.session_state.page == 'appeals':
            render_appeals()
        elif st.session_state.page == 'brta':
            render_brta()
        elif st.session_state.page == 'aidemo':
            render_aidemo()
        elif st.session_state.page == 'notifications':
            render_notifications()
        elif st.session_state.page == 'profile':
            render_profile()
        elif st.session_state.page == 'admin':
            render_admin()

if __name__ == "__main__":
    main()
