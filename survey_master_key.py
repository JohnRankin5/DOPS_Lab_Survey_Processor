# survey_master_key.py

master_key = {
    "BIS_BAS": [
        "matrix",  # Type of question
        ["Filler", "BAS", "BIS"],  # Keywords
        "BIS_BAS",  # Scale name
        {   # Response map for matrix questions
            "Very True for Me": 1,
            "Somewhat True": 2,
            "Somewhat False": 3,
            "Very False for Me": 4
        },
        ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)',  # Reverse columns
         'BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)',
         'BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)',
         'BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)'],
        {  # Sections with their items
            "BAS_Drive": ['BAS_drive_3(-)', 'BAS_drive_9(-)', 'BAS_drive_12(-)', 'BAS_drive_21(-)'],
            "BAS_Fun_Seeking": ['BAS_fun_5(-)', 'BAS_fun_10(-)', 'BAS_fun_15(-)', 'BAS_fun_20(-)'],
            "BAS_Reward_Responsiveness": ['BAS_rew_4(-)', 'BAS_rew_7(-)', 'BAS_rew_14(-)', 'BAS_rew_18(-)', 'BAS_rew_23(-)'],
            "BIS": ['BIS_8(-)', 'BIS_13(-)', 'BIS_16(-)', 'BIS_19(-)', 'BIS_24(-)', 'BIS_2', 'BIS_22']
        }
    ],
    "PANAS": [
        "matrix",  # Type of question
        ["PANAS"],  # Keywords
        "PANAS",  # Scale name
        {   # Response map for PANAS questions
            "Never": 1,
            "Almost Never": 2,
            "Neutral": 3,
            "Sometimes": 4,
            "Always": 5
        },
        [],  # No reverse scoring columns
        {   # Sections with their items
            "PANAS Positive Affect": ['PAN_inspire', 'PAN_determin', 'PAN_attent', 'PANAS_active', 'PAN_alert'],
            "PANAS Negative Affect": ['PAN_upset', 'PAN_hostile', 'PAN_ashame', 'PAN_nervous', 'PANAS_afraid']
        }
    ],
    "DES": [
        "slider",  # Type of question (slider, for percentage answers)
        ["DES"],  # Keywords
        "DES",  # Scale name
        {},  # No response map (because it's direct numerical input)
        [],  # No reverse scoring columns
        {   # Sections (28 slider questions)
            "Dissociative Experiences Total": ['DES_1', 'DES_2', 'DES_3', 'DES_4', 'DES_5', 'DES_6', 'DES_7', 
                                                'DES_8', 'DES_9', 'DES_10', 'DES_11', 'DES_12', 'DES_13', 
                                                'DES_14', 'DES_15', 'DES_16', 'DES_17', 'DES_18', 'DES_19', 
                                                'DES_20', 'DES_21', 'DES_22', 'DES_23', 'DES_24', 'DES_25', 
                                                'DES_26', 'DES_27', 'DES_28']
        }
    ]
}
