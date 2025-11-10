import tkinter as tk
from tkinter import ttk
import json
import os

# ---------- JSON Setup ----------
def setup_json():
    """Create a demo JSON file if it doesn't exist."""
    data = {
        "kw10": [
            {"name": "Alice\nBrown", "salary": 55000},
            {"name": "Bob", "salary": 52000}
        ],
        "kw11": [
            {"name": "Charlie", "salary": 70000},
            {"name": "Diana", "salary": 68000}
        ],
        "kw12": [
            {"name": "Ethan", "salary": 60000},
            {"name": "Fiona", "salary": 62000}
        ]
    }
    if not os.path.exists("employees.json"):
        with open("employees.json", "w") as f:
            json.dump(data, f, indent=4)

def load_data():
    """Load all department data from JSON file."""
    with open("employees.json", "r") as f:
        return json.load(f)


class ResultBrowser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Company Employee Viewer (JSON Version)")
        self.geometry("520x400")
        self.configure(bg="#f0f2f5")

        self.data = load_data()
        departments = list(self.data.keys())

        # ---- Styling ----
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#dfe6e9")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        self.style.map("Treeview", background=[("selected", "#74b9ff")])

        ttk.Label(self, text="Select Department:", font=("Segoe UI", 12, "bold"), background="#f0f2f5").pack(pady=10)

        self.combo = ttk.Combobox(self, values=departments, state="readonly", font=("Segoe UI", 11))
        self.combo.pack(pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)

        self.tree = ttk.Treeview(self, columns=("Name", "Salary"), show="headings")
        self.tree.heading("Name", text="Employee Name")
        self.tree.heading("Salary", text="Salary ($)")
        self.tree.column("Name", width=220)
        self.tree.column("Salary", width=100, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=20, pady=20)

        self.status = ttk.Label(
            self,
            text="Select a department to view employees.",
            font=("Segoe UI", 10),
            background="#f0f2f5",
            foreground="#555"
        )
        self.status.pack(pady=(0, 10))

    def on_select(self, event):
        department = self.combo.get()
        rows = self.data.get(department, [])

        # Clear table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insert new data
        for emp in rows:
            self.tree.insert("", "end", values=(emp["name"], f"${emp['salary']:,}"))

        self.status.config(text=f"Showing {len(rows)} employees in {department}")
        
        
# if __name__ == "__main__":
    # setup_json()
    # app = ResultBrowser()
    # app.mainloop()