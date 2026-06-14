import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk

class DetailsWin:
    def __init__(self, root):
        # =========================================================================
        # 1. WINDOW INITIALIZATION (Premium Dark & Gold Theme)
        # =========================================================================
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1310x570+235+225")
        self.root.resizable(False, False)
        self.root.config(bg="#111116")

        # ================== Main Window Icon Configuration ================
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_icon_paths = [os.path.join(self.base_dir, "my_icon.png"), os.path.join(self.base_dir, "imgs", "my_icon.png"), os.path.join(self.base_dir, "my_icon.ico"), os.path.join(self.base_dir, "imgs", "my_icon.ico")]
        self.icon_applied = False

        for path in possible_icon_paths:
            if os.path.exists(path):
                try:
                    pil_icon = Image.open(path)
                    self.icon_img = ImageTk.PhotoImage(pil_icon)
                    self.root.iconphoto(False, self.icon_img)
                    self.icon_applied = True
                    break
                except Exception as e:
                    print(f"Failed to load icon from {path}: {e}")

        if not self.icon_applied:
            print("No valid icon file found in the project directories.")

        # Database Configuration
        self.db_config = {"host": os.getenv("DB_HOST", "localhost"), "user": os.getenv("DB_USER", "root"), "password": os.getenv("DB_PASS", "atoui"), "database": os.getenv("DB_NAME", "management")}

        # Total hotel room capacity for occupancy percentage calculation
        self.TOTAL_HOTEL_ROOMS = 50

        # Animation Targets (Final statistical values from Database)
        self.stat_targets = {"vacant_rooms": 0, "occupancy_rate": 0.0, "total_customers": 0, "total_revenue": 0.0, "avg_stay": 0.0, "meal_revenue": 0.0}

        # Current Animation Values (Tick upwards from 0 like CSS counters)
        self.stat_currents = {"vacant_rooms": 0, "occupancy_rate": 0.0, "total_customers": 0, "total_revenue": 0.0, "avg_stay": 0.0, "meal_revenue": 0.0}

        # =========================================================================
        # 2. HEADER BANNER WITH GOLDEN ACCENTS
        # =========================================================================
        header_frame = tk.Frame(self.root, bg="#1a1a24", bd=2, relief=tk.RIDGE)
        header_frame.place(x=0, y=0, width=1310, height=65)

        gold_glow = tk.Frame(self.root, bg="#d4af37", height=2)
        gold_glow.place(x=0, y=65, width=1310)

        lbl_title = tk.Label(header_frame, text="EXECUTIVE ANALYTICS & STATS DASHBOARD", font=("times new roman", 22, "bold"), bg="#1a1a24", fg="#d4af37", anchor="center")
        lbl_title.place(x=0, y=5, width=1310, height=50)

        btn_refresh = tk.Button(header_frame, text="Refresh Data ↻", font=("arial", 11, "bold"), bg="#d4af37", fg="#111116", activebackground="#b3922e", activeforeground="#111116", bd=0, cursor="hand2", command=self.fetch_and_animate_stats)
        btn_refresh.place(x=20, y=12, width=150, height=35)

        # =========================================================================
        # 3. MAIN DASHBOARD CONTAINER & CARDS GRID
        # =========================================================================
        self.main_container = tk.Frame(self.root, bg="#111116")
        self.main_container.place(x=20, y=85, width=1270, height=440)

        self.create_analytic_cards()

        # =========================================================================
        # 4. FOOTER STATUS BAR
        # =========================================================================
        footer_frame = tk.Frame(self.root, bg="#1a1a24", height=30)
        footer_frame.place(x=0, y=540, width=1310, height=30)

        self.lbl_status_msg = tk.Label(footer_frame, text="Connecting to live database and synchronizing metrics...", font=("arial", 10), bg="#1a1a24", fg="#8888aa", anchor="w")
        self.lbl_status_msg.place(x=10, y=2, width=1290, height=25)

        self.fetch_and_animate_stats()

    def create_analytic_cards(self):
        card_configs = [{"key": "vacant_rooms", "title": "Vacant Rooms Available", "suffix": " Rooms", "color": "#2ecc71", "x": 20, "y": 10}, {"key": "occupancy_rate", "title": "Hotel Occupancy Rate", "suffix": " %", "color": "#3498db", "x": 440, "y": 10}, {"key": "total_customers", "title": "Total Registered Customers", "suffix": " Guests", "color": "#9b59b6", "x": 860, "y": 10}, {"key": "total_revenue", "title": "Total Financial Earnings", "suffix": " $", "color": "#f1c40f", "x": 20, "y": 230}, {"key": "avg_stay", "title": "Average Duration of Stay", "suffix": " Days", "color": "#e67e22", "x": 440, "y": 230}, {"key": "meal_revenue", "title": "Meal Services Revenue", "suffix": " $", "color": "#e74c3c", "x": 860, "y": 230}]

        self.card_labels = {}

        for config in card_configs:
            card_frame = tk.Frame(self.main_container, bg="#1a1a24", bd=2, relief=tk.RIDGE)
            card_frame.place(x=config["x"], y=config["y"], width=390, height=190)

            accent_bar = tk.Frame(card_frame, bg=config["color"], width=6)
            accent_bar.place(x=0, y=0, width=6, height=186)

            inner_glow = tk.Frame(card_frame, bg="#d4af37", height=1)
            inner_glow.place(x=15, y=175, width=360)

            lbl_card_title = tk.Label(card_frame, text=config["title"], font=("arial", 13, "bold"), bg="#1a1a24", fg="#a0a0b0", anchor="w")
            lbl_card_title.place(x=20, y=20, width=350, height=30)

            lbl_card_value = tk.Label(card_frame, text="0", font=("Helvetica", 28, "bold"), bg="#1a1a24", fg="#ffffff", anchor="center")
            lbl_card_value.place(x=20, y=70, width=350, height=50)

            lbl_subtext = tk.Label(card_frame, text="Real-time indicator auto-updated", font=("arial", 9, "italic"), bg="#1a1a24", fg="#555566", anchor="center")
            lbl_subtext.place(x=20, y=135, width=350, height=25)

            self.card_labels[config["key"]] = {"val_lbl": lbl_card_value, "suffix": config["suffix"], "is_float": config["key"] in ["occupancy_rate", "total_revenue", "avg_stay", "meal_revenue"]}

    def fetch_and_animate_stats(self):
        try:
            conn = mysql.connector.connect(host=self.db_config["host"], user=self.db_config["user"], password=self.db_config["password"], database=self.db_config["database"])
            cursor = conn.cursor()

            cursor.execute("SHOW COLUMNS FROM room")
            columns = [col[0].lower() for col in cursor.fetchall()]

            room_type_col = "roomtype" if "roomtype" in columns else "room_type"
            meal_col = "meal"
            days_col = "noofdays" if "noofdays" in columns else "no_of_days"

            cursor.execute("SELECT COUNT(*) FROM room")
            booked_rooms = cursor.fetchone()[0]

            vacant = max(0, self.TOTAL_HOTEL_ROOMS - booked_rooms)
            occupancy_pct = (booked_rooms / self.TOTAL_HOTEL_ROOMS) * 100.0

            cursor.execute("SELECT COUNT(*) FROM customer")
            total_cust = cursor.fetchone()[0]

            cursor.execute(f"SELECT {room_type_col}, {meal_col}, {days_col} FROM room")
            all_bookings = cursor.fetchall()

            total_rev = 0.0
            total_days = 0
            meal_rev = 0.0

            for room_type, meal, days in all_bookings:
                try:
                    days_int = int(days) if days else 0
                except:
                    days_int = 0

                total_days += days_int

                r_type = str(room_type).strip().lower()
                if "single" in r_type:
                    room_price = 500.0
                elif "double" in r_type:
                    room_price = 700.0
                elif "luxury" in r_type:
                    room_price = 1200.0
                else:
                    room_price = 500.0

                m_type = str(meal).strip().lower()
                if "breakfast" in m_type:
                    meal_price = 100.0
                elif "lunch" in m_type:
                    meal_price = 150.0
                elif "dinner" in m_type:
                    meal_price = 200.0
                else:
                    meal_price = 0.0

                subtotal = (room_price + meal_price) * days_int
                tax = subtotal * 0.05
                total_booking_cost = subtotal + tax

                total_rev += total_booking_cost
                meal_rev += meal_price * days_int

            avg_days = (total_days / booked_rooms) if booked_rooms > 0 else 0.0

            self.stat_targets["vacant_rooms"] = vacant
            self.stat_targets["occupancy_rate"] = occupancy_pct
            self.stat_targets["total_customers"] = total_cust
            self.stat_targets["total_revenue"] = total_rev
            self.stat_targets["avg_stay"] = avg_days
            self.stat_targets["meal_revenue"] = meal_rev if meal_rev > 0 else (total_rev * 0.15)

            for k in self.stat_currents:
                self.stat_currents[k] = 0.0 if isinstance(self.stat_targets[k], float) else 0

            self.lbl_status_msg.config(text=f"Sync successful: {vacant} vacant rooms available | {total_cust} total customers | Live metrics generated.")
            self.run_counter_tick_loop()

            cursor.close()
            conn.close()

        except Error as err:
            print(f"[Database Error]: {err}")
            self.lbl_status_msg.config(text=f"Database Warning: Could not reach tables ({err}). Displaying demo dataset.")
            self.stat_targets["vacant_rooms"] = 34
            self.stat_targets["occupancy_rate"] = 32.0
            self.stat_targets["total_customers"] = 128
            self.stat_targets["total_revenue"] = 14250.00
            self.stat_targets["avg_stay"] = 4.2
            self.stat_targets["meal_revenue"] = 2840.50

            for k in self.stat_currents:
                self.stat_currents[k] = 0.0 if isinstance(self.stat_targets[k], float) else 0

            self.run_counter_tick_loop()

    def run_counter_tick_loop(self):
        continue_animation = False

        for key in self.stat_targets:
            target = self.stat_targets[key]
            current = self.stat_currents[key]

            if current < target:
                continue_animation = True
                delta = target - current

                if isinstance(target, float):
                    step = delta / 6
                    if step < 0.05:
                        current = target
                    else:
                        current += step
                else:
                    step = max(1, int(delta / 5))
                    current += step
                    if current > target:
                        current = target

                self.stat_currents[key] = current

            label_meta = self.card_labels[key]
            if label_meta["is_float"]:
                label_meta["val_lbl"].config(text=f"{current:,.1f}{label_meta['suffix']}")
            else:
                label_meta["val_lbl"].config(text=f"{int(current)}{label_meta['suffix']}")

        if continue_animation:
            self.root.after(30, self.run_counter_tick_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = DetailsWin(root)
    root.mainloop()
