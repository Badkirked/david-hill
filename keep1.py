import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import re

# Constants for file paths
CONFIG_FILE = "form_config.json"
STORED_OPTIONS_FILE = "stored_options.json"

# Function to load JSON data
def load_json_file(filepath, default=None):
    if not os.path.exists(filepath):
        return default
    with open(filepath, 'r') as file:
        return json.load(file)

# Function to save JSON data
def save_json_file(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def alphanumeric_sort(data):
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(data, key=alphanum_key)

# Load configuration and stored options
form_config = load_json_file(CONFIG_FILE)
stored_options = load_json_file(STORED_OPTIONS_FILE, default={
    "locations": ["OUTSIDE", "INSIDE", "11"],
    "brands": ["ABC", "CDE", "FFS", "WTF"],
    "bays": list(map(str, range(1, 51))),
    "rack_dimensions": ["100x200", "300x400", "500x600"],
    "rack_numbers": alphanumeric_sort(list(map(str, range(1, 51)))),
    "columns": ["Column1", "Column2", "Column3"],
    "arms": ["Arm1", "Arm2", "Arm3"],
    "bracings": ["Bracing1", "Bracing2", "Bracing3"]
})

submitted_rack_numbers = set()  # Set to keep track of submitted rack numbers

def collect_data(widgets, color_widgets):
    data = {}
    for field, widget in widgets.items():
        data[field] = widget.get() if isinstance(widget, (tk.StringVar, tk.Entry, ttk.Combobox)) else None
    for field, widget in color_widgets.items():
        data[f"{field} Color"] = widget.get()
    return data

def save_to_json(data, filename, client_info, form_config, client_info_saved):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            json_data = json.load(file)
    else:
        json_data = []

    if not client_info_saved:
        json_data.append(client_info)
        client_info_saved = True

    json_data.append(data)

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)

    return client_info_saved

def start_rack_form(welcome_root, entries):
    client_info = {label: entry.get() for label, entry in entries.items()}
    if not all(client_info.values()):
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    welcome_root.destroy()
    main_form(client_info)

def add_new_item(entry, combo, category):
    new_item = entry.get().strip()
    if new_item and new_item not in stored_options[category]:
        stored_options[category].append(new_item)
        stored_options[category] = alphanumeric_sort(stored_options[category])
        save_json_file(STORED_OPTIONS_FILE, stored_options)
        combo['values'] = stored_options[category]
        entry.delete(0, tk.END)

def create_colored_combobox(parent, options, field, widgets, row, column):
    def on_select(value, var):
        var.set(value)
        menu_btn.config(text=value, foreground=color_option_styles[value]["foreground"])

    var = tk.StringVar(value=options[0])
    menu_btn = tk.Menubutton(parent, text=options[0], indicatoron=True, borderwidth=1, relief="raised", foreground="red" if options[0] == "Red" else "black")
    menu = tk.Menu(menu_btn, tearoff=False)
    menu_btn.configure(menu=menu)

    color_option_styles = {
        "Red": {"foreground": "red"},
        "Amber": {"foreground": "orange"},
        "Green": {"foreground": "green"}
    }

    for option in options:
        menu.add_command(label=option, foreground=color_option_styles[option]["foreground"], command=lambda opt=option: on_select(opt, var))

    menu_btn.grid(row=row, column=column, padx=5, sticky=tk.W)
    widgets[field] = var

