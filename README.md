# Premium Hotel Management System 🏨✨

A comprehensive, desktop-based **Hotel Management System** built using **Python**, **Tkinter** for a rich graphical user interface, and **MySQL** for robust, real-time data persistence. The system features a dark, premium aesthetic with dynamic visual counters, advanced analytics, user authentication, and fully featured modules for customer profiles and room bookings.

---

## 🚀 Key Features

* **Advanced Authentication (`login.py`)**: 
    * Secure registration and login system with password hashing (`hashlib`).
    * Input validation and duplicate credential checking.
* **Main Dashboard (`main.py`)**:
    * A high-end, centralized control panel to navigate seamlessly between different services.
    * Dynamic profile updates and account deletion management.
* **Customer Management (`customer.py`)**:
    * Auto-generation of unique Customer Reference IDs.
    * Full CRUD operations (Create, Read, Update, Delete) for guest details.
    * Multi-criteria search engine (Search by Mobile, Ref, Name, or ID Number).
* **Room Booking Module (`room.py`)**:
    * Real-time check-in and check-out tracking using `tkcalendar`.
    * Automated price, number of days, and meal cost configurations.
* **Analytics & Statistics (`details.py`)**:
    * A premium Dark & Gold themed interface.
    * Dynamic, animated stat counters showing revenue and total records with smooth numerical transitions.

---

## 📂 Project Structure

```text
Hotel-Management-System/
│
├── assets/                  # Media, images, and system icons
│   └── imgs/
│       └── my_icon.png
│
├── src/                    # Core Python source code
│   ├── main.py             # Main application dashboard
│   ├── login.py            # Login & user registration interface
│   ├── customer.py         # Customer management window
│   ├── room.py             # Room booking and calculation window
│   └── details.py          # Dashboard analytics & reporting
│
├── database/               # SQL database backup and schema
│   └── database_setup.sql
│
├── .gitignore              # Specifies intentionally untracked files to ignore
├── requirements.txt        # Python external dependencies
└── README.md               # Project documentation