import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import yaml
import gc  # For garbage collection to clean memory

# Global variables
df_global = None  # To store the uploaded DataFrame
master_score = pd.DataFrame()  # To store the computed scores
participant_df = pd.DataFrame()  # To store the participant's data
individual = False # To check if the user selected 'Individual' option

# Load the YAML file containing the master key for the survey scales
with open('survey_master_key.yaml', 'r') as f:
    master_key_yaml = yaml.safe_load(f)

# Function to convert YAML data into the required master key format
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
master_key = convert_yaml_to_master_key(master_key_yaml)

# Function to handle file upload and process CSV
def upload_file():
    global df_global
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df_global = pd.read_csv(file_path)
        messagebox.showinfo("File Uploaded", f"File processed: {file_path}")
    else:
        messagebox.showwarning("No File", "No file was selected!")

# Function to map text responses to numerical scores
def map_response_to_score(response, response_map):
    return response_map.get(response, None)

# Function to reverse score an item for general scales
def reverse_score(score, max_score):
    return max_score + 1 - score

# Reverse scoring logic for binary (0 and 1) questions
def reverse_score_binary(score):
    return abs(1 - score)  # Flip between 0 and 1

# Function to process subscales based on question type
def process_subscales(df, scale_name):
    if df is None or scale_name not in master_key:
        print("Data or master key is not loaded")
        return

    # Retrieve details from the master key for the given scale
    scale_details = master_key[scale_name]
    q_type, keywords, scale, response_map, reverse_columns, sections = scale_details
    max_score = max(response_map.values()) if response_map else None  # For matrix and multiple choice

    # Initialize a dictionary to store scores for each section
    scores = {}

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

    elif q_type == "multiple_choice_binary":
        # Binary (yes/no) questions processing
        for section_name, items in sections.items():
            section_score = 0
            for item in items:
                if item in df.columns:
                    # Map responses to numerical scores
                    df[item] = df[item].apply(lambda x: map_response_to_score(x, response_map))
                    # Apply reverse scoring if necessary
                    if item in reverse_columns:
                        df[item] = df[item].apply(lambda x: reverse_score_binary(x) if pd.notna(x) else x)
                    # Sum the scores for the section
                    section_score += df[item].sum()
            # Store the total score for the section
            scores[section_name] = section_score


    
    elif q_type == "multiple_choice_average":
        for section_name, items in sections.items():
            section_score = 0
            for item in items:
                if item in df.columns:
                    # Map responses to numerical scores
                    df[item] = df[item].apply(lambda x: map_response_to_score(x, response_map))
                    # Apply reverse scoring if necessary
                    if item in reverse_columns:
                        df[item] = df[item].apply(lambda x: reverse_score_binary(x) if pd.notna(x) else x)
                    # Sum the scores for the section
                    section_score += df[item].sum()
            # Store the total score for the section
            scores[section_name] = section_score / len(items)


    elif q_type == "slider":
    


        # Slider Question Processing
        for section_name, items in sections.items():
            section_score = 0
            valid_items = 0  # Count valid items for averaging
            for item in items:
                if item in df.columns:
                    # Sum up all the slider values (assumed to be percentages)
                    section_score += df[item].astype(float).sum()
                    valid_items += 1
            # Calculate the average score (sum divided by number of items)
            if valid_items > 0:
                average_score = section_score / valid_items
                scores[section_name] = round(average_score, 3)  # Store the average score
            else:
                scores[section_name] = 0

                
    return scores




def process_data_by_last_name(last_name):
    global individual, participant_df
    individual = True # Set individual to True
    # Check if df_global and master_key have data
    if df_global is None or master_key is None:
        messagebox.showwarning("No Data", "No data available! Please upload a file and load the master key.")
        return

    # Find the row of the participant by last name
    matched_row = df_global[df_global['RecipientLastName'].str.lower() == last_name.lower()]
    
    # Check if the participant was found
    if matched_row.empty:
        messagebox.showinfo("No Results", f"No results found for '{last_name}'.")
        return
    else:
        messagebox.showinfo("Participant Found", f"Participant '{last_name}' found")

    # Extract the participant's data into a new DataFrame
    participant_df = pd.concat([df_global.iloc[:2], matched_row], ignore_index=True)


    # Process each scale using the process_subscales function
    process_survey(participant_df)



