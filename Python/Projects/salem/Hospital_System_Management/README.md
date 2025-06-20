# Hospital Management System

A command-line based Hospital Management System for managing patients, staff, departments, rooms, billing, and procedures, with persistent data storage and user authentication.

## Features
- **User Authentication:**
  - Login required to access the system (default: `admin` / `admin`).
  - Credentials and logic can be updated in `auth/login.py`.
- **Patient Management:**
  - Add, edit, and remove patients (by name or unique patient number).
  - Assign unique, sequential patient numbers automatically.
  - Track patient status (normal, surgery, emergency, etc.).
  - Assign rooms to patients and manage room assignments.
  - Store and update next of kin and insurance information for each patient.
  - Register, discharge, and record date of death for patients.
- **Staff & Department Management:**
  - Add, edit, and remove departments.
  - Add, edit, and remove staff (doctors, nurses, other staff) in departments.
  - Assign patients to doctors within departments.
  - View staff by department, including doctors and nurses.
- **Procedures:**
  - Add and view medical procedures for each patient.
  - Mark procedures as billed.
  - Generate bills from unbilled procedures.
- **Billing:**
  - Generate bills for patients manually or from procedures.
  - Apply insurance discounts automatically if insurance info is present.
  - Mark bills as paid and view payment status.
  - View all bills for a patient in a clear, tabular format.
- **Data Persistence:**
  - All data is saved automatically to `hospital_database.json` (JSON format).
- **Pretty CLI Tables:**
  - Uses PrettyTable for clear, tabular display of bills, procedures, and staff.
- **Extensible Design:**
  - Easily extendable for new features such as advanced reporting, search, or a graphical interface.

## Data Models
- **Patient:**
  - Inherits from Person. Stores medical, contact, next of kin, insurance, procedures, billing, and status info.
- **Staff:**
  - Inherits from Person. Includes Doctor and Nurse subclasses, with department and specialty fields.
- **Department:**
  - Holds lists of doctors, nurses, staff, and patients. Supports patient assignment to doctors.
- **Billing:**
  - Represents bills, supports insurance discounts, and tracks payment status.

## Setup
1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies:**
   ```bash
   pip install prettytable
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage
- **Login:** Use the default credentials (`admin` / `admin`).
- **Menu Navigation:** Follow the on-screen menu to manage patients, staff, departments, procedures, and billing.
- **Patient Operations:** Use either the patient name or patient number for all operations. Add next of kin and insurance info as needed.
- **Procedures & Billing:**
  - Add procedures to a patient.
  - Use "Generate Bills from Procedures" to create bills for all unbilled procedures, entering the cost for each.
  - Insurance discounts are applied automatically if present.
  - Mark bills as paid when payment is received.

## File Structure
- `main.py` — Entry point for the application
- `core/hospital_system.py` — Main system logic and menu
- `model/` — Data models:
  - `patient.py`, `staff.py`, `department.py`, `billing.py`, `person.py`
- `auth/login.py` — Authentication logic
- `hospital_database.json` — Data storage (auto-generated)

## Credits
- Developed by Salem Sameer and Mohamed Gamal (and contributors)
- Powered by Python 3 and PrettyTable

---
Feel free to extend this system with more features such as reporting, advanced search, or a graphical interface!
