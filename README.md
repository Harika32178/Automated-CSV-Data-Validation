# Automated CSV Data Validation Tool

A beginner-friendly Python command-line project that checks a CSV file for:
- Missing values
- Invalid email formats (when an `Email` column is present)
- Invalid ages (when an `Age` column is present; allowed range: 0–120)
- Duplicate rows

It creates two output files beside the input CSV:
- `<filename>_cleaned.csv` — rows that passed all checks
- `<filename>_validation_report.csv` — issues found, with row numbers

## Requirements
- Python 3.8 or newer
- No external Python packages required

## Run the sample

Open a terminal in this project folder and run:

```bash
python validator.py sample_data/employees.csv
```

On Windows, `py` also works:

```bash
py validator.py sample_data/employees.csv
```

Open the `sample_data` folder to see the generated output files.

## Try your own CSV
Your CSV should have a header row. If you want email and age checks, name those columns
exactly `Email` and `Age` (case-sensitive). Then run:

```bash
python validator.py path/to/your_file.csv
```

## Learning points
This project demonstrates Python file handling, CSV processing, dictionaries, loops,
regular expressions, input validation, exception handling, and command-line arguments.

## Important
Understand and test the code yourself before describing this project on a CV.
