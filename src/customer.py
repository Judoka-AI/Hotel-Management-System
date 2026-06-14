from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import random
from tkinter import messagebox
import mysql.connector
import os


class Cust_Win:
    def __init__(self, root):
        # Window Configuration
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1310x570+235+225")
        self.root.resizable(False, False)

        # Customer Variables
        self.var_ref = StringVar()
        self.generate_unique_ref()

        self.var_name = StringVar()
        self.var_family = StringVar()
        self.var_gender = StringVar()
        self.var_post = StringVar()
        self.var_mobile = StringVar()
        self.var_email = StringVar()
        self.var_nationality = StringVar()
        self.var_idproof = StringVar()
        self.var_idnumber = StringVar()
        self.var_address = StringVar()

        # UI Styling and Theme Configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Thin.Horizontal.TScrollbar", arrowsize=9, thickness=8, background="#333333", troughcolor="black", bordercolor="black", gripcount=0)
        self.style.configure("Custom.TCombobox", selectbackground="white", selectforeground="black", fieldbackground="white", background="white")
        self.style.map("Custom.TCombobox", selectbackground=[("readonly", "white"), ("focus", "white")], selectforeground=[("readonly", "black"), ("focus", "black")], fieldbackground=[("readonly", "white")])
        self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=25, font=("arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#4E4E4E")], foreground=[("selected", "gold")])
        self.style.configure("Treeview.Heading", background="#313131", foreground="gold", font=("arial", 11, "bold"))
        self.style.map("Treeview.Heading", background=[("active", "#636363")])

        # Title Label
        lbl_title = Label(self.root, text="Customer Details".upper(), font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1310, height=50)

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

        # Logo Loading
        try:
            logo = Image.open(r"imgs\logo1.png")
            logo = logo.resize((90, 50), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo)
            lbl_logo = Label(self.root, image=self.logo, bd=0, relief=RIDGE)
            lbl_logo.place(x=3, y=3, width=90, height=40)
        except:
            pass

        # Left Input Frame
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Customer Details", font=("times new roman", 12, "bold"), pady=2)
        labelframeleft.place(x=5, y=50, width=425, height=510)

        # Form Entry Fields
        lbl_cust_ref = Label(labelframeleft, text="Customer Ref", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_cust_ref.grid(row=0, column=0, sticky=W)
        entry_cust_ref = ttk.Entry(labelframeleft, textvariable=self.var_ref, width=29, font=("arial", 13, "bold"), state="readonly")
        entry_cust_ref.grid(row=0, column=1)

        lbl_cust_name = Label(labelframeleft, text="First Name", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_cust_name.grid(row=1, column=0, sticky=W)
        entry_cust_name = ttk.Entry(labelframeleft, textvariable=self.var_name, width=29, font=("arial", 13, "bold"))
        entry_cust_name.grid(row=1, column=1)

        lbl_cust_family = Label(labelframeleft, text="Family Name", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_cust_family.grid(row=2, column=0, sticky=W)
        entry_cust_family = ttk.Entry(labelframeleft, textvariable=self.var_family, width=29, font=("arial", 13, "bold"))
        entry_cust_family.grid(row=2, column=1)

        lbl_gender = Label(labelframeleft, text="Gender", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_gender.grid(row=3, column=0, sticky=W)
        combo_gender = ttk.Combobox(labelframeleft, textvariable=self.var_gender, font=("arial", 13, "bold"), width=27, state="readonly", style="Custom.TCombobox")
        combo_gender["value"] = ("Male", "Female", "Other")
        combo_gender.current(0)
        combo_gender.grid(row=3, column=1)

        lbl_cust_postcode = Label(labelframeleft, text="PostCode", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_cust_postcode.grid(row=4, column=0, sticky=W)
        entry_cust_postcode = ttk.Entry(labelframeleft, textvariable=self.var_post, width=29, font=("arial", 13, "bold"))
        entry_cust_postcode.grid(row=4, column=1)

        lbl_mobile = Label(labelframeleft, text="Mobile", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_mobile.grid(row=5, column=0, sticky=W)
        entry_mobile = ttk.Entry(labelframeleft, textvariable=self.var_mobile, width=29, font=("arial", 13, "bold"))
        entry_mobile.grid(row=5, column=1)

        lbl_email = Label(labelframeleft, text="Email", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_email.grid(row=6, column=0, sticky=W)
        entry_email = ttk.Entry(labelframeleft, textvariable=self.var_email, width=29, font=("arial", 13, "bold"))
        entry_email.grid(row=6, column=1)

        lbl_nationality = Label(labelframeleft, text="Nationality", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_nationality.grid(row=7, column=0, sticky=W)
        combo_nationality = ttk.Combobox(labelframeleft, textvariable=self.var_nationality, font=("arial", 13, "bold"), width=27, state="readonly", style="Custom.TCombobox")
        combo_nationality["values"] = ("Moroccan", "Algerian", "Tunisian", "Egyptian", "Saudi", "Emirati", "Jordanian", "Omani", "Kuwaiti", "Bahraini", "Qatari", "Lebanese", "Syrian", "Palestinian", "Iraqi", "Yemeni", "Sudanese", "Libyan")
        combo_nationality.current(1)
        combo_nationality.grid(row=7, column=1)

        lbl_proof_id = Label(labelframeleft, text="ID Proof Type", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_proof_id.grid(row=8, column=0, sticky=W)
        combo_idproof = ttk.Combobox(labelframeleft, textvariable=self.var_idproof, font=("arial", 13, "bold"), width=27, state="readonly", style="Custom.TCombobox")
        combo_idproof["values"] = ("National ID", "Passport", "Driving License")
        combo_idproof.current(0)
        combo_idproof.grid(row=8, column=1)

        lbl_idnum = Label(labelframeleft, text="ID Number", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_idnum.grid(row=9, column=0, sticky=W)
        entry_idnum = ttk.Entry(labelframeleft, textvariable=self.var_idnumber, width=29, font=("arial", 13, "bold"))
        entry_idnum.grid(row=9, column=1)

        lbl_address = Label(labelframeleft, text="Address", font=("arial", 12, "bold"), padx=15, pady=6)
        lbl_address.grid(row=10, column=0, sticky=W)
        entry_address = ttk.Entry(labelframeleft, textvariable=self.var_address, width=29, font=("arial", 13, "bold"))
        entry_address.grid(row=10, column=1)

        # Control Buttons Frame
        btn_frame = Frame(labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=3, y=420, width=412, height=40)

        btn_add = Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_add.grid(row=0, column=0, padx=1, pady=1.5)

        btn_update = Button(btn_frame, text="Update", command=self.update_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_update.grid(row=0, column=1, padx=1, pady=1.5)

        btn_remove = Button(btn_frame, text="Remove", command=self.delete_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_remove.grid(row=0, column=2, padx=1, pady=1.5)

        btn_reset = Button(btn_frame, text="Reset", command=self.reset_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_reset.grid(row=0, column=3, padx=1, pady=1.5)

        # Hover Effects for Buttons
        def on_enter(event):
            event.widget.config(bg="#3b3a3a", fg="gold")

        def on_leave(event):
            event.widget.config(bg="black", fg="gold")

        btn_add.bind("<Enter>", on_enter)
        btn_add.bind("<Leave>", on_leave)
        btn_remove.bind("<Enter>", on_enter)
        btn_remove.bind("<Leave>", on_leave)
        btn_update.bind("<Enter>", on_enter)
        btn_update.bind("<Leave>", on_leave)
        btn_reset.bind("<Enter>", on_enter)
        btn_reset.bind("<Leave>", on_leave)

        # Right Data Display Frame
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details and Search System", font=("times new roman", 12, "bold"), pady=2)
        table_frame.place(x=440, y=50, width=860, height=510)

        # Search Controls
        lbl_search = Label(table_frame, text="Search By:", font=("arial", 12, "bold"), fg="gold", bg="black", padx=6, pady=2)
        lbl_search.grid(row=0, column=0, padx=2)

        self.combo_search = ttk.Combobox(table_frame, font=("arial", 13, "bold"), width=18, state="readonly", style="Custom.TCombobox")
        self.combo_search["values"] = ("Mobile", "Ref", "Name", "ID Number")
        self.combo_search.current(0)
        self.combo_search.grid(row=0, column=1, padx=2)

        self.entry_search_address = ttk.Entry(table_frame, width=22, font=("arial", 13, "bold"))
        self.entry_search_address.grid(row=0, column=2, padx=2)

        btn_search = Button(table_frame, text="Search", command=self.search_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_search.grid(row=0, column=3, padx=2)
        btn_search.bind("<Enter>", on_enter)
        btn_search.bind("<Leave>", on_leave)

        btn_show_all = Button(table_frame, text="Show All", command=self.fetch_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10, cursor="hand2")
        btn_show_all.grid(row=0, column=4, padx=2)
        btn_show_all.bind("<Enter>", on_enter)
        btn_show_all.bind("<Leave>", on_leave)

        # Data Table Setup (Treeview)
        details_table = Frame(table_frame, bd=2, relief=RIDGE)
        details_table.place(x=13, y=70, width=830, height=350)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.cust_details_table = ttk.Treeview(details_table, columns=("ref", "name", "family", "gender", "post", "mobile", "email", "nationality", "idproof", "idnumber", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.cust_details_table.xview)
        scroll_y.config(command=self.cust_details_table.yview)

        self.cust_details_table.heading("ref", text="Refer No")
        self.cust_details_table.heading("name", text="Name")
        self.cust_details_table.heading("family", text="Family")
        self.cust_details_table.heading("gender", text="Gender")
        self.cust_details_table.heading("post", text="PostCode")
        self.cust_details_table.heading("mobile", text="Mobile")
        self.cust_details_table.heading("email", text="Email")
        self.cust_details_table.heading("nationality", text="Nationality")
        self.cust_details_table.heading("idproof", text="ID Proof")
        self.cust_details_table.heading("idnumber", text="ID Number")
        self.cust_details_table.heading("address", text="Address")

        self.cust_details_table["show"] = "headings"

        self.cust_details_table.column("ref", width=100)
        self.cust_details_table.column("name", width=100)
        self.cust_details_table.column("family", width=100)
        self.cust_details_table.column("gender", width=100)
        self.cust_details_table.column("post", width=100)
        self.cust_details_table.column("mobile", width=150)
        self.cust_details_table.column("email", width=150)
        self.cust_details_table.column("nationality", width=100)
        self.cust_details_table.column("idproof", width=100)
        self.cust_details_table.column("idnumber", width=100)
        self.cust_details_table.column("address", width=100)
        self.cust_details_table.pack(fill=BOTH, expand=1)
        self.cust_details_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    def generate_unique_ref(self):
        """Generates a random 4-digit unique reference number and verifies it against the database."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
            my_cursor = conn.cursor()
            while True:
                x = random.randint(1000, 9999)
                my_cursor.execute("SELECT * FROM customer WHERE Ref = %s", (str(x),))
                if my_cursor.fetchone() is None:
                    self.var_ref.set(str(x))
                    break
            conn.close()
        except:
            self.var_ref.set(str(random.randint(1000, 9999)))

    def add_data(self):
        """Validates entry fields, checks for duplicate mobile/ID numbers, and inserts new record into database."""
        if self.var_name.get().strip() == "" or self.var_family.get().strip() == "" or self.var_gender.get().strip() == "" or self.var_post.get().strip() == "" or self.var_mobile.get().strip() == "" or self.var_email.get().strip() == "" or self.var_nationality.get().strip() == "" or self.var_idproof.get().strip() == "" or self.var_idnumber.get().strip() == "" or self.var_address.get().strip() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
                my_cursor = conn.cursor()

                check_query = "SELECT Mobile, IdNumber FROM customer WHERE Mobile = %s OR IdNumber = %s"
                my_cursor.execute(check_query, (self.var_mobile.get().strip(), self.var_idnumber.get().strip()))
                row = my_cursor.fetchone()

                if row is not None:
                    if row[0] == self.var_mobile.get().strip():
                        messagebox.showerror("Error", "This Mobile Number already exists!", parent=self.root)
                    else:
                        messagebox.showerror("Error", "This ID Number already exists!", parent=self.root)
                    conn.close()
                    return

                my_cursor.execute("SELECT * FROM customer WHERE Ref = %s", (self.var_ref.get().strip(),))
                if my_cursor.fetchone() is not None:
                    self.generate_unique_ref()

                query = "INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (self.var_ref.get().strip(), self.var_name.get().strip(), self.var_family.get().strip(), self.var_gender.get().strip(), self.var_post.get().strip(), self.var_mobile.get().strip(), self.var_email.get().strip(), self.var_nationality.get().strip(), self.var_idproof.get().strip(), self.var_idnumber.get().strip(), self.var_address.get().strip())

                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Customer has been added successfully", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def fetch_data(self):
        """Retrieves all customer records from the database and populates the Treeview table."""
        conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from customer")
        rows = my_cursor.fetchall()

        self.cust_details_table.delete(*self.cust_details_table.get_children())
        if len(rows) != 0:
            for i in rows:
                self.cust_details_table.insert("", END, values=i)
        conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        """Fetches data from the selected row in the table and fills the input fields."""
        cursor_row = self.cust_details_table.focus()
        if not cursor_row:
            return
        row_data = self.cust_details_table.set(cursor_row)

        if row_data:
            self.var_ref.set(row_data.get("ref", ""))
            self.var_name.set(row_data.get("name", ""))
            self.var_family.set(row_data.get("family", ""))
            self.var_gender.set(row_data.get("gender", ""))
            self.var_post.set(row_data.get("post", ""))
            self.var_mobile.set(row_data.get("mobile", ""))
            self.var_email.set(row_data.get("email", ""))
            self.var_nationality.set(row_data.get("nationality", ""))
            self.var_idproof.set(row_data.get("idproof", ""))
            self.var_idnumber.set(row_data.get("idnumber", ""))
            self.var_address.set(row_data.get("address", ""))

    def update_data(self):
        """Updates customer profile details and synchronizes mobile updates across related database tables."""
        if self.var_name.get().strip() == "" or self.var_family.get().strip() == "" or self.var_gender.get().strip() == "" or self.var_post.get().strip() == "" or self.var_mobile.get().strip() == "" or self.var_email.get().strip() == "" or self.var_nationality.get().strip() == "" or self.var_idproof.get().strip() == "" or self.var_idnumber.get().strip() == "" or self.var_address.get().strip() == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT Mobile FROM customer WHERE Ref = %s", (self.var_ref.get().strip(),))
                old_mobile_row = my_cursor.fetchone()

                if old_mobile_row:
                    old_mobile = str(old_mobile_row[0]).strip()
                    if old_mobile.endswith(".0"):
                        old_mobile = old_mobile[:-2]
                else:
                    old_mobile = None

                check_query = "SELECT Mobile, IdNumber FROM customer WHERE (Mobile = %s OR IdNumber = %s) AND Ref != %s"
                my_cursor.execute(check_query, (self.var_mobile.get().strip(), self.var_idnumber.get().strip(), self.var_ref.get().strip()))
                row = my_cursor.fetchone()

                if row is not None:
                    if row[0] == self.var_mobile.get().strip():
                        messagebox.showerror("Error", "This Mobile Number is already assigned to another customer!", parent=self.root)
                    else:
                        messagebox.showerror("Error", "This ID Number is already assigned to another customer!", parent=self.root)
                    conn.close()
                    return

                new_mobile = self.var_mobile.get().strip()
                if new_mobile.endswith(".0"):
                    new_mobile = new_mobile[:-2]

                if old_mobile:
                    query_room = "UPDATE room SET Contact=%s WHERE Contact=%s"
                    my_cursor.execute(query_room, (new_mobile, old_mobile))

                query_customer = """UPDATE customer SET 
                            Name=%s, Family=%s, Gender=%s, PostCode=%s, Mobile=%s, 
                            Email=%s, Nationality=%s, IdProof=%s, IdNumber=%s, Address=%s 
                           WHERE Ref=%s"""

                values = (self.var_name.get().strip(), self.var_family.get().strip(), self.var_gender.get().strip(), self.var_post.get().strip(), new_mobile, self.var_email.get().strip(), self.var_nationality.get().strip(), self.var_idproof.get().strip(), self.var_idnumber.get().strip(), self.var_address.get().strip(), self.var_ref.get().strip())

                my_cursor.execute(query_customer, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Customer details and their room contact have been updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)

    def delete_data(self):
        """Deletes customer account along with their related room booking details from the database."""
        if not self.cust_details_table.focus():
            messagebox.showerror("Error", "Please select a customer from the table first!", parent=self.root)
        else:
            m_delete = messagebox.askyesno("Hotel Management System", "Do you really want to delete this customer? This will also remove their room bookings.", parent=self.root)
            if m_delete > 0:
                try:
                    conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
                    my_cursor = conn.cursor()

                    customer_mobile = self.var_mobile.get().strip()

                    if customer_mobile.endswith(".0"):
                        customer_mobile = customer_mobile[:-2]

                    if customer_mobile == "":
                        messagebox.showerror("Error", "Mobile number is empty or invalid!", parent=self.root)
                        conn.close()
                        return

                    query_room = "DELETE FROM room WHERE Contact=%s"
                    my_cursor.execute(query_room, (customer_mobile,))

                    query_customer = "DELETE FROM customer WHERE Mobile=%s"
                    my_cursor.execute(query_customer, (customer_mobile,))

                    conn.commit()
                    self.fetch_data()
                    conn.close()

                    messagebox.showinfo("Success", "Customer and their room data have been deleted successfully", parent=self.root)
                    self.reset_data()
                except Exception as es:
                    messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)
            else:
                return

    def reset_data(self):
        """Resets all entry fields to their default values and generates a new unique reference code."""
        self.generate_unique_ref()

        self.var_name.set("")
        self.var_family.set("")
        self.var_gender.set("Male")
        self.var_post.set("")
        self.var_mobile.set("")
        self.var_email.set("")
        self.var_nationality.set("Algerian")
        self.var_idproof.set("National ID")
        self.var_idnumber.set("")
        self.var_address.set("")

    def search_data(self):
        """Searches the database based on the selected filter criteria and displays results in the table."""
        if self.entry_search_address.get().strip() == "":
            messagebox.showerror("Error", "Please enter what you want to search for", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="atoui", database="management")
                my_cursor = conn.cursor()

                search_by = self.combo_search.get().strip()
                search_txt = self.entry_search_address.get().strip()

                if search_by == "Mobile":
                    query = "SELECT * FROM customer WHERE Mobile LIKE %s"
                elif search_by == "Ref":
                    query = "SELECT * FROM customer WHERE Ref LIKE %s"
                elif search_by == "Name":
                    query = "SELECT * FROM customer WHERE Name LIKE %s"
                elif search_by == "ID Number":
                    query = "SELECT * FROM customer WHERE IdNumber LIKE %s"

                my_cursor.execute(query, (f"%{search_txt}%",))
                rows = my_cursor.fetchall()

                self.cust_details_table.delete(*self.cust_details_table.get_children())
                if len(rows) != 0:
                    for i in rows:
                        self.cust_details_table.insert("", END, values=i)
                else:
                    messagebox.showinfo("Information", "No record found", parent=self.root)

                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = Cust_Win(root)
    root.mainloop()