def main_form(client_info):
    global root, client_info_saved
    client_info_saved = False  # Initialize the variable here

    root = tk.Tk()
    root.title("Data Collection Form")
    root.configure(padx=20, pady=20)
    widgets = {}
    color_widgets = {}

    field_order = [
        "Rack Number", "Location", "Bay", "Rack Brand", "Rack Dimensions", "Column", "Arm", "Bracing",
        "Pin", "Clip", "Dyna Bolt", "Base", "Guide Rail", "SWL Chart",
        "Damaged", "Missing", "Comments"
    ]

    color_options = ["Red", "Amber", "Green"]

    for i, field in enumerate(field_order):
        tk.Label(root, text=f"{field}:").grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
        if field == "Rack Number":
            rack_number_combo = ttk.Combobox(root, values=stored_options["rack_numbers"], state='readonly')
            rack_number_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Rack Number"] = rack_number_combo

            new_rack_number_entry = tk.Entry(root)
            new_rack_number_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Rack Number", command=lambda: add_new_item(new_rack_number_entry, rack_number_combo, "rack_numbers")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Location":
            location_combo = ttk.Combobox(root, values=stored_options["locations"], state='readonly')
            location_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Location"] = location_combo

            new_location_entry = tk.Entry(root)
            new_location_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Location", command=lambda: add_new_item(new_location_entry, location_combo, "locations")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Bay":
            bay_combo = ttk.Combobox(root, values=stored_options["bays"], state='readonly')
            bay_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Bay"] = bay_combo

            new_bay_entry = tk.Entry(root)
            new_bay_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Bay", command=lambda: add_new_item(new_bay_entry, bay_combo, "bays")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Rack Brand":
            brand_combo = ttk.Combobox(root, values=stored_options["brands"], state='readonly')
            brand_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Rack Brand"] = brand_combo

            new_brand_entry = tk.Entry(root)
            new_brand_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Brand", command=lambda: add_new_item(new_brand_entry, brand_combo, "brands")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Rack Dimensions":
            rack_dimensions_combo = ttk.Combobox(root, values=stored_options["rack_dimensions"], state='readonly')
            rack_dimensions_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Rack Dimensions"] = rack_dimensions_combo

            new_rack_dimensions_entry = tk.Entry(root)
            new_rack_dimensions_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Rack Dimensions", command=lambda: add_new_item(new_rack_dimensions_entry, rack_dimensions_combo, "rack_dimensions")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Column":
            column_combo = ttk.Combobox(root, values=stored_options["columns"], state='readonly')
            column_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Column"] = column_combo

            new_column_entry = tk.Entry(root)
            new_column_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Column", command=lambda: add_new_item(new_column_entry, column_combo, "columns")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Arm":
            arm_combo = ttk.Combobox(root, values=stored_options["arms"], state='readonly')
            arm_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Arm"] = arm_combo

            new_arm_entry = tk.Entry(root)
            new_arm_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Arm", command=lambda: add_new_item(new_arm_entry, arm_combo, "arms")).grid(row=i, column=3, sticky=tk.W, padx=5)

        elif field == "Bracing":
            bracing_combo = ttk.Combobox(root, values=stored_options["bracings"], state='readonly')
            bracing_combo.grid(row=i, column=1, sticky=tk.W, padx=5)
            widgets["Bracing"] = bracing_combo

            new_bracing_entry = tk.Entry(root)
            new_bracing_entry.grid(row=i, column=2, sticky=tk.W, padx=5)
            tk.Button(root, text="Add Bracing", command=lambda: add_new_item(new_bracing_entry, bracing_combo, "bracings")).grid(row=i, column=3, sticky=tk.W, padx=5)

        else:
            question = next((q for q in form_config["questions"] if q["field"] == field), None)
            if not question:
                continue

            label = tk.Label(root, text=question["question"])
            label.grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)

            options = question["options"] or stored_options.get(field.lower() + "s", [])

            if options:
                if field in ["Pin", "Clip", "Dyna Bolt", "Base", "Guide Rail", "SWL Chart", "Missing", "Damaged"]:
                    var = tk.StringVar(value="yes")
                    tk.Radiobutton(root, text="Yes", variable=var, value="yes").grid(row=i, column=1, padx=5, sticky=tk.W)
                    tk.Radiobutton(root, text="No", variable=var, value="no").grid(row=i, column=2, padx=5, sticky=tk.W)
                    widgets[field] = var
                    create_colored_combobox(root, color_options, field, color_widgets, i, 3)
                else:
                    combo = ttk.Combobox(root, values=options, state='readonly')
                    combo.current(0)
                    combo.grid(row=i, column=1, sticky=tk.W, padx=5)
                    widgets[field] = combo
                    if question.get("custom_entry", False):
                        entry = tk.Entry(root)
                        entry.grid(row=i, column=2, sticky=tk.W, padx=5)
                        widgets[f"{field} Custom"] = entry
            else:
                entry = tk.Entry(root)
                entry.grid(row=i, column=1, columnspan=2, sticky=tk.W + tk.E, padx=5)
                widgets[field] = entry

    tk.Button(root, text="Submit", command=lambda: submit(root, widgets, color_widgets, client_info)).grid(row=len(field_order), column=0, pady=10)
    tk.Button(root, text="Finish", command=lambda: finish(root, widgets, color_widgets, client_info)).grid(row=len(field_order), column=1, pady=10)
    root.mainloop()

def welcome_form():
    welcome_root = tk.Tk()
    welcome_root.title("Welcome to Data Collection")
    welcome_root.configure(padx=20, pady=20)

    entries = {}
    labels = ["Client Name", "Client Address", "Audit No", "Customer", "Site Address", "Contact", "Date of Inspection", "Description"]
    for i, label_text in enumerate(labels):
        tk.Label(welcome_root, text=f"{label_text}: ").grid(row=i, column=0, sticky=tk.W)
        entry = tk.Entry(welcome_root)
        if label_text == "Date of Inspection":
            entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        entry.grid(row=i, column=1, sticky=tk.W + tk.E, pady=5)
        entries[label_text] = entry

    tk.Button(welcome_root, text="Submit", command=lambda: start_rack_form(welcome_root, entries)).grid(row=len(labels), column=0, columnspan=2, pady=10)
    welcome_root.mainloop()

def all_fields_filled(widgets, color_widgets):
    excluded_fields = {"Add Rack Number", "Add Location", "Add Bay", "Add Brand", "Add Rack Dimensions", "Add Column", "Add Arm", "Add Bracing", "Comments"}
    for field, widget in widgets.items():
        if field not in excluded_fields:
            if isinstance(widget, tk.StringVar) and not widget.get():
                return False
            if isinstance(widget, ttk.Combobox) and not widget.get():
                return False
            if isinstance(widget, tk.Entry) and not widget.get():
                return False
    for field, widget in color_widgets.items():
        if field not in excluded_fields:
            if not widget.get():
                return False
    return True

def submit(root, widgets, color_widgets, client_info):
    global client_info_saved
    if not all_fields_filled(widgets, color_widgets):
        messagebox.showerror("Error", "Please fill in all fields before submitting.")
        return
    data = collect_data(widgets, color_widgets)
    rack_number = data.get("Rack Number")
    
    if rack_number in submitted_rack_numbers:
        messagebox.showerror("Error", f"Rack Number {rack_number} has already been submitted.")
        return

    submitted_rack_numbers.add(rack_number)
    client_info_saved = save_to_json(data, f"{client_info['Client Name']}.json", client_info, form_config, client_info_saved)
    root.destroy()  # Destroy the current form
    main_form(client_info)  # Reopen the form with the same client_info

def finish(root, widgets, color_widgets, client_info):
    if not all_fields_filled(widgets, color_widgets):
        messagebox.showerror("Error", "Please fill in all fields before finishing.")
        return
    data = collect_data(widgets, color_widgets)
    save_to_json(data, f"{client_info['Client Name']}.json", client_info, form_config, client_info_saved=True)
    messagebox.showinfo("Information", "Final record saved. Exiting application.")
    root.destroy()

welcome_form()
