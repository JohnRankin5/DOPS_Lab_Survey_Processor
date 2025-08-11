# Survey Processor (GUI)

A Tkinter-based GUI application to:
- Load a CSV file of survey responses,
- Parse a YAML **master key** describing how each survey scale is scored,
- Process each participant’s responses according to the scoring rules,
- Optionally insert selected **custom columns** from `config.yaml` into the output,
- Save the processed `master_score.csv` file.

## Quick start

### 1) Environment setup & install
```bash
# Optional: Create & activate a Conda environment
conda create -n survey python=3.11 -y
conda activate survey

# Install dependencies (tkinter is included in most Python installs)
pip install pandas PyYAML
```

### 2) Files expected in the **working** folder
```
survey_master_key.yaml   # Scoring rules for all scales
config.yaml              # Defines which CSV columns to copy to the output
your_survey_export.csv   # Survey data (uploaded via GUI)
main.py                  # The main script
```

### 3) Run
```bash
python main.py
```

Make sure you are in the src directory

1. Click **Upload File** → select your CSV file.
2. Click **Everyone** → compute scores for all participants.
3. When the GUI closes, a Save dialog will appear → choose where to save the final CSV.

---

## Data formats

### `survey_master_key.yaml` schema

```yaml
MyScaleA:
  type: "matrix"                      
  keywords: ["optional", "tags"]      
  scale_name: "MyScaleA"              
  response_map:                       
    "Strongly disagree": 1
    "Disagree": 2
    "Neutral": 3
    "Agree": 4
    "Strongly agree": 5
  reverse_columns: ["Q3", "Q8"]       
  sections:                           
    Engagement: ["Q1","Q2","Q3"]
    Satisfaction: ["Q4","Q5","Q6"]
```

Look at the example yaml file

**Notes on `type`:**
- **matrix** → sums mapped item scores per section; reverse scoring uses `max(response_map.values())`.
- **multiple_choice_binary** → maps to 0/1 and sums; reverse scoring flips binary.
- **multiple_choice_average** → maps to 0/1 and averages per section.
- **slider** → treats responses as numeric and averages per section.

### `config.yaml` example

```yaml
custom_columns:
  - RecipientLastName
  - RecipientFirstName
  - ResponseID
  - DateSubmitted
```
> These column names (case-insensitive) will be inserted at the start of the final CSV.

---

## CSV expectations

- This would be the unedited CSV file direclty from Quartics
- Row **0**: column headers (actual names used in processing).
- Rows **0–1**: treated as metadata → dropped before scoring.
- Column names in `sections` of the master key must match the CSV headers (case-insensitive match is applied after lowercasing).

---

## Function reference

### `convert_yaml_to_master_key(yaml_data) -> dict`
Converts the YAML data into the internal list format:
```python
{
  scale_name: [
    q_type,
    keywords,
    scale_name,
    response_map,
    reverse_columns,
    sections
  ],
  ...
}
```

### `upload_file()`
- Opens a file dialog to choose a CSV file.
- Loads the file into the global `df_global` DataFrame.
- Displays a confirmation message.

### `map_response_to_score(response, response_map)`
Maps a raw survey response to its numeric score according to `response_map`. Returns `None` if the response is not found.

### `reverse_score(score, max_score)`
Reverses ordinal scores: `max_score + 1 - score`.

### `reverse_score_binary(score)`
Flips a binary score: `0 → 1`, `1 → 0`.

### `process_subscales(df, scale_name) -> dict`
Processes a **single participant** (1-row DataFrame) for the given `scale_name`:
- Maps raw responses to numeric scores.
- Applies reverse scoring to specified `reverse_columns`.
- Aggregates per section based on `q_type`:
  - **matrix**: sum of scores
  - **multiple_choice_binary**: sum of binary values
  - **multiple_choice_average**: average per section
  - **slider**: average of numeric values, rounded to 3 decimals

Returns `{section_name: score, ...}`.

### `process_survey(df)`
Processes all participants in `df`:
- Skips first two metadata rows (`df.iloc[2:]`).
- For each participant, calls `process_subscales()` for all scales in `master_key`.
- Merges all section scores into one row and appends to the global `master_score` DataFrame.

### `make_UI()`
Builds the Tkinter interface:
- **Upload File** button → triggers `upload_file()`.
- **Everyone** button → calls `process_survey(df_global)`.
- Runs `root.mainloop()` to start the GUI.

### `main()`
Controls overall execution:
1. Runs the GUI.
2. After closing:
   - Cleans and lowercases headers from uploaded CSV.
   - Drops the first two metadata rows.
   - Loads `config.yaml` and finds matching `custom_columns`.
   - Inserts these columns at the start of `master_score`.
   - Prompts for save location and writes the CSV.

---

## Output

A CSV file with:
1. Custom columns from `config.yaml`.
2. Computed section scores per participant.

---

## Troubleshooting

- **"No matching columns found"** → Check that your CSV headers and `config.yaml` column names match (case-insensitive).
- Reverse scoring for **matrix** types depends on `max(response_map.values())` → ensure consistent scales.
- **slider** items must be numeric in the CSV.
- If GUI doesn’t open on Windows, ensure Python was installed with Tkinter.

---

## Example workflow

1. Edit `survey_master_key.yaml` and `config.yaml` to match your survey structure.
2. Run:
```bash
python main.py
```
3. Upload your CSV when prompted.
4. Click **Everyone** to process all participants.
5. Choose where to save the resulting `master_score.csv`.
