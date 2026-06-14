from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import hashlib
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import webbrowser
from customer import Cust_Win
from room import RoomBooking
from details import DetailsWin


class HotelManagementSystem:
    def __init__(self, root, username="Admin"):
        self.root = root
        self.username = username
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")
        self.root.resizable(False, False)

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

        self.current_win = None

        # Database configuration
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "root")
        self.db_pass = os.getenv("DB_PASS", "atoui")
        self.db_name = os.getenv("DB_NAME", "management")

        # ================== Top Image ================
        try:
            img1_path = os.path.join(self.base_dir, "imgs", "img1.png")
            img1 = Image.open(img1_path)
            img1 = img1.resize((1550, 140), Image.LANCZOS)
            self.img1 = ImageTk.PhotoImage(img1)
            lbl_img1 = Label(self.root, image=self.img1, bd=4, relief=RIDGE)
            lbl_img1.place(x=230, y=0, width=1320, height=140)
        except Exception as e:
            print(f"Top img1 is not found: {e}")

        # ================== Logo ================
        try:
            logo_path = os.path.join(self.base_dir, "imgs", "logo.png")
            logo = Image.open(logo_path)
            logo = logo.resize((230, 140), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo)
            lbl_logo = Label(self.root, image=self.logo, bd=4, relief=RIDGE)
            lbl_logo.place(x=0, y=0, width=230, height=140)
        except Exception as e:
            print(f"Logo is not found: {e}")

        # ================== Title ================
        lbl_title = Label(self.root, text="Hotel Management System".upper(), font=("times new roman", 40, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=140, width=1550, height=50)

        # ================== Main Frame ================
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=610)

        # ================== Menu ================
        lbl_menu = Label(main_frame, text="MENU", font=("times new roman", 20, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_menu.place(x=0, y=0, width=230, height=35)

        # ================== Btn Frame ================
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE, bg="#7D6732")
        btn_frame.place(x=1, y=35, width=228, height=190)

        cust_btn = Button(btn_frame, text="CUSTOMER", width=22, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand2", command=self.cust_details)
        cust_btn.grid(row=0, column=0, pady=1)

        room_btn = Button(btn_frame, text="ROOM", width=22, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand2", command=self.room_details)
        room_btn.grid(row=1, column=0, pady=1)

        details_btn = Button(btn_frame, text="DETAILS", width=22, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand2", command=self.details_win)
        details_btn.grid(row=2, column=0, pady=1)

        about_btn = Button(btn_frame, text="ABOUT", width=22, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand2", command=self.open_about)
        about_btn.grid(row=3, column=0, pady=1)

        profile_btn = Button(btn_frame, text="PROFILE", width=22, font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0, cursor="hand2", command=self.open_profile)
        profile_btn.grid(row=4, column=0, pady=1)

        def on_enter(event):
            event.widget.config(bg="#3b3a3a", fg="gold")

        def on_leave(event):
            event.widget.config(bg="black", fg="gold")

        cust_btn.bind("<Enter>", on_enter)
        cust_btn.bind("<Leave>", on_leave)
        room_btn.bind("<Enter>", on_enter)
        room_btn.bind("<Leave>", on_leave)
        details_btn.bind("<Enter>", on_enter)
        details_btn.bind("<Leave>", on_leave)
        about_btn.bind("<Enter>", on_enter)
        about_btn.bind("<Leave>", on_leave)
        profile_btn.bind("<Enter>", on_enter)
        profile_btn.bind("<Leave>", on_leave)

        # ================== Right Side Image ================
        try:
            img2_path = os.path.join(self.base_dir, "imgs", "img2.png")
            img2 = Image.open(img2_path)
            img2 = img2.resize((1315, 606), Image.LANCZOS)
            self.img2 = ImageTk.PhotoImage(img2)
            lbl_img2 = Label(main_frame, image=self.img2, bd=4, relief=RIDGE)
            lbl_img2.place(x=230, y=0, width=1315, height=606)
        except Exception as e:
            print(f"Img2 is not found: {e}")

        # ================== Down Images ================
        try:
            img3_path = os.path.join(self.base_dir, "imgs", "img3.png")
            img3 = Image.open(img3_path)
            img3 = img3.resize((233, 210), Image.LANCZOS)
            self.img3 = ImageTk.PhotoImage(img3)
            lbl_img3 = Label(main_frame, image=self.img3, bd=4, relief=RIDGE)
            lbl_img3.place(x=0, y=225, width=233, height=210)
        except Exception as e:
            print(f"Img3 is not found: {e}")

        try:
            img4_path = os.path.join(self.base_dir, "imgs", "img4.png")
            img4 = Image.open(img4_path)
            img4 = img4.resize((233, 176), Image.LANCZOS)
            self.img4 = ImageTk.PhotoImage(img4)
            lbl_img4 = Label(main_frame, image=self.img4, bd=4, relief=RIDGE)
            lbl_img4.place(x=0, y=430, width=233, height=176)
        except Exception as e:
            print(f"Img4 is not found: {e}")

    def close_current_window(self):
        if self.current_win is not None:
            try:
                self.current_win.destroy()
            except:
                pass
            self.current_win = None

    def apply_sub_icon(self, window):
        try:
            if hasattr(self, "icon_img"):
                window.iconphoto(False, self.icon_img)
        except:
            pass

    def cust_details(self):
        self.close_current_window()
        self.new_window = Toplevel(self.root)
        self.apply_sub_icon(self.new_window)
        self.app = Cust_Win(self.new_window)
        self.current_win = self.new_window

    def room_details(self):
        self.close_current_window()
        self.new_window = Toplevel(self.root)
        self.apply_sub_icon(self.new_window)
        self.app = RoomBooking(self.new_window)
        self.current_win = self.new_window

    def details_win(self):
        self.close_current_window()
        self.new_window = Toplevel(self.root)
        self.apply_sub_icon(self.new_window)
        self.app = DetailsWin(self.new_window)
        self.current_win = self.new_window

    def open_about(self):
        self.close_current_window()
        self.new_window = Toplevel(self.root)
        self.apply_sub_icon(self.new_window)
        self.new_window.title("About Developer & System")
        self.new_window.geometry("460x600+550+100")
        self.new_window.config(bg="#0B0B0E")
        self.new_window.resizable(False, False)
        self.current_win = self.new_window

        Label(self.new_window, text="ABOUT THE SYSTEM", font=("Segoe UI", 14, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=50, y=25)
        sys_desc = "Hotel Management System v1.0\nA premium desktop application designed to streamline hotel operations, handle customer details, manage room bookings, and visualize data insightfully."
        lbl_sys = Label(self.new_window, text=sys_desc, font=("Segoe UI", 10), fg="#FFFFFF", bg="#16161E", justify="left", anchor="nw", padx=12, pady=10, wraplength=335)
        lbl_sys.place(x=50, y=55, width=360, height=85)

        Label(self.new_window, text="THE DEVELOPER", font=("Segoe UI", 14, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=50, y=165)
        dev_desc = "Name: Atoui\nRole: Full-Stack Software Engineer & UI/UX Designer\nFocus: Robust Desktop Apps & Database Management Solutions."
        lbl_dev = Label(self.new_window, text=dev_desc, font=("Segoe UI", 10), fg="#FFFFFF", bg="#16161E", justify="left", anchor="nw", padx=12, pady=10, wraplength=335)
        lbl_dev.place(x=50, y=195, width=360, height=85)

        Label(self.new_window, text="DEVELOPER CAPABILITIES", font=("Segoe UI", 12, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=50, y=305)
        skills = "• Advanced Python Development (Tkinter, OOP, Async)\n• Database Architecture & Query Optimization (MySQL)\n• Secure Systems Engineering (Data Hashing, Secure Login)\n• Clean, Modern & Responsive UI/UX Architectures"
        lbl_skills = Label(self.new_window, text=skills, font=("Segoe UI", 9), fg="#8A8A93", bg="#0B0B0E", justify="left", anchor="nw")
        lbl_skills.place(x=50, y=340, width=360, height=110)

        def open_github():
            webbrowser.open_new_tab("https://github.com/Judoka-AI")

        btn_github = Button(self.new_window, text="VISIT MY GITHUB PROFILE", font=("Segoe UI", 11, "bold"), bg="#C5A059", fg="#0B0B0E", activebackground="#A38144", bd=0, cursor="hand2", command=open_github)
        btn_github.place(x=50, y=490, width=360, height=42)

    def open_profile(self):
        self.close_current_window()
        self.new_window = Toplevel(self.root)
        self.apply_sub_icon(self.new_window)
        self.new_window.title("Profile & User Management")
        self.new_window.geometry("480x640+550+80")
        self.new_window.config(bg="#0B0B0E")
        self.new_window.resizable(False, False)
        self.current_win = self.new_window

        email_str = ""
        try:
            conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username = %s", (self.username,))
            res = cursor.fetchone()
            if res:
                email_str = res[0]
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error fetching profile details: {e}")

        tab_bar = Frame(self.new_window, bg="#121218", height=45)
        tab_bar.place(x=20, y=20, width=440, height=45)

        container = Frame(self.new_window, bg="#0B0B0E")
        container.place(x=20, y=85, width=440, height=535)

        tab1_frame = Frame(container, bg="#0B0B0E")
        tab2_frame = Frame(container, bg="#0B0B0E")

        line_tab1 = Frame(tab_bar, bg="#C5A059")
        line_tab2 = Frame(tab_bar, bg="#C5A059")

        def show_tab1():
            tab2_frame.place_forget()
            tab1_frame.place(x=0, y=0, width=440, height=535)
            btn_tab1.config(fg="#C5A059", font=("Segoe UI", 11, "bold"))
            btn_tab2.config(fg="#626270", font=("Segoe UI", 11, "normal"))
            line_tab1.place(x=0, y=42, width=220, height=3)
            line_tab2.place_forget()

        def show_tab2():
            tab1_frame.place_forget()
            tab2_frame.place(x=0, y=0, width=440, height=535)
            btn_tab2.config(fg="#C5A059", font=("Segoe UI", 11, "bold"))
            btn_tab1.config(fg="#626270", font=("Segoe UI", 11, "normal"))
            line_tab2.place(x=220, y=42, width=220, height=3)
            line_tab1.place_forget()

        btn_tab1 = Button(tab_bar, text="MY ACCOUNT", bg="#121218", fg="#C5A059", font=("Segoe UI", 11, "bold"), bd=0, activebackground="#121218", activeforeground="#C5A059", cursor="hand2", command=show_tab1)
        btn_tab1.place(x=0, y=0, width=220, height=42)

        btn_tab2 = Button(tab_bar, text="REGISTERED USERS", bg="#121218", fg="#626270", font=("Segoe UI", 11), bd=0, activebackground="#121218", activeforeground="#C5A059", cursor="hand2", command=show_tab2)
        btn_tab2.place(x=220, y=0, width=220, height=42)

        show_tab1()

        Label(tab1_frame, text="ACCOUNT CONTROL", font=("Segoe UI", 15, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=40, y=15)

        Label(tab1_frame, text="Username (Fixed)", font=("Segoe UI", 9, "bold"), fg="#626270", bg="#0B0B0E").place(x=40, y=65)
        lbl_username = Label(tab1_frame, text=self.username, font=("Segoe UI", 11, "bold"), fg="#8A8A93", bg="#14141A", anchor="w", padx=12, relief=FLAT)
        lbl_username.place(x=40, y=90, width=360, height=38)

        Label(tab1_frame, text="Current Email Address", font=("Segoe UI", 9, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=40, y=145)
        txt_email = Entry(tab1_frame, font=("Segoe UI", 11), bg="#14141A", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#22222E", highlightcolor="#C5A059")
        txt_email.place(x=40, y=170, width=360, height=38)
        txt_email.insert(0, email_str)

        Label(tab1_frame, text="New Password (leave blank to keep current)", font=("Segoe UI", 9, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=40, y=225)
        txt_new_password = Entry(tab1_frame, font=("Segoe UI", 11), bg="#14141A", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#22222E", highlightcolor="#C5A059", show="*")
        txt_new_password.place(x=40, y=250, width=360, height=38)

        Label(tab1_frame, text="Old Password (Required to authorize updates) *", font=("Segoe UI", 9, "bold"), fg="#FF4444", bg="#0B0B0E").place(x=40, y=305)
        txt_old_password = Entry(tab1_frame, font=("Segoe UI", 11), bg="#14141A", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0, highlightthickness=1, highlightbackground="#3A1C1C", highlightcolor="#FF4444", show="*")
        txt_old_password.place(x=40, y=330, width=360, height=38)

        Label(tab2_frame, text="SYSTEM DIRECTORY", font=("Segoe UI", 15, "bold"), fg="#C5A059", bg="#0B0B0E").place(x=20, y=15)

        list_wrapper = Frame(tab2_frame, bg="#0B0B0E")
        list_wrapper.place(x=20, y=60, width=400, height=460)

        canvas = Canvas(list_wrapper, bg="#0B0B0E", bd=0, highlightthickness=0, yscrollincrement=1)
        scrollable_frame = Frame(canvas, bg="#0B0B0E")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=390)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scroll_bar_width = 4
        scroll_thumb = canvas.create_rectangle(396, 0, 396 + scroll_bar_width, 0, fill="#252530", outline="")

        def update_custom_scrollbar(*args):
            if not canvas.winfo_exists():
                return
            try:
                v_start, v_end = canvas.yview()
                if v_start <= 0.0 and v_end >= 1.0:
                    canvas.coords(scroll_thumb, 0, 0, 0, 0)
                    return

                c_height = canvas.winfo_height()
                y_start = int(v_start * c_height)
                y_end = int(v_end * c_height)

                canvas.coords(scroll_thumb, 393, y_start, 393 + scroll_bar_width, y_end)
            except:
                pass

        canvas.configure(yscrollcommand=update_custom_scrollbar)
        list_wrapper.bind("<Configure>", lambda e: update_custom_scrollbar())

        def highlight_thumb(active=True):
            color = "#C5A059" if active else "#252530"
            canvas.itemconfig(scroll_thumb, fill=color)

        def _on_mousewheel(event):
            highlight_thumb(True)
            canvas.yview_scroll(int(-1 * (event.delta / 40)), "units")
            canvas.after(400, lambda: highlight_thumb(False))

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        def load_users_as_cards():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            try:
                conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT username, email FROM users")
                rows = cursor.fetchall()

                for row in rows:
                    u_name, u_email = row

                    card = Frame(scrollable_frame, bg="#14141A", bd=0, padx=14, pady=12)
                    card.pack(fill=X, pady=5, padx=(2, 12))

                    edge_indicator = Frame(card, bg="#C5A059", width=3)
                    edge_indicator.pack(side=LEFT, fill=Y, padx=(0, 10))

                    info_container = Frame(card, bg="#14141A")
                    info_container.pack(side=LEFT, fill=BOTH, expand=True)

                    lbl_u = Label(info_container, text=u_name, font=("Segoe UI", 11, "bold"), fg="#C5A059", bg="#14141A", anchor="w")
                    lbl_u.pack(fill=X)

                    lbl_e = Label(info_container, text=u_email, font=("Segoe UI", 9), fg="#8A8A93", bg="#14141A", anchor="w")
                    lbl_e.pack(fill=X, pady=(3, 0))

                cursor.close()
                conn.close()
            except Error as e:
                Label(scrollable_frame, text=f"Failed to sync users: {e}", fg="#FF4444", bg="#0B0B0E", font=("Segoe UI", 10)).pack(pady=20)

        load_users_as_cards()

        def verify_old_password(cursor):
            old_pass = txt_old_password.get().strip()
            if not old_pass:
                messagebox.showerror("Verification Error", "You must enter your old password to authorize this action!", parent=self.new_window)
                return False

            hashed_old = hashlib.sha256(old_pass.encode()).hexdigest()
            cursor.execute("SELECT password FROM users WHERE username = %s", (self.username,))
            res = cursor.fetchone()
            if res:
                if res[0] == hashed_old:
                    return True
                else:
                    messagebox.showerror("Verification Error", "The old password entered is incorrect. Please try again.", parent=self.new_window)
                    return False
            else:
                messagebox.showerror("Verification Error", "User record not found.", parent=self.new_window)
                return False

        def update_profile():
            new_email = txt_email.get().strip()
            new_pass = txt_new_password.get().strip()

            if not new_email:
                messagebox.showerror("Error", "Email field cannot be empty.", parent=self.new_window)
                return
            if "@" not in new_email or "." not in new_email:
                messagebox.showerror("Error", "Please enter a valid email address structure.", parent=self.new_window)
                return

            try:
                conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
                cursor = conn.cursor()

                if not verify_old_password(cursor):
                    cursor.close()
                    conn.close()
                    return

                if new_pass:
                    hashed_password = hashlib.sha256(new_pass.encode()).hexdigest()
                    query = "UPDATE users SET email = %s, password = %s WHERE username = %s"
                    cursor.execute(query, (new_email, hashed_password, self.username))
                else:
                    query = "UPDATE users SET email = %s WHERE username = %s"
                    cursor.execute(query, (new_email, self.username))

                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Profile details updated successfully!", parent=self.new_window)
                self.new_window.destroy()
            except Error as ex:
                messagebox.showerror("Database Error", f"Update failed: {str(ex)}", parent=self.new_window)

        def delete_profile():
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently delete your account?\nThis action cannot be undone and you will be logged out instantly.", parent=self.new_window)
            if confirm:
                try:
                    conn = mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pass, database=self.db_name)
                    cursor = conn.cursor()

                    if not verify_old_password(cursor):
                        cursor.close()
                        conn.close()
                        return

                    cursor.execute("DELETE FROM users WHERE username = %s", (self.username,))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    messagebox.showinfo("Deleted", "Your account has been deleted successfully.", parent=self.new_window)

                    self.new_window.destroy()
                    for widget in self.root.winfo_children():
                        widget.destroy()

                    from src.login import AdvancedLoginWin

                    app = AdvancedLoginWin(self.root)
                except Error as ex:
                    messagebox.showerror("System Error", f"Deletion failed: {str(ex)}", parent=self.new_window)

        btn_update = Button(tab1_frame, text="UPDATE PROFILE", font=("Segoe UI", 10, "bold"), bg="#C5A059", fg="#0B0B0E", activebackground="#A38144", activeforeground="#0B0B0E", bd=0, cursor="hand2", command=update_profile)
        btn_update.place(x=40, y=400, width=360, height=42)

        btn_delete = Button(tab1_frame, text="DELETE ACCOUNT PERMANENTLY", font=("Segoe UI", 10, "bold"), bg="#3A1C1C", fg="#FF4444", activebackground="#5A1C1C", activeforeground="#FF4444", bd=0, cursor="hand2", command=delete_profile)
        btn_delete.place(x=40, y=455, width=360, height=42)


# ========== Run The App ==========
if __name__ == "__main__":
    root = Tk()
    app = HotelManagementSystem(root, username="Admin")
    root.mainloop()
