import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from IPython.display import display
import yaml
import gc  # For garbage collection to clean memory

# Load the YAML file This will be the master key for the survey scales
with open('survey_master_key.yaml', 'r') as f:
    master_key = yaml.safe_load(f)



# Convert the loaded YAML into the desired format (if needed)
def convert_yaml_to_master_key(yaml_data):
    converted_master_key = {}
    
    for scale_name, scale_details in yaml_data.items():
        q_type = scale_details['type']
        keywords = scale_details['keywords']
        scale_name = scale_details['scale_name']
        response_map = scale_details['response_map']
        reverse_columns = scale_details['reverse_columns']
        sections = scale_details['sections']

        converted_master_key[scale_name] = [
            q_type,
            keywords,
            scale_name,
            response_map,
            reverse_columns,
            sections
        ]
    
    return converted_master_key

# Convert the loaded YAML data to match the Python structure
master_key = convert_yaml_to_master_key(master_key)



#Testing ---
master_score = pd.DataFrame()


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


def process_subscales(df, scale_name):
    if df is None or scale_name not in master_key:
        print("Data or master key is not loaded")
        return

    # Pull the details from the master key for the given scale
    scale_details = master_key[scale_name]
    q_type, keywords, scale, response_map, reverse_columns, sections = scale_details
    max_score = max(response_map.values()) if response_map else None  # Only for matrix and multiple choice
    
    # Initialize a dictionary to store scores for each section
    scores = {}

    # Process based on question type
    if q_type == "matrix":
        # Matrix Question Processing
        for section_name, items in sections.items():
            section_score = 0
            for item in items:
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

    elif q_type == "multiple_choice":
        # Multiple Choice Question Processing
        for section_name, items in sections.items():
            section_score = 0
            for item in items:
                if item in df.columns:
                    # Map responses to numerical scores for multiple choice
                    df[item] = df[item].apply(lambda x: map_response_to_score(x, response_map))
                    
                    # Sum the scores for the section
                    section_score += df[item].sum()

            # Store the total score for the section
            scores[section_name] = section_score


        

    elif q_type == "slider":
        # Slider Question Processing (DES scale)
        for section_name, items in sections.items():
            section_score = 0
            valid_items = 0  # Count valid items for averaging
            for item in items:
                if item in df.columns:
                    # Sum up all the slider values (already percentages)
                    section_score += df[item].astype(float).sum()
                    valid_items += 1

            # Calculate the average score (sum divided by number of items)
            if valid_items > 0:
                average_score = section_score / valid_items
                scores[section_name] = round(average_score, 3) # Store the average score for DES
            else:
                scores[section_name] = 0

    return scores






def process_survey(df):
    global master_score  # Declare master_score as a global variable
    
    scales = list(master_key.keys())  # This will dynamically extract all the keys

    # Loop through each row (participant) in the DataFrame
    for index, row in df.iloc[2:].iterrows():  # Skip the first two rows
        combined_scores = {}  # Initialize a dictionary to store combined scores for one participant
        
        # Process the row for each scale
        for scale in scales:
            scores = process_subscales(row.to_frame().T, scale)  # Convert the row to a DataFrame
            
            # Ensure scores is a dictionary and merge it into combined_scores
            if isinstance(scores, dict):
                combined_scores.update(scores)  # Merge the scores for this scale into combined_scores
            else:
                print(f"Invalid data format for scale {scale} in row {index}: {type(scores)}")
        
        # After processing all scales, append the combined scores to master_score
        combined_scores_df = pd.DataFrame([combined_scores])  # Convert combined_scores to DataFrame
        
        # Append the combined scores to the master_score DataFrame, creating a new row for each participant
        master_score = pd.concat([master_score, combined_scores_df], ignore_index=True)

    # Optionally display the current master_score after processing all participants
    display(master_score)





def clear_sensitive_data():
    global df_global, file_path_global
    
    # Clear DataFrame from memory
    if df_global is not None:
        del df_global  # Clear the DataFrame from memory
        df_global = None  # Reset the global variable
    
    # Reset the file path variable, but do not delete the file
    file_path_global = None
    
    # Force garbage collection to clear memory
    gc.collect()



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


clear_sensitive_data()  # Clear sensitive data. Remove all temporary files and clear memory.