import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from IPython.display import display

#Testing ---
master_score = pd.DataFrame()

# Master Key
master_key = {
    "BIS_BAS": [
        ["Filler", "BAS", "BIS"],  # Keywords
        "BIS_BAS",                 # Scale name
        {                           # Response map
            "Very True for Me": 1,
            "Somewhat True": 2,
            "Somewhat False": 3,
            "Very False for Me": 4
        },
        ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)',  # Reverse columns
         'BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)',
         'BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)',
         'BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)'],
        {                           # Sections with their items
            "BAS_Drive": ['BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)'],
            "BAS_Fun_Seeking": ['BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)'],
            "BAS_Reward_Responsiveness": ['BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)'],
            "BIS": ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)', 'BIS_2', 'BIS_22']
        }
    ]
}

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

# Function to map text responses to numerical scores
def map_response_to_score(response, response_map):
    return response_map.get(response, None)

# Function to reverse score an item
def reverse_score(score, scale):
    return scale + 1 - score

# Universal function to process subscales based on the master key dictionary
def process_subscales(df, scale_name):
    if df is None or scale_name not in master_key:
        print("Data or master key is not loaded")
        return

    # Pull the details from the master key for the given scale
    scale_details = master_key[scale_name]
    keywords, scale, response_map, reverse_columns, sections = scale_details
    max_score = max(response_map.values())
    print(max_score)
    
    # Initialize a dictionary to store scores for each section
    scores = {}
    
    # Iterate over sections (subscales)
    for section_name, items in sections.items():
        section_score = 0
        for item in items:
            # Check if the item exists in the dataframe
            if item in df.columns:
                # Map responses to numerical scores
                df[item] = df[item].apply(lambda x: map_response_to_score(x, response_map))
                
                # Apply reverse scoring if necessary
                if item in reverse_columns:
                    df[item] = df[item].apply(lambda x: reverse_score(x, max_score) if pd.notna(x) else x)

                # Sum the scores for the section
                section_score += df[item].sum()

        # Store the total score for the section
        scores[section_name] = section_score

    # Return the scores
    return scores




def process_survey(df):
    global master_score  # Declare master_score as a global variable
    
    scales = ["BIS_BAS"]  # You can add more scales here

    # Loop through each row (participant) in the DataFrame
    for index, row in df.iloc[2:].iterrows():  # Skip the first two rows
        # Process the row as a separate participant
        for scale in scales:
            scores = process_subscales(row.to_frame().T, scale)  # Convert the row to a DataFrame
            
            # Ensure scores is a dictionary and convert it to a DataFrame
            if isinstance(scores, dict):
                scores_df = pd.DataFrame([scores])  # Convert dict to DataFrame8=
                
                
                # Append the scores to the master_score DataFrame, creating a new row for each participant
                master_score = pd.concat([master_score, scores_df], ignore_index=True)

            else:
                print(f"Invalid data format for scale {scale} in row {index}: {type(scores)}")

    # Optionally display the current master_score after processing all participants
    display(master_score)




# Function to create the UI
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




# Start the UI
make_UI()

# Remove the first two rows from df_global
df_cleaned = df_global.iloc[2:]

# Extract the last name and response ID columns after skipping the first two rows
last_names = df_cleaned[['RecipientLastName', 'ResponseId']]

# Insert the last names and response IDs into the master_score DataFrame as the first columns
# First insert 'ResponseId' as the second column
master_score.insert(0, 'ResponseId', last_names['ResponseId'].reset_index(drop=True))

# Then insert 'Last Name' as the first column
master_score.insert(0, 'Last Name', last_names['RecipientLastName'].reset_index(drop=True))

# Save the updated master_score to a CSV file
master_score.to_csv('master_score.csv', index=False)
