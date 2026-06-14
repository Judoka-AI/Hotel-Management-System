import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
from mysql.connector import Error
from main import HotelManagementSystem


class AdvancedLoginWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System - Login")
        self.root.geometry("1100x650+450+150")
        self.root.resizable(False, False)
        self.root.config(bg="#0B0B0E")

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

        # Database configuration variables
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "root")
        self.db_pass = os.getenv("DB_PASS", "atoui")
        self.db_name = os.getenv("DB_NAME", "management")

        self.initialize_database()

        self.show_pass_login = False
        self.show_pass_register = False

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Premium.TEntry", fieldbackground="#16161E", foreground="#FFFFFF", insertcolor="#FFFFFF", bordercolor="#262633")

        self.create_widgets()

    def initialize_database(self):
        try:
            conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            cursor.execute(f"USE {self.db_name}")

            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
        except Error as e:
            messagebox.showerror("Database Initialization Error", f"Could not setup database:\n{str(e)}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_widgets(self):
        left_panel = tk.Frame(self.root, bg="#111116", width=450, height=650, bd=0, highlightthickness=0)
        left_panel.place(x=0, y=0)

        gold_line = tk.Frame(left_panel, bg="#C5A059", width=4, height=250)
        gold_line.place(x=50, y=200)

        brand_lbl = tk.Label(left_panel, text="THE LUXE", font=("Cinzel", 28, "bold"), fg="#C5A059", bg="#111116")
        brand_lbl.place(x=70, y=200)

        sub_brand_lbl = tk.Label(left_panel, text="H O T E L  &  R E S O R T", font=("Montserrat", 10, "bold"), fg="#8A8A93", bg="#111116")
        sub_brand_lbl.place(x=73, y=255)

        desc_lbl = tk.Label(left_panel, text="Welcome to the next generation of luxury\nmanagement interfaces. Secure & sleek.", font=("Segoe UI", 9), fg="#555562", bg="#111116", justify="left")
        desc_lbl.place(x=73, y=300)

        self.right_container = tk.Frame(self.root, bg="#0B0B0E", width=650, height=650)
        self.right_container.place(x=450, y=0)

        self.show_login_interface()

    def show_login_interface(self):
        for widget in self.right_container.winfo_children():
            widget.destroy()

        title = tk.Label(self.right_container, text="Sign In", font=("Segoe UI", 26, "bold"), fg="#FFFFFF", bg="#0B0B0E")
        title.place(x=100, y=100)

        subtitle = tk.Label(self.right_container, text="Please enter your credentials to proceed.", font=("Segoe UI", 10), fg="#8A8A93", bg="#0B0B0E")
        subtitle.place(x=100, y=150)

        tk.Label(self.right_container, text="Username", font=("Segoe UI", 10, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=100, y=210)
        self.txt_login_user = ttk.Entry(self.right_container, font=("Segoe UI", 12), style="Premium.TEntry", width=38)
        self.txt_login_user.place(x=100, y=240, height=40)

        tk.Label(self.right_container, text="Password", font=("Segoe UI", 10, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=100, y=310)
        self.txt_login_pass = ttk.Entry(self.right_container, font=("Segoe UI", 12), style="Premium.TEntry", width=38, show="*")
        self.txt_login_pass.place(x=100, y=340, height=40)

        self.btn_toggle_login_pass = tk.Button(self.right_container, text="👁", font=("Segoe UI", 11), bg="#16161E", fg="#8A8A93", activebackground="#16161E", activeforeground="#C5A059", bd=0, cursor="hand2", command=self.toggle_login_password)
        self.btn_toggle_login_pass.place(x=455, y=342, width=35, height=36)

        btn_login = tk.Button(self.right_container, text="LOGIN", font=("Segoe UI", 11, "bold"), bg="#C5A059", fg="#0B0B0E", activebackground="#A38144", activeforeground="#0B0B0E", bd=0, cursor="hand2", command=self.handle_login)
        btn_login.place(x=100, y=420, width=390, height=45)
        self.bind_hover(btn_login, "#C5A059", "#A38144")

        switch_lbl = tk.Label(self.right_container, text="Don't have an account?", font=("Segoe UI", 10), fg="#8A8A93", bg="#0B0B0E")
        switch_lbl.place(x=180, y=500)

        btn_switch = tk.Button(self.right_container, text="Create New Account", font=("Segoe UI", 10, "bold", "underline"), bg="#0B0B0E", fg="#C5A059", activebackground="#0B0B0E", activeforeground="#FFFFFF", bd=0, cursor="hand2", command=self.show_register_interface)
        btn_switch.place(x=325, y=498)

    def show_register_interface(self):
        for widget in self.right_container.winfo_children():
            widget.destroy()

        title = tk.Label(self.right_container, text="Create Account", font=("Segoe UI", 26, "bold"), fg="#FFFFFF", bg="#0B0B0E")
        title.place(x=100, y=60)

        subtitle = tk.Label(self.right_container, text="Join us to get full access to the administration panel.", font=("Segoe UI", 10), fg="#8A8A93", bg="#0B0B0E")
        subtitle.place(x=100, y=110)

        tk.Label(self.right_container, text="Username", font=("Segoe UI", 10, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=100, y=160)
        self.txt_reg_user = ttk.Entry(self.right_container, font=("Segoe UI", 12), style="Premium.TEntry", width=38)
        self.txt_reg_user.place(x=100, y=190, height=40)

        tk.Label(self.right_container, text="Email Address", font=("Segoe UI", 10, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=100, y=250)
        self.txt_reg_email = ttk.Entry(self.right_container, font=("Segoe UI", 12), style="Premium.TEntry", width=38)
        self.txt_reg_email.place(x=100, y=280, height=40)

        tk.Label(self.right_container, text="Password", font=("Segoe UI", 10, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=100, y=340)
        self.txt_reg_pass = ttk.Entry(self.right_container, font=("Segoe UI", 12), style="Premium.TEntry", width=38, show="*")
        self.txt_reg_pass.place(x=100, y=370, height=40)

        self.btn_toggle_reg_pass = tk.Button(self.right_container, text="👁", font=("Segoe UI", 11), bg="#16161E", fg="#8A8A93", activebackground="#16161E", activeforeground="#C5A059", bd=0, cursor="hand2", command=self.toggle_register_password)
        self.btn_toggle_reg_pass.place(x=455, y=372, width=35, height=36)

        btn_register = tk.Button(self.right_container, text="REGISTER", font=("Segoe UI", 11, "bold"), bg="#C5A059", fg="#0B0B0E", activebackground="#A38144", activeforeground="#0B0B0E", bd=0, cursor="hand2", command=self.handle_registration)
        btn_register.place(x=100, y=450, width=390, height=45)
        self.bind_hover(btn_register, "#C5A059", "#A38144")

        switch_lbl = tk.Label(self.right_container, text="Already have an account?", font=("Segoe UI", 10), fg="#8A8A93", bg="#0B0B0E")
        switch_lbl.place(x=185, y=520)

        btn_switch = tk.Button(self.right_container, text="Sign In", font=("Segoe UI", 10, "bold", "underline"), bg="#0B0B0E", fg="#C5A059", activebackground="#0B0B0E", activeforeground="#FFFFFF", bd=0, cursor="hand2", command=self.show_login_interface)
        btn_switch.place(x=345, y=518)

    def toggle_login_password(self):
        if self.show_pass_login:
            self.txt_login_pass.config(show="*")
            self.btn_toggle_login_pass.config(fg="#8A8A93")
            self.show_pass_login = False
        else:
            self.txt_login_pass.config(show="")
            self.btn_toggle_login_pass.config(fg="#C5A059")
            self.show_pass_login = True

    def toggle_register_password(self):
        if self.show_pass_register:
            self.txt_reg_pass.config(show="*")
            self.btn_toggle_reg_pass.config(fg="#8A8A93")
            self.show_pass_register = False
        else:
            self.txt_reg_pass.config(show="")
            self.btn_toggle_reg_pass.config(fg="#C5A059")
            self.show_pass_register = True

    def bind_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    def handle_login(self):
        username = self.txt_login_user.get().strip()
        password = self.txt_login_pass.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        hashed_password = self.hash_password(password)
        conn = None
        try:
            conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", f"Welcome back, {username}!", parent=self.root)
                for widget in self.root.winfo_children():
                    widget.destroy()
                app = HotelManagementSystem(self.root, username=username)
            else:
                messagebox.showerror("Error", "Invalid Username or Password.", parent=self.root)
        except Error as e:
            messagebox.showerror("Database Error", f"Connection failed: {str(e)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def handle_registration(self):
        """Processes and strictly validates emails during user sign up"""
        username = self.txt_reg_user.get().strip()
        email = self.txt_reg_email.get().strip()
        password = self.txt_reg_pass.get().strip()

        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required for registration!", parent=self.root)
            return

        # Strict checks on email formatting and presence
        if "@" not in email or "." not in email or len(email) < 5:
            messagebox.showerror("Data Error", "Please provide a valid email address.", parent=self.root)
            return

        hashed_password = self.hash_password(password)
        conn = None
        try:
            conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
            cursor = conn.cursor()

            # Prevent duplicate user credentials from being registered
            check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
            cursor.execute(check_query, (username, email))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Username or Email address already exists in the system!", parent=self.root)
                return

            insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (username, email, hashed_password))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully! You can now log in.", parent=self.root)
            self.show_login_interface()
        except Error as e:
            messagebox.showerror("Database Error", f"Registration failed: {str(e)}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedLoginWin(root)
    root.mainloop()
