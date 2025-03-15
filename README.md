# secret_santa_coding_challenge

# Secret Santa Assignment

## Overview
This project automates the process of assigning Secret Santa pairs while ensuring that:
- Each employee gets a unique secret child.
- Employees are not assigned to themselves.
- Employees are not assigned to the same person as in the previous year.
- The assignment process is optimized for efficiency (O(1) lookups and assignment).

## Project Structure
```
|-- main.py               # Entry point of the application
|-- parse_csv.py          # Handles CSV reading and validation
|-- secret_santa.py       # Contains the Secret Santa assignment logic
|-- test_secret_santa.py  # Contains test cases
```

## Setup & Installation
### Prerequisites
Ensure you have Python installed (>=3.6). You will also need Pandas:
```bash
pip install pandas pytest
```

### Running the Program
1. Place your employee list CSV and previous year’s assignment CSV in the project directory.
2. Run the script:
```bash
python main.py
```
3. Follow the prompts to provide the correct file paths.
4. The new assignments will be saved in `new_assignments.csv`.

## CSV File Format
### `employees.csv`
```
Employee_Name,Employee_EmailID
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

### `previous_year.csv`
```
Employee_EmailID,Secret_Child_EmailID
john.doe@example.com,jane.smith@example.com
jane.smith@example.com,john.doe@example.com
```

### Output: `new_assignments.csv`
```
Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
John Doe,john.doe@example.com,Jane Smith,jane.smith@example.com
Jane Smith,jane.smith@example.com,John Doe,john.doe@example.com
```
## Explanation of Code
### **1. `main.py` (Entry Point)**
- Handles user input and ensures valid file paths are provided.
- Calls `SecretSanta` to process assignments and generates output CSV.

### **2. `parse_csv.py` (CSV Parsing)**
- Reads employee and previous assignment data from CSV files.
- Handles errors like missing files, malformed CSVs, and missing columns.

### **3. `secret_santa.py` (Assignment Logic)**
- Ensures each employee gets assigned a unique recipient.
- Avoids self-assignments and previous matches.
- Uses a **circular assignment approach** to ensure correctness.

## Automated Tests
The `test_secret_santa.py` file contains test cases to ensure the correctness and reliability of the code.

### **Test Cases Implemented**

| Test Case | Description |
|-----------|-------------|
| **test_parse_csv** | Ensures the CSV file is parsed correctly and all data is loaded. |
| **test_secret_santa_assignments** | Verifies that all employees get assigned, with no self-assignments or repeat matches. |
| **test_output_csv** | Ensures that the Secret Santa assignments are written to an output CSV file correctly. |
| **test_single_employee** | Ensures that the script raises a `ValueError` when only one employee exists. |

### **How to Run Tests**
Run the following command to execute all test cases:
```bash
pytest test_secret_santa.py
```

The tests ensure:
 The script runs successfully with valid inputs.
 Edge cases are handled properly.
 The output meets expected constraints (no self-assignments, no repeated matches).
Performance remains stable with different data inputs.

## Features
Efficient assignment using circular rotation.
Preserves employee order.
Prevents self-assignments and repeated matches.
Modular and extensible design for easy maintenance.



