import customtkinter as ctk
from tkinter import ttk, messagebox
import database
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4
from PIL import Image, ImageDraw
import threading

database.create_tables()

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Color scheme
PRIMARY_COLOR = "#1e40af"
SECONDARY_COLOR = "#0f172a"
ACCENT_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"
DANGER_COLOR = "#ef4444"
WARNING_COLOR = "#f59e0b"
INFO_COLOR = "#06b6d4"
TEXT_COLOR = "#f8fafc"
HOVER_COLOR = "#1e3a8a"

# ================= ANIMATED LOGIN WINDOW ================= #
def open_login():
    login_win = ctk.CTk()
    login_win.title("EduTrack Login")
    login_win.geometry("500x600")
    login_win.resizable(False, False)
    
    # Add corner radius
    login_win.grid_rowconfigure(0, weight=1)
    login_win.grid_columnconfigure(0, weight=1)
    
    # Main frame
    main_frame = ctk.CTkFrame(login_win, fg_color=SECONDARY_COLOR, corner_radius=15)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Header section
    header_frame = ctk.CTkFrame(main_frame, fg_color=PRIMARY_COLOR, corner_radius=15)
    header_frame.pack(fill="x", padx=20, pady=(20, 40))
    
    title_label = ctk.CTkLabel(
        header_frame, 
        text="EduTrack", 
        font=("Helvetica", 36, "bold"),
        text_color=TEXT_COLOR
    )
    title_label.pack(pady=15)
    
    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Student Score Management System",
        font=("Helvetica", 12),
        text_color="#e0e7ff"
    )
    subtitle_label.pack(pady=(0, 15))
    
    # Form frame
    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.pack(padx=40, pady=20, fill="both", expand=True)
    
    # Username
    user_label = ctk.CTkLabel(
        form_frame,
        text="Username",
        font=("Helvetica", 12, "bold"),
        text_color=TEXT_COLOR
    )
    user_label.pack(anchor="w", pady=(0, 8))
    
    user_entry = ctk.CTkEntry(
        form_frame,
        placeholder_text="Enter username",
        width=300,
        height=40,
        corner_radius=8,
        font=("Helvetica", 12),
        fg_color="#1e293b",
        border_color=ACCENT_COLOR,
        border_width=2
    )
    user_entry.pack(pady=(0, 20))
    
    # Password
    pwd_label = ctk.CTkLabel(
        form_frame,
        text="Password",
        font=("Helvetica", 12, "bold"),
        text_color=TEXT_COLOR
    )
    pwd_label.pack(anchor="w", pady=(0, 8))
    
    pwd_entry = ctk.CTkEntry(
        form_frame,
        placeholder_text="Enter password",
        width=300,
        height=40,
        corner_radius=8,
        font=("Helvetica", 12),
        fg_color="#1e293b",
        border_color=ACCENT_COLOR,
        border_width=2,
        show="•"
    )
    pwd_entry.pack(pady=(0, 30))
    
    # Info text
    info_label = ctk.CTkLabel(
        form_frame,
        text="Demo Credentials:\nUsername: admin | Password: admin123\nUsername: teacher | Password: teach123",
        font=("Helvetica", 10),
        text_color="#94a3b8",
        justify="left"
    )
    info_label.pack(pady=(0, 20))
    
    def animate_login_button(button):
        button.configure(fg_color=HOVER_COLOR, text_color="#e0e7ff")
    
    def reset_login_button(button):
        button.configure(fg_color=PRIMARY_COLOR, text_color=TEXT_COLOR)
    
    def login():
        user = user_entry.get()
        pwd = pwd_entry.get()
        
        if not user or not pwd:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        role = database.check_login(user, pwd)
        if role:
            login_win.destroy()
            open_dashboard(role[0])
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")
            pwd_entry.delete(0, "end")
    
    login_button = ctk.CTkButton(
        form_frame,
        text="Login",
        width=300,
        height=45,
        corner_radius=10,
        font=("Helvetica", 14, "bold"),
        fg_color=PRIMARY_COLOR,
        text_color=TEXT_COLOR,
        hover_color=HOVER_COLOR,
        command=login
    )
    login_button.pack(pady=10)
    
    login_button.bind("<Enter>", lambda e: animate_login_button(login_button))
    login_button.bind("<Leave>", lambda e: reset_login_button(login_button))
    
    # Bind Enter key to login
    pwd_entry.bind("<Return>", lambda e: login())
    
    login_win.mainloop()


