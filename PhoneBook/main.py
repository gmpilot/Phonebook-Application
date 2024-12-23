import csv
import os
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Define paths and color scheme
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "phonebook.csv")

primary_color = "#007BFF"
header_color = "#222831"
button_color = "#00ADB5"
border_color = "#393E46"
error_color = "#E74C3C"
success_color = "#1ABC9C"


# Create the CSV file if it doesn't exist
def create_csv():
    try:
        with open(csv_file, mode="r", newline="") as file:
            pass
    except FileNotFoundError:
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Gender", "Area"])


create_csv()


# File operations
def read_data():
    with open(csv_file, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [row for row in reader]


def write_data(data):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Gender", "Area"])
        writer.writerows(data)


# Phonebook operations
def add_data(data):
    phonebook = read_data()
    if any(contact[1] == data[1] for contact in phonebook):
        messagebox.showwarning("Duplicate Contact", "This phone number already exists.")
        return
    phonebook.append(data)
    write_data(phonebook)


def update_data(updated_data):
    phonebook = read_data()
    for i, contact in enumerate(phonebook):
        if contact[1] == updated_data[1]:
            phonebook[i] = updated_data
            break
    write_data(phonebook)


def delete_data(phone):
    phonebook = [contact for contact in read_data() if contact[1] != phone]
    write_data(phonebook)


def search_data(name="", gender="", phone="", area=""):
    return [
        row
        for row in read_data()
        if (name.lower() in row[0].lower() or not name)
        and (gender.lower() == row[2].lower() or not gender)
        and (phone in row[1] or not phone)
        and (area.lower() in row[3].lower() or not area)
    ]


# Visualization
def plot_visualizations():
    area_input = entry_area.get()
    if not area_input:
        messagebox.showwarning("Input Error", "Please provide an area.")
        return

    data = read_data()
    female_count = sum(
        1
        for row in data
        if row[2].lower() == "female" and area_input.lower() in row[3].lower()
    )
    male_count = sum(
        1
        for row in data
        if row[2].lower() == "male" and area_input.lower() in row[3].lower()
    )
    total_count = female_count + male_count

    if total_count == 0:
        messagebox.showinfo("No Data", "No contacts found in the specified area.")
        return

    percentages = [female_count / total_count * 100, male_count / total_count * 100]
    plt.bar(["Female", "Male"], percentages, color=[button_color, "#F4B6C2"])
    plt.title(f"Gender Distribution in {area_input}")
    plt.ylim(0, 100)
    plt.ylabel("Percentage")
    plt.show()


# UI operations
def show_data():
    for widget in frame_table.winfo_children():
        widget.destroy()

    columns = ["Name", "Phone", "Gender", "Area"]
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
    for row in read_data():
        tree.insert("", "end", values=row)


def add_contact():
    name = entry_name.get()
    gender = (
        "Female" if gender_female_var.get() else "Male" if gender_male_var.get() else ""
    )
    phone = entry_phone.get()
    area = entry_area.get()

    if not all([name, gender, phone, area]):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    add_data([name, phone, gender, area])
    show_data()
    messagebox.showinfo("Success", "Contact added successfully.")
    entry_name.delete(0, END)
    entry_phone.delete(0, END)
    entry_area.delete(0, END)
    gender_female_var.set(False)
    gender_male_var.set(False)


def update_contact():
    name = entry_name.get()
    gender = (
        "Female" if gender_female_var.get() else "Male" if gender_male_var.get() else ""
    )
    phone = entry_phone.get()
    area = entry_area.get()

    if not all([name, gender, phone, area]):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    update_data([name, phone, gender, area])
    show_data()
    messagebox.showinfo("Success", "Contact updated successfully.")


def delete_contact():
    phone = entry_phone.get()
    if not phone:
        messagebox.showwarning("Input Error", "Phone number is required.")
        return

    delete_data(phone)
    show_data()
    messagebox.showinfo("Success", "Contact deleted successfully.")


def search_contact():
    name = entry_name.get()
    gender = (
        "Female" if gender_female_var.get() else "Male" if gender_male_var.get() else ""
    )
    phone = entry_phone.get()
    area = entry_area.get()

    results = search_data(name, gender, phone, area)
    for widget in frame_table.winfo_children():
        widget.destroy()

    columns = ["Name", "Phone", "Gender", "Area"]
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
    for row in results:
        tree.insert("", "end", values=row)


# Main Window Setup
window = Tk()
window.title("Phonebook")
window.geometry("700x700")
window.configure(bg=primary_color)

frame_title = Frame(window, bg=header_color)
frame_title.pack(fill="x")
Label(
    frame_title,
    text="Phonebook Application",
    font=("Arial", 18, "bold"),
    bg=header_color,
    fg="#FFFFFF",
).pack(pady=10)

frame_input = Frame(window, bg=primary_color)
frame_input.pack(fill="x", padx=10)

Label(frame_input, text="Name", bg=primary_color, font=("Arial", 12), fg="#fff").grid(
    row=0, column=0, pady=5
)
entry_name = Entry(frame_input, font=("Arial", 12), width=25)
entry_name.grid(row=0, column=1, pady=5)

Label(frame_input, text="Gender", bg=primary_color, font=("Arial", 12), fg="#fff").grid(
    row=1, column=0, pady=5
)
gender_female_var = BooleanVar()
gender_male_var = BooleanVar()
Checkbutton(
    frame_input,
    text="Female",
    variable=gender_female_var,
    bg=primary_color,
    font=("Arial", 12),
    fg="#fff",
).grid(row=1, column=1)
Checkbutton(
    frame_input,
    text="Male",
    variable=gender_male_var,
    bg=primary_color,
    font=("Arial", 12),
    fg="#fff",
).grid(row=1, column=2)

Label(frame_input, text="Phone", bg=primary_color, font=("Arial", 12), fg="#fff").grid(
    row=2, column=0, pady=5
)
entry_phone = Entry(frame_input, font=("Arial", 12), width=25)
entry_phone.grid(row=2, column=1, pady=5)

Label(frame_input, text="Area", bg=primary_color, font=("Arial", 12), fg="#fff").grid(
    row=3, column=0, pady=5
)
entry_area = Entry(frame_input, font=("Arial", 12), width=25)
entry_area.grid(row=3, column=1, pady=5)

frame_buttons = Frame(window, bg=primary_color)
frame_buttons.pack(fill="x", padx=10, pady=10)

Button(
    frame_buttons,
    text="Add",
    bg=success_color,
    fg=primary_color,
    font=("Arial", 12),
    command=add_contact,
).grid(row=0, column=0, padx=5)
Button(
    frame_buttons,
    text="Update",
    bg=button_color,
    fg=primary_color,
    font=("Arial", 12),
    command=update_contact,
).grid(row=0, column=1, padx=5)
Button(
    frame_buttons,
    text="Delete",
    bg=error_color,
    fg=primary_color,
    font=("Arial", 12),
    command=delete_contact,
).grid(row=0, column=2, padx=5)
Button(
    frame_buttons,
    text="Search",
    bg=button_color,
    fg=primary_color,
    font=("Arial", 12),
    command=search_contact,
).grid(row=0, column=3, padx=5)
Button(
    frame_buttons,
    text="Visualize",
    bg=success_color,
    fg=primary_color,
    font=("Arial", 12),
    command=plot_visualizations,
).grid(row=0, column=4, padx=5)

frame_table = Frame(window)
frame_table.pack(fill="both", padx=10, pady=10, expand=True)

show_data()
window.mainloop()
