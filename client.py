import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Server Configuration
SERVER_URL = "http://localhost:5000"

# Helper Function for API Calls
def api_call(endpoint, method='GET', data=None):
    url = f"{SERVER_URL}{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url, params=data)
        return response.json(), response.status_code
    except Exception as e:
        messagebox.showerror("Error", f"API Error: {e}")
        return None, 500

# Colors
BACKGROUND_COLOR = "#D4EBF8"
PRIMARY_COLOR = "#1F509A"
SECONDARY_COLOR = "#0A3981"
ACCENT_COLOR = "#E38E49"

# Registration Screen
def register_screen():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {"username": username, "password": password}
        response, status_code = api_call("/register", "POST", data)

        if status_code == 201:
            messagebox.showinfo("Success", response["message"])
            window.destroy()
            login_screen()
        else:
            messagebox.showerror("Error", response["message"])

    window = tk.Tk()
    window.title("Register")
    window.minsize(200, 500)
    window.configure(bg=BACKGROUND_COLOR)

    tk.Label(window, text="Register", font=("Arial", 16), bg=PRIMARY_COLOR, fg="white", padx=10, pady=5).pack(pady=10, fill=tk.X)
    tk.Label(window, text="Username:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Password:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    tk.Button(window, text="Register", command=register_user, bg=ACCENT_COLOR, fg="white").pack(pady=10)
    tk.Button(window, text="Login Instead", command=lambda: [window.destroy(), login_screen()], bg=PRIMARY_COLOR, fg="white").pack(pady=5)

    window.mainloop()

# Login Screen
def login_screen():
    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {"username": username, "password": password}
        response, status_code = api_call("/login", "POST", data)

        if status_code == 200:
            messagebox.showinfo("Success", response["message"])
            window.destroy()
            dashboard(response["user_id"])
        else:
            messagebox.showerror("Error", response["message"])

    window = tk.Tk()
    window.title("Login")
    window.minsize(200, 500)
    window.configure(bg=BACKGROUND_COLOR)

    tk.Label(window, text="Login", font=("Arial", 16), bg=PRIMARY_COLOR, fg="white", padx=10, pady=5).pack(pady=10, fill=tk.X)
    tk.Label(window, text="Username:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Password:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    tk.Button(window, text="Login", command=login_user, bg=ACCENT_COLOR, fg="white").pack(pady=10)
    tk.Button(window, text="Register Instead", command=lambda: [window.destroy(), register_screen()], bg=PRIMARY_COLOR, fg="white").pack(pady=5)

    window.mainloop()

# Dashboard
def dashboard(user_id):
    def register_file():
        file_name = file_name_entry.get()
        file_size = file_size_entry.get()
        file_type = file_type_entry.get()
        ip_address = ip_entry.get()
        port = port_entry.get()

        if not all([file_name, file_size, file_type, ip_address, port]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type,
            "shared_by": user_id,
            "ip_address": ip_address,
            "port": int(port),
        }
        response, status_code = api_call("/register_file", "POST", data)

        if status_code == 201:
            messagebox.showinfo("Success", response["message"])
        else:
            messagebox.showerror("Error", response["message"])

    def search_files():
        query = query_entry.get()
        file_type = search_type_entry.get()

        params = {"query": query, "type": file_type}
        response, status_code = api_call("/search", "GET", params)

        if status_code == 200:
            results_text.delete("1.0", tk.END)
            files = response.get("files", [])
            if not files:
                results_text.insert(tk.END, "No files found.\n")
            else:
                for file in files:
                    results_text.insert(tk.END, f"{file['file_name']} ({file['file_type']})\n")
        else:
            messagebox.showerror("Error", response["message"])

    window = tk.Tk()
    window.title("Dashboard")
    window.minsize(200, 500)
    window.configure(bg=BACKGROUND_COLOR)

    tk.Label(window, text="Dashboard", font=("Arial", 16), bg=PRIMARY_COLOR, fg="white", padx=10, pady=5).pack(pady=10, fill=tk.X)

    tk.Label(window, text="File Name:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    file_name_entry = tk.Entry(window)
    file_name_entry.pack(pady=5)

    tk.Label(window, text="File Size:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    file_size_entry = tk.Entry(window)
    file_size_entry.pack(pady=5)

    tk.Label(window, text="File Type:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    file_type_entry = tk.Entry(window)
    file_type_entry.pack(pady=5)

    tk.Label(window, text="IP Address:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    ip_entry = tk.Entry(window)
    ip_entry.pack(pady=5)

    tk.Label(window, text="Port:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    port_entry = tk.Entry(window)
    port_entry.pack(pady=5)

    tk.Button(window, text="Register File", command=register_file, bg=ACCENT_COLOR, fg="white").pack(pady=10)

    tk.Label(window, text="Search Query:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    query_entry = tk.Entry(window)
    query_entry.pack(pady=5)

    tk.Label(window, text="File Type:", bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR).pack(pady=5)
    search_type_entry = tk.Entry(window)
    search_type_entry.pack(pady=5)

    tk.Button(window, text="Search Files", command=search_files, bg=ACCENT_COLOR, fg="white").pack(pady=10)

    results_text = tk.Text(window, height=10, width=40, bg=BACKGROUND_COLOR, fg=SECONDARY_COLOR)
    results_text.pack(pady=10)

    window.mainloop()

# Start with the Login Screen
login_screen()