# Function to process the survey data and compute scores
def process_survey(df):
    global master_score  # Declare master_score as a global variable
    scales = list(master_key.keys())  # Dynamically extract all the scale names

    # Loop through each row (participant) in the DataFrame, skipping the first two rows
    for index, row in df.iloc[2:].iterrows():
        combined_scores = {}
        for scale in scales:
            # Convert the row to a DataFrame for processing
            scores = process_subscales(row.to_frame().T, scale)
            if isinstance(scores, dict):
                combined_scores.update(scores)
            else:
                print(f"Invalid data format for scale {scale} in row {index}: {type(scores)}")
        # Convert combined scores to DataFrame and append to master_score
        combined_scores_df = pd.DataFrame([combined_scores])
        master_score = pd.concat([master_score, combined_scores_df], ignore_index=True)

# Function to clear sensitive data from memory
def clear_sensitive_data():
    global df_global
    if df_global is not None:
        del df_global  # Clear the DataFrame from memory
        df_global = None  # Reset the global variable
    gc.collect()  # Force garbage collection

# Function to create the GUI using tkinter
def make_UI():
    # Function for 'Everyone' button action
    def everyone_action():
        if df_global is not None:
            process_survey(df_global)
            messagebox.showinfo("Processing Complete", "Survey data has been processed.")
        else:
            messagebox.showwarning("No Data", "No data available! Please upload a file.")

    # Function for 'Individual' button action
    def individual_action():
        global individual  # Declare individual as global
        individual = True
        last_name = entry_last_name.get()
        if last_name:
            process_data_by_last_name(last_name)  # Call the processing function with the entered last name
        else:
            messagebox.showwarning("Input Error", "Please enter a last name!")


    # Create the root window
    root = tk.Tk()
    root.title("File Uploader & Search Interface")
    root.geometry("550x450")  # Set window size
    root.grid_columnconfigure(0, weight=1)  # Center align elements

    # Styling variables
    button_style = {"font": ("Arial", 14)}
    label_style = {"font": ("Arial", 16)}
    entry_style = {"font": ("Arial", 14)}

    # Title Label
    title_label = tk.Label(root, text="File Uploader & Search Interface", **label_style)
    title_label.pack(pady=20)

    # Upload File Section
    upload_btn = tk.Button(root, text="Upload File", command=upload_file, **button_style)
    upload_btn.pack(pady=10)

    # Separator
    separator = tk.Label(root, text="----------------", **label_style)
    separator.pack(pady=10)

    # 'Everyone' Button
    everyone_btn = tk.Button(root, text="Everyone", command=everyone_action, **button_style)
    everyone_btn.pack(pady=10)

    # Search by Individual
    label_last_name = tk.Label(root, text="Search by Last Name:", **label_style)
    label_last_name.pack(pady=10)

    entry_last_name = tk.Entry(root, width=30, **entry_style)
    entry_last_name.pack(pady=10)

    individual_btn = tk.Button(root, text="Individual", command=individual_action, **button_style)
    individual_btn.pack(pady=10)

    # Start the application
    root.mainloop()

# Start the GUI application
make_UI()

# After GUI closes, process and save the master_score DataFrame
if df_global is not None:


    if individual:

            df_cleaned = participant_df.iloc[2:]
            # Extract the last name and response ID columns after skipping the first two rows
            last_names = df_cleaned[['RecipientLastName', 'ResponseId']].reset_index(drop=True)



            # Insert the last names and response IDs into the master_score DataFrame as the first columns
            master_score.insert(0, 'ResponseId', last_names['ResponseId'])
            master_score.insert(0, 'Last Name', last_names['RecipientLastName'])

        
 
    else:
        # Remove the first two rows from df_global
        df_cleaned = df_global.iloc[2:]

        # Extract the last name and response ID columns after skipping the first two rows
        last_names = df_cleaned[['RecipientLastName', 'ResponseId']].reset_index(drop=True)

        # Insert the last names and response IDs into the master_score DataFrame as the first columns
        master_score.insert(0, 'ResponseId', last_names['ResponseId'])
        master_score.insert(0, 'Last Name', last_names['RecipientLastName'])

    # Prompt user to specify the save location and file name
    file_path = filedialog.asksaveasfilename(
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv")],
    title="Save the master score file",
    initialfile="master_score.csv"
    )

    # Save the updated master_score to the specified file if a path was selected
    if file_path:
        master_score.to_csv(file_path, index=False)
        print(f"File saved to {file_path}")
    else:
        print("Save operation was canceled.")



    # Clear sensitive data from memory
    clear_sensitive_data()
else:
    print("No data was processed.")
