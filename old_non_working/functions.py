import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from old_non_working.SubScale import *
from IPython.display import display


# Function to handle file upload and process CSV
# Global variable for DataFrame
df_global = None

# Function to handle file upload and process CSV
def upload_file():
    global df_global  # Declare as global
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df_global = pd.read_csv(file_path)
        messagebox.showinfo("File Uploaded", f"File processed: {file_path}")
    else:
        messagebox.showwarning("No File", "No file was selected!")


# Function to process the survey CSV data (placeholder logic)
def process_survey(df):
    # Split the DataFrame into sections based on keywords
    keywords = [["Filler", "BAS", "BIS"]]
    scales = [["BIS_BAS"]] 
    split_section = split_dataframe_by_keywords(df, keywords)  # This is now a dictionary
    
    # Check if the number of split sections and scales match
    if len(split_section) != len(scales):
        print(f"Error: Mismatch between number of sections ({len(split_section)}) and scales ({len(scales)}).")
        return

    # Iterate over the keywords and use them to access the split_section dictionary
    for i in range(len(keywords)):
        # Join the keywords to create the corresponding key
        section_key = f"split_section_{'_'.join(keywords[i])}"
        
        # Retrieve the section DataFrame using the key
        section = split_section.get(section_key)
        scale = scales[i]
        
        # Check if section is a valid DataFrame
        if isinstance(section, pd.DataFrame) and not section.empty:
            process_subscale(section, scale)
        else:
            print(f"Error: Expected a non-empty DataFrame for section {i} with key {section_key}, but got {type(section)}.")




           
def make_UI():

    # Function for Everyone button
    def everyone_action():
        if df_global is not None:
            process_survey(df_global)
        else:
            messagebox.showwarning("No Data", "No data available! Please upload a file.")

    # Function for Individual button
    def individual_action():
        last_name = entry_last_name.get()
        if last_name:
            messagebox.showinfo("Action", f"Searching for: {last_name}")
        else:
            messagebox.showwarning("Input Error", "Please enter a last name!")

    # Initialize CustomTkinter
    ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # Options: "blue", "dark-blue", "green"

    # Create the root window
    root = ctk.CTk()
    root.title("Enhanced CustomTkinter UI")
    root.geometry("550x450")  # Set a specific window size
    root.grid_columnconfigure(0, weight=1)  # Center align elements

    # Styling variables
    button_style = {"corner_radius": 10, "font": ("Arial", 14)}
    label_style = {"font": ("Arial", 16)}
    entry_style = {"font": ("Arial", 14)}
    # Title Label
    title_label = ctk.CTkLabel(root, text="File Uploader & Search Interface", **label_style)
    title_label.pack(pady=20)

    # Upload File Section
    upload_btn = ctk.CTkButton(root, text="Upload File", command=upload_file, **button_style)
    upload_btn.pack(pady=10)

    # Separator
    separator = ctk.CTkLabel(root, text="----------------", **label_style)
    separator.pack(pady=10)

    # Buttons for Everyone and Individual Search
    everyone_btn = ctk.CTkButton(root, text="Everyone", command=everyone_action, **button_style)
    everyone_btn.pack(pady=10)

    # Search by Individual
    label_last_name = ctk.CTkLabel(root, text="Search by Last Name:", **label_style)
    label_last_name.pack(pady=10)

    entry_last_name = ctk.CTkEntry(root, width=300, **entry_style)
    entry_last_name.pack(pady=10)

    individual_btn = ctk.CTkButton(root, text="Individual", command=individual_action, **button_style)
    individual_btn.pack(pady=10)

    # Start the application
    root.mainloop()