# ================= ANIMATED DASHBOARD ================= #
def open_dashboard(role):
    root = ctk.CTk()
    root.title("EduTrack Dashboard")
    root.geometry("1600x850")
    root.resizable(True, True)
    
    # Configure grid
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Header/Navigation bar
    nav_frame = ctk.CTkFrame(root, fg_color=PRIMARY_COLOR, height=70, corner_radius=0)
    nav_frame.grid(row=0, column=0, sticky="ew")
    nav_frame.grid_rowconfigure(0, weight=1)
    nav_frame.grid_columnconfigure(0, weight=1)
    
    nav_content = ctk.CTkFrame(nav_frame, fg_color="transparent")
    nav_content.grid(row=0, column=0, sticky="ew", padx=25, pady=12)
    nav_content.grid_columnconfigure(0, weight=1)
    
    # Title and role indicator
    title_frame = ctk.CTkFrame(nav_content, fg_color="transparent")
    title_frame.grid(row=0, column=0, sticky="w")
    
    title_label = ctk.CTkLabel(
        title_frame,
        text="📚 EduTrack",
        font=("Helvetica", 24, "bold"),
        text_color=TEXT_COLOR
    )
    title_label.pack(side="left", padx=10)
    
    role_badge = ctk.CTkFrame(
        title_frame,
        fg_color="#0ea5e9",
        corner_radius=6,
        height=30
    )
    role_badge.pack(side="left", padx=10)
    
    role_label = ctk.CTkLabel(
        role_badge,
        text=f"🔐 {role}",
        font=("Helvetica", 11, "bold"),
        text_color=TEXT_COLOR
    )
    role_label.pack(padx=12, pady=5)
    
    # Logout button
    def logout():
        root.destroy()
        open_login()
    
    logout_button = ctk.CTkButton(
        nav_content,
        text="↪ Logout",
        width=100,
        height=40,
        corner_radius=8,
        font=("Helvetica", 11, "bold"),
        fg_color=DANGER_COLOR,
        hover_color="#dc2626",
        command=logout
    )
    logout_button.grid(row=0, column=1, sticky="e")
    
    # Main content frame
    main_frame = ctk.CTkFrame(root, fg_color=SECONDARY_COLOR)
    main_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=0)
    main_frame.grid_columnconfigure(1, weight=1)
    
    # Left panel - Form
    left_panel = ctk.CTkFrame(main_frame, fg_color="#1e293b", corner_radius=12, width=280)
    left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=0)
    left_panel.grid_propagate(False)
    
    form_title = ctk.CTkLabel(
        left_panel,
        text="Add Student",
        font=("Helvetica", 14, "bold"),
        text_color=TEXT_COLOR
    )
    form_title.pack(padx=15, pady=(15, 15))
    
    # Input fields
    fields_data = [
        ("Roll No", "roll_entry"),
        ("Name", "name_entry"),
        ("Subject 1", "sub1_entry"),
        ("Subject 2", "sub2_entry"),
        ("Subject 3", "sub3_entry")
    ]
    
    entries = {}
    
    for idx, (label_text, var_name) in enumerate(fields_data):
        label = ctk.CTkLabel(
            left_panel,
            text=label_text,
            font=("Helvetica", 10, "bold"),
            text_color="#cbd5e1"
        )
        label.pack(anchor="w", padx=15, pady=(6, 2))
        
        entry = ctk.CTkEntry(
            left_panel,
            placeholder_text=f"Enter {label_text.lower()}",
            width=230,
            height=32,
            corner_radius=5,
            font=("Helvetica", 10),
            fg_color="#0f172a",
            border_color=ACCENT_COLOR,
            border_width=1
        )
        entry.pack(padx=15, pady=(0, 3))
        entries[var_name] = entry
    
    def grade(p):
        if p >= 90: return "A+"
        elif p >= 75: return "A"
        elif p >= 60: return "B"
        elif p >= 40: return "C"
        else: return "Fail"
    
    def add_student():
        try:
            r = int(entries['roll_entry'].get())
            n = entries['name_entry'].get()
            s1 = int(entries['sub1_entry'].get())
            s2 = int(entries['sub2_entry'].get())
            s3 = int(entries['sub3_entry'].get())
            
            if not n:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            total = s1 + s2 + s3
            per = total / 3
            g = grade(per)
            
            # show spinner in a thread to avoid freeze
            threading.Thread(target=lambda: database.insert_student((r, n, s1, s2, s3, total, per, g))).start()
            
            # Clear entries
            for entry in entries.values():
                entry.delete(0, "end")
            
            load_data()
            messagebox.showinfo("Success", "Student added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def delete_data():
        if role != "Admin":
            messagebox.showwarning("Permission Denied", "Only Admin can delete records")
            return
        
        selected = table.focus()
        if selected:
            roll_no = table.item(selected)['values'][0]
            database.delete_student(roll_no)
            load_data()
            messagebox.showinfo("Success", "Student deleted successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a student to delete")
    
    def export_pdf():
        try:
            data = database.fetch_students()
            if not data:
                messagebox.showwarning("Warning", "No student data to export")
                return
            pdf = SimpleDocTemplate("Student_Results.pdf", pagesize=A4)
            table_data = [["Roll", "Name", "S1", "S2", "S3", "Total", "%", "Grade"]] + [list(d) for d in data]
            pdf.build([Table(table_data)])
            messagebox.showinfo("Success", "PDF Exported Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting PDF: {str(e)}")
    
    def show_chart():
        data = database.fetch_students()
        if not data:
            messagebox.showwarning("Warning", "No student data to display")
            return
        names = [d[1] for d in data]
        perc = [d[6] for d in data]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(names, perc, color='#3b82f6', edgecolor='#1e40af', linewidth=1.5)
        plt.ylabel("Percentage", fontsize=12, fontweight='bold')
        plt.title("Student Performance Analysis", fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, 100)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    # Button frame
    button_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    button_frame.pack(padx=15, pady=(12, 15), fill="x")
    
    buttons_data = [
        ("Add Student", SUCCESS_COLOR, "#047857", add_student),
        ("Delete Student", DANGER_COLOR, "#991b1b", delete_data),
        ("Export PDF", ACCENT_COLOR, HOVER_COLOR, export_pdf),
        ("Show Chart", WARNING_COLOR, "#92400e", show_chart)
    ]
    
    for btn_text, fg_color, hover_color, cmd in buttons_data:
        btn = ctk.CTkButton(
            button_frame,
            text=btn_text,
            width=230,
            height=32,
            corner_radius=5,
            font=("Helvetica", 10, "bold"),
            fg_color=fg_color,
            hover_color=hover_color,
            command=cmd
        )
        btn.pack(pady=3)
    
    # Right panel - Table
    right_panel = ctk.CTkFrame(main_frame, fg_color="#1e293b", corner_radius=12)
    right_panel.grid(row=0, column=1, sticky="nsew")
    right_panel.grid_rowconfigure(1, weight=1)
    right_panel.grid_columnconfigure(0, weight=1)
    
    table_title = ctk.CTkLabel(
        right_panel,
        text="Student Records",
        font=("Helvetica", 14, "bold"),
        text_color=TEXT_COLOR
    )
    table_title.grid(row=0, column=0, padx=15, pady=(15, 12), sticky="w")
    
    # Table frame with scrollbar
    table_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
    table_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    # Configure treeview style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview",
                    background="#0f172a",
                    foreground=TEXT_COLOR,
                    rowheight=30,
                    fieldbackground="#0f172a",
                    borderwidth=0)
    style.map('Treeview',
              background=[('selected', PRIMARY_COLOR)],
              foreground=[('selected', TEXT_COLOR)])
    style.configure("Treeview.Heading",
                    background=PRIMARY_COLOR,
                    foreground=TEXT_COLOR,
                    borderwidth=0)
    style.map("Treeview.Heading",
              background=[('active', HOVER_COLOR)])
    
    cols = ("Roll", "Name", "S1", "S2", "S3", "Total", "%", "Grade")
    table = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
    
    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscroll=scrollbar.set)
    
    table.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    def load_data():
        for i in table.get_children():
            table.delete(i)
        for row in database.fetch_students():
            table.insert("", "end", values=row, tags=("oddrow",))
    
    load_data()
    
    root.mainloop()


# ================= START APP ================= #
open_login()
