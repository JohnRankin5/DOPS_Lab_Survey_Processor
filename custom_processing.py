def process_custom(df, scale_name, master_key):
    """
    Custom processing function for various scales (Positive-Constructive Daydreaming,
    Guilt and Fear-of-Failure Daydreaming, Poor Attentional Control).
    """
    custom_scores = {}

    # Get the starting points and items to add/subtract for the selected scale
    starting_points = master_key[scale_name].get('starting_points', 0)
    items_to_add = master_key[scale_name].get('items_to_add', [])
    items_to_subtract = master_key[scale_name].get('items_to_subtract', [])

    # Add points for items to be added
    add_score = df[items_to_add].sum().sum()  # Sum the selected items
    subtract_score = df[items_to_subtract].sum().sum()  # Sum the items to be subtracted

    # Calculate the total score for the scale
    total_score = starting_points + add_score - subtract_score
    custom_scores[f'{scale_name}_Score'] = total_score

    return custom_scores
