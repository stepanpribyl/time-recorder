import tkinter as tk
from tkinter import ttk
import os
import json
from math import floor

class DynamicTableApp(tk.Tk):
    def __init__(self, headers, session_dir):
        super().__init__()
        self.title("Dynamic Table Viewer")
        self.geometry("600x400")
        self.configure(bg="#f0f2f5")
        
        self.session_dir = session_dir
        self.headers = headers
        self.data = {header: {} for header in self.headers}

        # Style for a cleaner look
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#dfe6e9")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.map("Treeview", background=[("selected", "#74b9ff")])

        ttk.Label(self, text="Select Week:", font=("Segoe UI", 12, "bold"), background="#f0f2f5").pack(pady=10)

        # Dropdown for keys in dict
        self.combo = ttk.Combobox(self, values=list(self.headers), state="readonly", font=("Segoe UI", 11))
        self.combo.pack(pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)

        # Treeview frame
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.tree = ttk.Treeview(frame, show="headings")
        self.tree.pack(expand=True, fill="both", side="left")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)
        # get tags
        self.tree.tag_configure("highlight", foreground="green")
        self.tree.tag_configure("fade", foreground="#9b9b9b")

        self.status = ttk.Label(
            self,
            text="Select a week to view data.",
            font=("Segoe UI", 10),
            background="#f0f2f5",
            foreground="#555"
        )
        self.status.pack(pady=(0, 10))

    def load_week(self, week_id):
        """
        import all data from last 5 weeks, names of weeks for dynamic import for the older weeks
        structure:
        "KW50": {
            {"date": "Mon 20-12-2025", "GEI": 5, "RTL": 10, "Rezie": 0},
            {"date": "Tue 21-12-2025", "GEI": 1, "RTL": 12, "Rezie": 1}
        }
        """
        # data = get_session_data()
        self.data[week_id] = []
        active_projects = []
        
        self.week_dir = os.path.join(self.session_dir, week_id)
        filenames = next(os.walk(self.week_dir))[2]
        
        # first round: get the overall list of used projects within this week
        for filename in filenames:
            with open(os.path.join(self.week_dir, filename), "r") as file:
                file_data = json.load(file)
                file.close()
            projects = [block["projectId"] for block in file_data["blocks"]]
            active_projects += projects
            
        print(f"All projects: {set(active_projects)}")
           
        # second round: fill data structure, compute for each project 
        for filename in filenames:
            with open(os.path.join(self.week_dir, filename), "r") as file:
                file_data = json.load(file)
                file.close()
                
            # LAYER 1 ----------------------------------------------------
            self.data[week_id].append({
                "date": filename[len("session")+4+1:].replace(".json", "")
            })
            for project_id in active_projects:
                # add all time slots within each project 
                self.data[week_id][-1][project_id] = round(sum([b["t_end"] - b["t_start"] for b in file_data["blocks"] if b["t_end"] != None and b["projectId"] == project_id])/3600, 2)
            
            # add a TOTAL column value for current day
            self.data[week_id][-1]["TOTAL"] = round(sum([b["t_end"] - b["t_start"] for b in file_data["blocks"] if b["t_end"] != None])/3600, 2)
            # print(self.data[week_id])
            
            # LAYER 2 ----------------------------------------------------
            self.data[week_id].append({
                "date": "",
            })
            
            for project_id in active_projects:
                # value from previous line:
                project_time = self.data[week_id][-2][project_id]
                general_time = self.data[week_id][-2]["general"]
                total_time = self.data[week_id][-2]["TOTAL"] - general_time
                
                if total_time + general_time > 0:
                    ratio = project_time / total_time
                else:
                    ratio = 0.5
                
                
                if project_time < 5/60 or project_id == "general":
                    target_time = 0
                elif project_time < 15/16:
                    target_time = 0.25
                else:
                    target_time = round(1/4 * round((project_time + ratio*general_time)*4, 0), 2)
                
                # add all time slots within each project 
                self.data[week_id][-1][project_id] = target_time
                
            # compute TOTAL column value for current day based on real one
            total_base = round(1/4 * floor(self.data[week_id][-2]["TOTAL"]*4), 2)
            total_temp = sum([item for key, item in self.data[week_id][-1].items() if item!=""])
            
            if total_base != total_temp:
                print(f"Trimming values to reach {total_base}")
                self.trim_values(week_id, total_base, total_temp)
            
            self.data[week_id][-1]["TOTAL"] = sum([item for key, item in self.data[week_id][-1].items() if item!=""])
            
        return
    
    def trim_values(self, week_id, total_base, total_temp):
        """
        total_base ... total value of actual times floored to 1/4s
        total_temp ... sum of single project values rounded to 1/4s
        
        This function aims to trim values such that these totals match.
        Method: Trim from the max to min values.
        """
        filtered_data = {k: v for k, v in self.data[week_id][-1].items() if k != "date" and k != "total"}
        sorted_values = {p_id: v for p_id, v in sorted(filtered_data.items(), key=lambda item: item[1])}
        print(sorted_values.keys())
        
        # init step and its direction
        step = 0.25
        if total_base < total_temp:
            step = -0.25
        
        non_zero_projects = {p_id: v for p_id, v in sorted_values.items() if v > 0}
        total_diff_quarters = int(abs((total_base - total_temp)/step))
        
        # if we have enough projects to iterate over
        if total_diff_quarters <= non_zero_projects:
            for i in range(total_diff_quarters):
                project_id = list(sorted_values.keys())[-1-i]
                self.data[week_id][-1][project_id] += step
        else:
            print("WARNING: Too few non-zero projects to process trimming.")
            
    
    def on_select(self, event):
        week_id = self.combo.get()
        if len(self.data[week_id]) == 0:
            self.load_week(week_id)
            
        rows = self.data.get(week_id, [])

        # Remove old columns and data
        self.tree.delete(*self.tree.get_children())
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0)

        # If empty, nothing to show
        if not rows:
            self.status.config(text=f"No data available for {week_id}.")
            self.tree["columns"] = ()
            return

        # Determine all columns dynamically
        columns = list(rows[0].keys())
        self.tree["columns"] = columns

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=max(100, len(col) * 10), anchor="center")

        # Insert data
        for i, entry in enumerate(rows):
            values = [entry.get(col, "") for col in columns]
            tags = len(columns)*[""]
            if i%2 == 1:
                tags = len(tags)*["fade"]
            self.tree.insert("", "end", values=values, tags=tags)

        self.status.config(text=f"Showing {len(rows)} records in {week_id}")

# ---------- Example Data ----------
data = {
    "HR": [
        {"name": "Alice", "salary": 55000, "age": 29},
        {"name": "Bob", "salary": 52000, "age": 31}
    ],
    "IT": [
        {"name": "Charlie", "salary": 70000, "project": "AI"},
        {"name": "Diana", "salary": 68000, "project": "Backend"}
    ],
    "Finance": [
        {"name": "Ethan", "salary": 60000},
        {"name": "Fiona", "salary": 62000}
    ]
}

# ---------- Run ----------
if __name__ == "__main__":
    app = DynamicTableApp(data)
    app.mainloop()
