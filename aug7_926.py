from tkinter import * 
from tkinter import filedialog 
from tkinter import ttk, messagebox
import sv_ttk
import subprocess 

# # Widgets: GUI Elements, like buttons, textboxes, images, or labels
# # Windows: Serve as containers to hold or contain these widgets 

def open_file():
    file_path = filedialog.askopenfilename()
    file = open(file_path, 'r')
    print(file.read())

def load_visitation(patient_id, x):
    pass

def run_subprocess(): 
    subprocess.run([
        "python",
        "rudimentary_script.py",
        "input.txt",
        "pred/MRN-002.json"
    ])
    load_output_file("pred/MRN-001.json")

def format_date_interval(date_str):
    MONTHS = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }

    if ".." not in date_str:
        year, month = date_str.split("-")
        return f"{MONTHS[month]} {year}"

    # Interval: "2019-12..2020-01"
    start, end = date_str.split("..")

    start_year, start_month = start.split("-")
    end_year, end_month = end.split("-")

    start_name = MONTHS[start_month]
    end_name = MONTHS[end_month]

    # Same year
    if start_year == end_year:
        return f"{start_name} to {end_name} {start_year}"

    # Different years
    return f"{start_name} {start_year} to {end_name} {end_year}"

class RecurrenceCard(ttk.Frame):
    def __init__(self, parent, patient_level_data):
        super().__init__(parent)

        self.configure(padding=10)

        # Title
        ttk.Label(
            self,
            text="Patient-Level Summary",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        ttk.Separator(self).pack(fill="x", pady=5)

        # Surgery date
        ttk.Label(
            self,
            text=f"First Surgery Date: {patient_level_data["first_surgery_date"]}"
        ).pack(anchor="w")

        # History summary
        ttk.Label(
            self,
            text="Prediction History Summary:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(10, 0))

        ttk.Label(
            self,
            text=patient_level_data["summary_patient_history"],
            wraplength=500,
            justify="left"
        ).pack(anchor="w")

        # Recurrence status
        ttk.Label(
            self,
            text=f"Has Recurrence: {patient_level_data["recurrence_prediction"]['has_recurrence']}"
        ).pack(anchor="w", pady=(10, 0))

        # Months
        ttk.Label(
            self,
            text="Recurrence Months:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        for month in patient_level_data["recurrence_prediction"]["recurrence_months"]:
            ttk.Label(
                self,
                text=f"• {month}"
            ).pack(anchor="w")

        # Regions
        ttk.Label(
            self,
            text="Regions:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(10, 0))

        for region in patient_level_data["recurrence_prediction"]["regions"]:
            ttk.Label(
                self,
                text=f"{region['month']}: {region['region']}",
                wraplength=500
            ).pack(anchor="w")

class PhaseCard(Frame):
    # Maps the recurrence code in the JSON to
    # (display text, display color)
    RECURRENCE_TYPES = {
        "REC": ("Recurrence", "#C93B1E"),
        "SUSP": ("Possible Recurrence", "#C9A11E"),
        "NOREC_PHASE": ("No Recurrence Found", "#9BC91E"),
    }

    def __init__(self, parent, data, patient_id):
        """
        Parameters
        ----------
        parent : tkinter widget

        data : dict
            {
                "date_or_interval": Any,
                "type": "REC" | "SUSP" | "NOREC_PHASE",
                "supporting_vis": list[str],
                "reasoning": str,
                "evidence_summary": str (optional),
                "why_not_single_month": str (optional)
            }

        patient_id : str
            Used when opening supporting visitations.
        """
        super().__init__(
            parent,
            relief="solid",
            bg="#f0f0f0",
            padx=5,
            pady=5
        )

        # header

        header = Frame(self, bg="#f0f0f0")
        header.pack(fill="x")

        Label(
            header,
            text="Date or Interval:",
            font=("Segoe UI", 14, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=0)

        Label(
            header,
            text=format_date_interval(data["date_or_interval"]),
            bg="#f0f0f0"
        ).grid(row=0, column=1)

        Label(
            header,
            text="; Recurrence:",
            font=("Segoe UI", 14, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=2)

        recurrence_text, recurrence_color = self.RECURRENCE_TYPES[data["type"]]

        Label(
            header,
            text=recurrence_text,
            font=("Segoe UI", 14),
            fg=recurrence_color,
            bg="#f0f0f0"
        ).grid(row=0, column=3)

        Label(
            header,
            text="; Visitations:",
            font=("Segoe UI", 14, "bold"),
            bg="#f0f0f0"
        ).grid(row=0, column=4)

        # button for each supporting visit

        for i, vis in enumerate(data["supporting_vis"]):
            ttk.Button(
                header,
                text=vis,
                command=lambda v=vis: load_visitation(patient_id, v)
            ).grid(row=0, column=5 + i)

        # reasoning

        Label(
            self,
            text=data.get("reasoning", ""),
            wraplength=900,
            justify="left",
            bg="#f0f0f0"
        ).pack(anchor="w", pady=(5, 0))

        # evidence summary

        if data.get("evidence_summary"):

            Label(
                self,
                text=f"Summary: {data['evidence_summary']}",
                wraplength=600,
                justify="left",
                bg="#f0f0f0"
            ).pack(anchor="w", pady=(5, 0))

        # why does it span multiple months?

        if data.get("why_not_single_month"):

            Label(
                self,
                text=f"Note: {data['why_not_single_month']}",
                wraplength=600,
                justify="left",
                foreground="#999999",
                bg="#f0f0f0"
            ).pack(anchor="w", pady=(5, 0))


window = Tk() # Creates a window 

sv_ttk.set_theme("light")


container = Frame(window)
container.pack(fill = "both", expand = True)

canvas = Canvas(container)
scrollbar = ttk.Scrollbar(
    container, 
    orient = "vertical", 
    command = canvas.yview 
)

frame = Frame(canvas)
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
canvas.create_window((0, 0), window = frame, anchor = "nw")
canvas.configure(yscrollcommand = scrollbar.set)
canvas.pack(side = "left", fill = "both", expand = True)

def _bind_mousewheel(event):
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

def _unbind_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")

TRUE_SCROLL = 0
SCREEN_SCROLL = 0

def _on_mousewheel(event):
    global TRUE_SCROLL, SCREEN_SCROLL

    TRUE_SCROLL -= event.delta / 3

    target_scroll = int(TRUE_SCROLL)

    if target_scroll != SCREEN_SCROLL:
        canvas.yview_scroll(
            target_scroll - SCREEN_SCROLL,
            "units"
        )
        SCREEN_SCROLL = target_scroll

canvas.bind("<Enter>", _bind_mousewheel)
canvas.bind("<Leave>", _unbind_mousewheel)
window.bind_all("<MouseWheel>", _on_mousewheel)

scrollbar.pack(side = "right", fill = "y")


label = Label(frame, text = "SCRIBE GUI Upload Tool for 08/07/26").grid(row = 0, column = 0, sticky = "w")

file_upload_button = ttk.Button(
    frame,
    text = "Load File",
    command = open_file).grid(row = 1, column = 0, sticky = "w")

sp_button = ttk.Button(
    frame, 
    text = "Run Arbitrary Subprocess",
    command = run_subprocess
).grid(row = 2, column = 0, sticky = "w")

import json 

def load_output_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        patient_data = json.load(file)
    pld = patient_data['output']
    RecurrenceCard(frame, pld).grid(row = 4, column = 0, sticky = "w", pady = 5)
    timeline = patient_data['output']['timeline']
    for i in range(len(timeline)):
        PhaseCard(frame, timeline[i], 0).grid(row = 5 + i, column = 0, sticky = "w", pady = 5)

window.title("SCRIBE GUI Upload Tool")
window.geometry("420x420")
window.config(background = "white")
window.mainloop() # Shows the window 

