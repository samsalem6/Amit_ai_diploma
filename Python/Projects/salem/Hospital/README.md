# Hospital Management System

A command-line based Hospital Management System for managing patients, staff, departments, rooms, billing, and procedures.

## Features
- **User Authentication:** Login required to access the system.
- **Patient Management:**
  - Add, edit, remove patients (by name or patient number)
  - Assign unique, sequential patient numbers automatically
  - Track patient status (normal, surgery, emergency)
  - Assign rooms to patients
- **Staff & Department Management:**
  - Add departments
  - Add, edit, remove staff in departments
  - View staff by department
- **Procedures:**
  - Add and view medical procedures for each patient
  - Mark procedures as billed
- **Billing:**
  - Generate bills for patients manually or from procedures
  - Mark bills as paid
  - View all bills for a patient in a table
- **Data Persistence:**
  - All data is saved automatically to `hospital_database.json`
- **Pretty CLI Tables:**
  - Uses PrettyTable for clear, tabular display of bills and procedures

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
- **Login:** Use the default credentials (`admin` / `password`) or update the login logic in `auth/login.py`.
- **Menu Navigation:** Follow the on-screen menu to manage patients, staff, departments, procedures, and billing.
- **Patient Operations:** Use either the patient name or patient number for all operations.
- **Procedures & Billing:**
  - Add procedures to a patient.
  - Use "Generate Bills from Procedures" to create bills for all unbilled procedures, entering the cost for each.
  - Mark bills as paid when payment is received.

## File Structure
- `main.py` — Entry point for the application
- `core/hospital_system.py` — Main system logic
- `model/` — Data models (Patient, Staff, Department, Billing, etc.)
- `auth/login.py` — Simple authentication logic
- `hospital_database.json` — Data storage (auto-generated)

## Credits
- Developed by Salem Sameer and Mohamed Gamal (and contributors)
- Powered by Python 3 and PrettyTable

---
Feel free to extend this system with more features such as reporting, advanced search, or a graphical interface!
