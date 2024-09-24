import pandas as pd










def split_dataframe_by_keywords(df, sections_keywords):
    split_sections = {}  # Dictionary to store the resulting DataFrames
    
    for keywords in sections_keywords:
        # Join the keywords list into a name for the section
        section_name = '_'.join(keywords)
        
        # Filter the DataFrame columns based on the keywords for this section
        regex_pattern = '|'.join(keywords)  # Create a regex pattern to match any of the keywords
        section_df = df.filter(regex=regex_pattern)  # Filter the DataFrame
        
        # Create the dictionary key based on the section name
        split_sections[f'split_section_{section_name}'] = section_df

    return split_sections


def process_subscale(section, scale):
    if isinstance(section, pd.DataFrame):
        # Using if-else statement to handle different scales
        if scale[0] == "BIS_BAS":
            process_bis_bas(section)
        elif scale[0] == "hi":
            process_hi_scale(section)
        else:
            print(f"Error: No function found for scale {scale[0]}")


# Function to map text responses to numerical scores
def map_response_to_score_BIS_BAS(response):
    response_map = {
        "Very True for Me": 1,
        "Somewhat True": 2,
        "Somewhat False": 3,
        "Very False for Me": 4
    }
    return response_map.get(response, None)

# Using your reverse_score function
def reverse_score(num, scale):
    return scale + 1 - num

# Function to process BIS/BAS scale and calculate the scores
def process_bis_bas(section):
    print("Processing BIS/BAS scale...")

    # Skip the first row (title) and second row (metadata)
    section = section.iloc[2:].reset_index(drop=True)

    # Reverse scoring for specific items
    reverse_columns = ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)', 
                       'BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)',
                       'BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)',
                       'BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)']

    # Apply mapping and reverse scoring
    for col in section.columns:
        section[col] = section[col].apply(map_response_to_score_BIS_BAS)
        if col in reverse_columns:
            section[col] = section[col].apply(lambda x: reverse_score(x, 4) if pd.notna(x) else x)

    # Calculate the total scores for each section
    bas_drive_items = ['BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)']
    bas_fun_items = ['BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)']
    bas_rew_items = ['BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)']
    bis_items = ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)', 'BIS_2', 'BIS_22']



    scores = {
        "BAS_Drive": section[bas_drive_items].sum(axis=1).tolist(),
        "BAS_Fun_Seeking": section[bas_fun_items].sum(axis=1).tolist(),
        "BAS_Reward_Responsiveness": section[bas_rew_items].sum(axis=1).tolist(),
        "BIS": section[bis_items].sum(axis=1).tolist()
    }

    print("Scores calculated:")
    print(scores)

    return scores




def process_hi_scale(section):
    return section + ":)"
        