import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from tkcalendar import DateEntry


class RoomBooking:
    def __init__(self, root):
        # =========================================================================
        # 1. WINDOW INITIALIZATION & CONFIGURATION
        # =========================================================================
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1310x570+235+225")
        self.root.resizable(False, False)

        # Database Configuration
        self.db_config = {"host": os.getenv("DB_HOST", "localhost"), "username": os.getenv("DB_USER", "root"), "password": os.getenv("DB_PASS", "atoui"), "database": os.getenv("DB_NAME", "management")}

        self.selected_booking_old = None

        # =========================================================================
        # 2. STYLES & THEMING (UI CUSTOMIZATION)
        # =========================================================================
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Thin.Horizontal.TScrollbar", arrowsize=9, thickness=8, background="#333333", troughcolor="black", bordercolor="black", gripcount=0)
        self.style.configure("Custom.TCombobox", selectbackground="white", selectforeground="black", fieldbackground="white", background="white")
        self.style.map("Custom.TCombobox", selectbackground=[("readonly", "white"), ("focus", "white")], selectforeground=[("readonly", "black"), ("focus", "black")], fieldbackground=[("readonly", "white")])
        self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=25, font=("arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#4E4E4E")], foreground=[("selected", "gold")])
        self.style.configure("Treeview.Heading", background="#313131", foreground="gold", font=("arial", 11, "bold"))
        self.style.map("Treeview.Heading", background=[("active", "#636363")])
        self.style.map("CustomDate.TEntry", selectbackground=[("focus", "#4E4E4E"), ("!focus", "#333333")], selectforeground=[("focus", "gold"), ("!focus", "#b5b5b5")])

        # =========================================================================
        # 3. CONTROL VARIABLES (TKINTER VARIABLES)
        # =========================================================================
        self.var_contact = tk.StringVar()
        self.var_check_in = tk.StringVar()
        self.var_check_out = tk.StringVar()
        self.var_room_type = tk.StringVar()
        self.var_room_vailable = tk.StringVar()
        self.var_meal = tk.StringVar()
        self.var_no_of_days = tk.StringVar()
        self.var_room_price = tk.StringVar()
        self.var_actual_total = tk.StringVar()
        self.var_paid_tax = tk.StringVar()
        self.var_total = tk.StringVar()

        self.var_search_by = tk.StringVar()
        self.var_search_txt = tk.StringVar()

        # Matrix Pool for 50 Rooms total
        self.rooms_pool = {"Single": list(range(1, 21)), "Double": list(range(21, 41)), "Luxury": list(range(41, 51))}  # 20 Rooms  # 20 Rooms  # 10 Rooms
        self.available_rooms_list = []

        # =========================================================================
        # 4. HEADER & LOGO
        # =========================================================================
        lbl_title = tk.Label(self.root, text="Roombooking Details".upper(), font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=tk.RIDGE)
        lbl_title.place(x=0, y=0, width=1310, height=50)

        try:
            logo = Image.open(r"imgs\img5.png")
            logo = logo.resize((90, 50), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo)
            lbl_logo = tk.Label(self.root, image=self.logo, bd=0, relief=tk.RIDGE)
            lbl_logo.place(x=3, y=3, width=90, height=40)
        except FileNotFoundError:
            messagebox.showwarning("Image Warning", "Logo image not found. Proceeding without logo.", parent=self.root)

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

        # =========================================================================
        # 5. LEFT FRAME - INPUT FORM
        # =========================================================================
        labelframeleft = tk.LabelFrame(self.root, bd=2, relief=tk.RIDGE, text="Roombooking Details", font=("times new roman", 12, "bold"), pady=2)
        labelframeleft.place(x=5, y=50, width=425, height=510)

        validate_cmd = self.root.register(lambda action: action != "1")

        # Customer Contact
        lbl_cust_contact = tk.Label(labelframeleft, text="Customer Contact", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_cust_contact.grid(row=0, column=0, sticky=tk.W)
        self.entry_cust_contact = ttk.Entry(labelframeleft, textvariable=self.var_contact, width=20, font=("arial", 13, "bold"))
        self.entry_cust_contact.grid(row=0, column=1, sticky=tk.W)

        # Check-in Date
        lbl_check_in = tk.Label(labelframeleft, text="Check-in Date", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_check_in.grid(row=1, column=0, sticky=tk.W)
        self.entry_check_in = DateEntry(labelframeleft, textvariable=self.var_check_in, width=27, font=("arial", 13, "bold"), background="black", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", validate="key", validatecommand=(validate_cmd, "%d"), state="readonly", style="CustomDate.TEntry")
        self.entry_check_in.grid(row=1, column=1)

        # Check-out Date
        lbl_check_out = tk.Label(labelframeleft, text="Check-out Date", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_check_out.grid(row=2, column=0, sticky=tk.W)
        self.entry_check_out = DateEntry(labelframeleft, textvariable=self.var_check_out, width=27, font=("arial", 13, "bold"), background="black", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", validate="key", validatecommand=(validate_cmd, "%d"), state="readonly", style="CustomDate.TEntry")
        self.entry_check_out.grid(row=2, column=1)

        # Date Events Binding
        self.entry_check_in.bind("<<DateEntrySelected>>", self.update_date_limits)
        self.entry_check_out.bind("<<DateEntrySelected>>", self.update_date_limits)

        # Room Type
        lbl_room_type = tk.Label(labelframeleft, text="Room Type", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_room_type.grid(row=3, column=0, sticky=tk.W)
        combo_room_type = ttk.Combobox(labelframeleft, textvariable=self.var_room_type, font=("arial", 13, "bold"), width=27, state="readonly", style="Custom.TCombobox")
        combo_room_type["value"] = ("Single", "Double", "Luxury")
        combo_room_type.current(0)
        combo_room_type.grid(row=3, column=1)
        combo_room_type.bind("<<ComboboxSelected>>", self.update_room_price)

        # Room Available (Dropdown Replacement with Popup Matrix Window Layout)
        lbl_room_available = tk.Label(labelframeleft, text="Room Available", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_room_available.grid(row=4, column=0, sticky=tk.W)

        room_select_frame = tk.Frame(labelframeleft)
        room_select_frame.grid(row=4, column=1, sticky=tk.W)

        self.entry_room_available = ttk.Entry(room_select_frame, textvariable=self.var_room_vailable, font=("arial", 13, "bold"), width=21, state="readonly")
        self.entry_room_available.pack(side=tk.LEFT)

        btn_choose_room = tk.Button(room_select_frame, text="⋮", font=("arial", 11, "bold"), bg="black", fg="gold", width=3, cursor="hand2", command=self.popup_room_matrix)
        btn_choose_room.pack(side=tk.LEFT, padx=2)

        # Meal Options
        lbl_meal = tk.Label(labelframeleft, text="Meal", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_meal.grid(row=5, column=0, sticky=tk.W)
        combo_meal = ttk.Combobox(labelframeleft, textvariable=self.var_meal, font=("arial", 13, "bold"), width=27, state="readonly", style="Custom.TCombobox")
        combo_meal["value"] = ("Breakfast Only", "Half Board", "Full Board")
        combo_meal.current(0)
        combo_meal.grid(row=5, column=1)
        combo_meal.bind("<<ComboboxSelected>>", lambda e: self.calculate_bill())

        # Calculations Fields
        lbl_no_of_days = tk.Label(labelframeleft, text="No Of Days", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_no_of_days.grid(row=6, column=0, sticky=tk.W)
        entry_no_of_days = ttk.Entry(labelframeleft, textvariable=self.var_no_of_days, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_no_of_days.grid(row=6, column=1)

        lbl_room_price = tk.Label(labelframeleft, text="Room Price", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_room_price.grid(row=7, column=0, sticky=tk.W)
        entry_room_price = ttk.Entry(labelframeleft, textvariable=self.var_room_price, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_room_price.grid(row=7, column=1)

        lbl_sub_total = tk.Label(labelframeleft, text="Sub Total", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_sub_total.grid(row=8, column=0, sticky=tk.W)
        entry_sub_total = ttk.Entry(labelframeleft, textvariable=self.var_actual_total, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_sub_total.grid(row=8, column=1)

        lbl_paid_tax = tk.Label(labelframeleft, text="Paid Tax", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_paid_tax.grid(row=9, column=0, sticky=tk.W)
        entry_paid_tax = ttk.Entry(labelframeleft, textvariable=self.var_paid_tax, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_paid_tax.grid(row=9, column=1)

        lbl_total_cost = tk.Label(labelframeleft, text="Total Cost", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_total_cost.grid(row=10, column=0, sticky=tk.W)
        entry_total_cost = ttk.Entry(labelframeleft, textvariable=self.var_total, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_total_cost.grid(row=10, column=1)

        self.update_room_price()
        self.root.after(100, self.update_date_limits)

        # Button Hover Effects
        def on_enter(event):
            event.widget.config(bg="#3b3a3a", fg="gold")

        def on_leave(event):
            event.widget.config(bg="black", fg="gold")

        btn_featch_data = tk.Button(labelframeleft, text="Fetch Data", font=("arial", 9, "bold"), bg="black", fg="gold", width=10, command=self.fetch_contact, cursor="hand2")
        btn_featch_data.place(x=335, y=5)
        btn_featch_data.bind("<Enter>", on_enter)
        btn_featch_data.bind("<Leave>", on_leave)

        # =========================================================================
        # 6. ACTION BUTTONS FRAME
        # =========================================================================
        btn_frame = tk.Frame(labelframeleft, bd=2, relief=tk.RIDGE)
        btn_frame.place(x=3, y=442, width=412, height=40)

        btn_add = tk.Button(btn_frame, text="Add", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.add_data)
        btn_add.grid(row=0, column=0, padx=1, pady=1.5)

        btn_update = tk.Button(btn_frame, text="Update", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.update_data)
        btn_update.grid(row=0, column=1, padx=1, pady=1.5)

        btn_remove = tk.Button(btn_frame, text="Remove", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.remove_data)
        btn_remove.grid(row=0, column=2, padx=1, pady=1.5)

        btn_reset = tk.Button(btn_frame, text="Reset", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.reset_data)
        btn_reset.grid(row=0, column=3, padx=1, pady=1.5)

        for btn in (btn_add, btn_remove, btn_update, btn_reset):
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # =========================================================================
        # 7. RIGHT FRAME - SEARCH & VIEW DATA SYSTEM
        # =========================================================================
        table_frame = tk.LabelFrame(self.root, bd=2, relief=tk.RIDGE, text="View Details and Search System", font=("times new roman", 12, "bold"), pady=2)
        table_frame.place(x=440, y=280, width=860, height=280)

        lbl_search = tk.Label(table_frame, text="Search By:", font=("arial", 12, "bold"), fg="gold", bg="black", padx=6, pady=2)
        lbl_search.grid(row=0, column=0, padx=2)

        self.combo_search = ttk.Combobox(table_frame, textvariable=self.var_search_by, font=("arial", 13, "bold"), width=18, state="readonly", style="Custom.TCombobox")
        self.combo_search["values"] = ("Contact", "Room_available")
        self.combo_search.current(0)
        self.combo_search.grid(row=0, column=1, padx=2)

        self.entry_search_address = ttk.Entry(table_frame, textvariable=self.var_search_txt, width=22, font=("arial", 13, "bold"))
        self.entry_search_address.grid(row=0, column=2, padx=2)

        btn_search = tk.Button(table_frame, text="Search", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.search_data)
        btn_search.grid(row=0, column=3, padx=2)
        btn_search.bind("<Enter>", on_enter)
        btn_search.bind("<Leave>", on_leave)

        btn_show_all = tk.Button(table_frame, text="Show All", font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2", command=self.fetch_data)
        btn_show_all.grid(row=0, column=4, padx=2)
        btn_show_all.bind("<Enter>", on_enter)
        btn_show_all.bind("<Leave>", on_leave)

        try:
            img = Image.open(r"imgs\logo1.png")
            img = img.resize((540, 225), Image.LANCZOS)
            self.img = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(self.root, image=self.img, bd=0, relief=tk.RIDGE)
            lbl_img.place(x=760, y=55, width=540, height=225)
        except FileNotFoundError:
            pass

        # =========================================================================
        # 8. TREEVIEW DATA TABLE WITH SCROLLBARS
        # =========================================================================
        details_table = tk.Frame(table_frame, bd=2, relief=tk.RIDGE)
        details_table.place(x=13, y=70, width=830, height=180)

        scroll_x = ttk.Scrollbar(details_table, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=tk.VERTICAL)

        self.cust_details_table = ttk.Treeview(details_table, columns=("contact", "check_in", "check_out", "room_type", "room_available", "meal", "days"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.cust_details_table.xview)
        scroll_y.config(command=self.cust_details_table.yview)

        self.cust_details_table.heading("contact", text="Contact No")
        self.cust_details_table.heading("check_in", text="Check-in")
        self.cust_details_table.heading("check_out", text="Check-out")
        self.cust_details_table.heading("room_type", text="Room Type")
        self.cust_details_table.heading("room_available", text="Room No")
        self.cust_details_table.heading("meal", text="Meal")
        self.cust_details_table.heading("days", text="No of Days")

        self.cust_details_table["show"] = "headings"

        self.cust_details_table.column("contact", width=110)
        self.cust_details_table.column("check_in", width=100)
        self.cust_details_table.column("check_out", width=100)
        self.cust_details_table.column("room_type", width=100)
        self.cust_details_table.column("room_available", width=100)
        self.cust_details_table.column("meal", width=90)
        self.cust_details_table.column("days", width=90)

        self.cust_details_table.pack(fill=tk.BOTH, expand=1)
        self.cust_details_table.bind("<ButtonRelease-1>", self.get_cursor)

        # =========================================================================
        # 9. SCROLLABLE CUSTOMER DETAILS SIDE PANEL
        # =========================================================================
        self.show_dataframe = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="black")
        self.show_dataframe.place(x=450, y=55, width=300, height=225)

        self.inner_scrollbar_x = ttk.Scrollbar(self.show_dataframe, orient=tk.HORIZONTAL, style="Thin.Horizontal.TScrollbar")
        self.inner_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.show_dataframe, bg="black", highlightthickness=0, xscrollcommand=self.inner_scrollbar_x.set)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.inner_scrollbar_x.config(command=self.canvas.xview)

        self.inner_frame = tk.Frame(self.canvas, bg="black", padx=10, pady=10)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        labels_text = ["Name:", "Gender:", "Email:", "Nationality:", "Address:"]
        for i, text in enumerate(labels_text):
            lbl = tk.Label(self.inner_frame, text=text, font=("arial", 13, "bold"), bg="black", fg="gold")
            lbl.grid(row=i, column=0, sticky="w", pady=6, padx=2)

        self.fetch_data()

    # =========================================================================
    # 10. BACKEND LOGIC & DYNAMIC FILTERING FUNCTIONS
    # =========================================================================
    def get_db_connection(self):
        return mysql.connector.connect(host=self.db_config["host"], username=self.db_config["username"], password=self.db_config["password"], database=self.db_config["database"])

    def is_contact_registered(self, contact_number):
        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()
            query = "SELECT Mobile FROM customer WHERE Mobile=%s"
            my_cursor.execute(query, (contact_number.strip(),))
            row = my_cursor.fetchone()
            return row is not None
        except Error as es:
            print(f"Error checking contact: {str(es)}")
            return False
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def update_date_limits(self, event=None):
        try:
            today = datetime.now().date()
            self.entry_check_in.config(mindate=today)

            # Fixed calculation by using direct .get_date() object objects instead of unsafe strptime strings
            in_date = self.entry_check_in.get_date()
            out_date = self.entry_check_out.get_date()

            if in_date:
                self.entry_check_out.config(mindate=in_date)

            if out_date:
                self.entry_check_in.config(maxdate=out_date)

            if in_date and out_date:
                days = (out_date - in_date).days
                if days <= 0:
                    days = 1

                self.var_no_of_days.set(str(days))
                self.calculate_bill()

            self.refresh_available_rooms()
        except Exception as e:
            print(f"Error updating date limits: {e}")

    def update_room_price(self, event=None):
        room_type = self.var_room_type.get().strip()
        if room_type == "Single":
            price = 75.00
        elif room_type == "Double":
            price = 120.00
        elif room_type == "Luxury":
            price = 350.00
        else:
            price = 0.00

        self.var_room_price.set(f"${price:.2f}")
        if self.var_no_of_days.get().strip() != "":
            self.calculate_bill()

        self.refresh_available_rooms()

    def refresh_available_rooms(self):
        room_type = self.var_room_type.get().strip()
        all_rooms = self.rooms_pool.get(room_type, [])

        try:
            new_in = self.entry_check_in.get_date()
            new_out = self.entry_check_out.get_date()
        except Exception:
            self.available_rooms_list = all_rooms
            return

        conn, my_cursor = None, None
        booked_rooms = set()
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()
            query = "SELECT Room_available, Check_in, Check_out FROM room WHERE Room_type=%s"
            my_cursor.execute(query, (room_type,))
            rows = my_cursor.fetchall()

            for row in rows:
                r_no, db_in_val, db_out_val = row

                db_in = datetime.strptime(db_in_val, "%Y-%m-%d").date() if isinstance(db_in_val, str) else db_in_val
                db_out = datetime.strptime(db_out_val, "%Y-%m-%d").date() if isinstance(db_out_val, str) else db_out_val

                if self.selected_booking_old and str(r_no) == str(self.selected_booking_old[1]) and str(db_in_val) == str(self.selected_booking_old[2]):
                    continue

                if not (new_out < db_in or new_in > db_out):
                    booked_rooms.add(int(r_no))

        except Exception as e:
            print(f"Error checking dynamic room slots: {e}")
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

        self.available_rooms_list = [r for r in all_rooms if r not in booked_rooms]

        curr_val = self.var_room_vailable.get()
        if curr_val and (int(curr_val) not in self.available_rooms_list):
            if not (self.selected_booking_old and curr_val == str(self.selected_booking_old[1])):
                self.var_room_vailable.set("")

    # =========================================================================
    # Popup Grid Room Selection Matrix Logic
    # =========================================================================
    def popup_room_matrix(self):
        self.refresh_available_rooms()

        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)

        x = self.entry_room_available.winfo_rootx()
        y = self.entry_room_available.winfo_rooty() + self.entry_room_available.winfo_height()
        popup.geometry(f"230x180+{x}+{y}")
        popup.config(bg="#1a1a1a", bd=2, relief=tk.RIDGE)

        popup.bind("<FocusOut>", lambda e: popup.destroy())
        popup.focus_set()

        canvas = tk.Canvas(popup, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#1a1a1a")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        room_type = self.var_room_type.get()
        all_rooms_of_type = self.rooms_pool.get(room_type, [])

        for index, room_no in enumerate(all_rooms_of_type):
            row = index // 4
            col = index % 4

            if room_no in self.available_rooms_list:
                btn = tk.Button(scroll_frame, text=str(room_no), font=("arial", 10, "bold"), bg="black", fg="gold", width=4, height=1, activebackground="gold", activeforeground="black")
                btn.config(command=lambda r=room_no: [self.var_room_vailable.set(str(r)), popup.destroy()])
            else:
                btn = tk.Button(scroll_frame, text=str(room_no), font=("arial", 10, "bold"), bg="#404040", fg="#808080", width=4, height=1, state="disabled")

            btn.grid(row=row, column=col, padx=3, pady=3)

    def calculate_bill(self):
        if self.var_no_of_days.get().strip() == "":
            return
        try:
            days = int(self.var_no_of_days.get().strip())
            raw_price = self.var_room_price.get().replace("$", "")
            room_price_per_day = float(raw_price) if raw_price else 0.0

            meal_type = self.var_meal.get().strip()
            if meal_type == "Breakfast Only":
                meal_price_per_day = 10.00
            elif meal_type == "Half Board":
                meal_price_per_day = 25.00
            elif meal_type == "Full Board":
                meal_price_per_day = 45.00
            else:
                meal_price_per_day = 0.00

            sub_total = (room_price_per_day + meal_price_per_day) * days
            tax_rate = 0.14
            calculated_tax = sub_total * tax_rate
            total_cost = sub_total + calculated_tax

            self.var_actual_total.set(f"${sub_total:.2f}")
            self.var_paid_tax.set(f"${calculated_tax:.2f}")
            self.var_total.set(f"${total_cost:.2f}")
        except ValueError:
            pass

    # =========================================================================
    # 11. DATABASE CRUD OPERATIONS
    # =========================================================================
    def fetch_contact(self):
        if self.var_contact.get().strip() == "":
            messagebox.showerror("Error", "Please enter Customer Contact number.", parent=self.root)
            return

        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()
            query = "SELECT Name, Gender, Email, Nationality, Address FROM customer WHERE Mobile=%s"
            my_cursor.execute(query, (self.var_contact.get().strip(),))
            row = my_cursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "This contact number is not found.", parent=self.root)
            else:
                for widget in self.inner_frame.winfo_children():
                    widget.destroy()

                labels_data = [("Name:", row[0]), ("Gender:", row[1]), ("Email:", row[2]), ("Nationality:", row[3]), ("Address:", row[4])]
                for i, (title, value) in enumerate(labels_data):
                    lbl_title = tk.Label(self.inner_frame, text=title, font=("arial", 13, "bold"), bg="black", fg="gold")
                    lbl_title.grid(row=i, column=0, sticky="w", pady=6, padx=2)

                    lbl_val = tk.Label(self.inner_frame, text=value, font=("arial", 13, "bold"), bg="black", fg="#ffffff")
                    lbl_val.grid(row=i, column=1, sticky="w", pady=6, padx=10)

                self.inner_frame.update_idletasks()
                self.canvas.config(scrollregion=(0, 0, self.inner_frame.winfo_reqwidth(), self.inner_frame.winfo_reqheight()))
        except Error as es:
            messagebox.showerror("Database Error", f"Something went wrong: {str(es)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def add_data(self):
        if not all([self.var_contact.get().strip(), self.var_check_in.get().strip(), self.var_check_out.get().strip(), self.var_room_vailable.get().strip(), self.var_no_of_days.get().strip(), self.var_meal.get().strip()]):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if not self.is_contact_registered(self.var_contact.get()):
            messagebox.showerror("Error", "This contact number is not registered in Customer database!\nPlease register the customer first.", parent=self.root)
            return

        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()

            # Fixed Duplicate Entry Check: Prevent duplicate input when accidentally clicking 'Add' instead of 'Update'
            check_query = "SELECT * FROM room WHERE Contact=%s AND Room_available=%s AND Check_in=%s"
            my_cursor.execute(check_query, (self.var_contact.get().strip(), int(self.var_room_vailable.get().strip()), self.var_check_in.get().strip()))
            if my_cursor.fetchone():
                messagebox.showerror("Error", "This booking already exists!\nIf you intended to modify it, please use the 'Update' button instead.", parent=self.root)
                return

            query = "INSERT INTO room (Contact, Check_in, Check_out, Room_type, Room_available, Meal, No_of_days) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.var_contact.get().strip(), self.var_check_in.get().strip(), self.var_check_out.get().strip(), self.var_room_type.get().strip(), int(self.var_room_vailable.get().strip()), self.var_meal.get().strip(), int(self.var_no_of_days.get().strip()))

            my_cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Success", "Customer booking has been added successfully", parent=self.root)
            self.reset_data()
            self.fetch_data()
        except Error as es:
            messagebox.showerror("Database Error", f"Something went wrong with the database: {str(es)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def fetch_data(self):
        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT Contact, Check_in, Check_out, Room_type, Room_available, Meal, No_of_days FROM room")
            rows = my_cursor.fetchall()

            self.cust_details_table.delete(*self.cust_details_table.get_children())
            for row in rows:
                self.cust_details_table.insert("", tk.END, values=row)
        except Error as es:
            messagebox.showerror("Database Error", f"Failed to fetch data: {str(es)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def get_cursor(self, event):
        cursor_row = self.cust_details_table.focus()
        if not cursor_row:
            return

        row_data = self.cust_details_table.set(cursor_row)
        if row_data:
            self.entry_cust_contact.config(state="normal")
            self.var_contact.set(row_data.get("contact", ""))
            self.entry_cust_contact.config(state="readonly")

            self.selected_booking_old = (str(row_data.get("contact", "")).strip(), str(row_data.get("room_available", "")).strip(), str(row_data.get("check_in", "")).strip())

            self.entry_check_in.config(maxdate=None, mindate=None)
            self.entry_check_out.config(mindate=None)

            try:
                date_in_str = row_data.get("check_in", "")
                date_in = datetime.strptime(date_in_str, "%Y-%m-%d").date() if "-" in date_in_str else date_in_str
                self.entry_check_in.set_date(date_in)
            except Exception:
                self.var_check_in.set(row_data.get("check_in", ""))

            try:
                date_out_str = row_data.get("check_out", "")
                date_out = datetime.strptime(date_out_str, "%Y-%m-%d").date() if "-" in date_out_str else date_out_str
                self.entry_check_out.set_date(date_out)
            except Exception:
                self.var_check_out.set(row_data.get("check_out", ""))

            self.var_room_type.set(row_data.get("room_type", ""))

            self.refresh_available_rooms()
            self.var_room_vailable.set(row_data.get("room_available", ""))

            self.var_meal.set(row_data.get("meal", ""))
            self.var_no_of_days.set(row_data.get("days", ""))

            self.update_date_limits()
            self.update_room_price()
            self.calculate_bill()
            self.fetch_contact()

    def update_data(self):
        if self.selected_booking_old is None:
            messagebox.showerror("Error", "Please select a record from the table first to update.", parent=self.root)
            return

        current_contact = self.var_contact.get().strip()
        new_room_val = self.var_room_vailable.get().strip()

        if current_contact == "" or new_room_val == "":
            messagebox.showerror("Error", "Contact and Room Number fields cannot be empty.", parent=self.root)
            return

        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()

            query = "UPDATE room SET Check_in=%s, Check_out=%s, Room_type=%s, Room_available=%s, Meal=%s, No_of_days=%s WHERE Contact=%s AND Room_available=%s AND Check_in=%s"
            values = (self.var_check_in.get().strip(), self.var_check_out.get().strip(), self.var_room_type.get().strip(), int(new_room_val), self.var_meal.get().strip(), int(self.var_no_of_days.get().strip()), self.selected_booking_old[0], int(self.selected_booking_old[1]), self.selected_booking_old[2])

            my_cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Update", "Room details updated successfully", parent=self.root)
            self.reset_data()
            self.fetch_data()
        except Error as es:
            messagebox.showerror("Database Error", f"Something went wrong: {str(es)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def remove_data(self):
        if self.selected_booking_old is None:
            messagebox.showerror("Error", "Please select a record from the table first to delete.", parent=self.root)
            return

        lbl_confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this specific booking record?", parent=self.root)
        if lbl_confirm:
            conn, my_cursor = None, None
            try:
                conn = self.get_db_connection()
                my_cursor = conn.cursor()

                query = "DELETE FROM room WHERE Contact=%s AND Room_available=%s AND Check_in=%s"
                my_cursor.execute(query, (self.selected_booking_old[0], int(self.selected_booking_old[1]), self.selected_booking_old[2]))
                conn.commit()

                messagebox.showinfo("Deleted", "Record deleted successfully", parent=self.root)
                self.reset_data()
                self.fetch_data()
            except Error as es:
                messagebox.showerror("Database Error", f"Something went wrong: {str(es)}", parent=self.root)
            finally:
                if conn and conn.is_connected():
                    my_cursor.close()
                    conn.close()

    def search_data(self):
        if self.var_search_by.get().strip() == "" or self.var_search_txt.get().strip() == "":
            messagebox.showerror("Error", "Please select Search By option and type text.", parent=self.root)
            return

        conn, my_cursor = None, None
        try:
            conn = self.get_db_connection()
            my_cursor = conn.cursor()

            field = "Contact" if self.var_search_by.get().strip() == "Contact" else "Room_available"
            query = f"SELECT Contact, Check_in, Check_out, Room_type, Room_available, Meal, No_of_days FROM room WHERE {field} LIKE %s"

            my_cursor.execute(query, ("%" + self.var_search_txt.get().strip() + "%",))
            rows = my_cursor.fetchall()

            self.cust_details_table.delete(*self.cust_details_table.get_children())
            if len(rows) != 0:
                for row in rows:
                    self.cust_details_table.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Search Results", "No matching records found.", parent=self.root)
        except Error as es:
            messagebox.showerror("Database Error", f"Something went wrong: {str(es)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                my_cursor.close()
                conn.close()

    def reset_data(self):
        self.entry_cust_contact.config(state="normal")
        self.var_contact.set("")

        self.selected_booking_old = None
        self.entry_check_in.config(maxdate=None, mindate=None)
        self.entry_check_out.config(mindate=None)
        self.entry_check_in.set_date(datetime.now())
        self.entry_check_out.set_date(datetime.now())
        self.var_room_type.set("Single")
        self.var_room_vailable.set("")
        self.var_meal.set("Breakfast Only")
        self.var_no_of_days.set("")
        self.var_room_price.set("")
        self.var_actual_total.set("")
        self.var_paid_tax.set("")
        self.var_total.set("")
        self.update_room_price()


if __name__ == "__main__":
    root = tk.Tk()
    obj = RoomBooking(root)
    root.mainloop()
