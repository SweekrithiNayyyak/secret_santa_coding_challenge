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
  
```

## Setup & Installation
### Prerequisites
Ensure you have Python installed (>=3.6). You will also need Pandas:
```bash
pip install pandas
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

## Features
Efficient assignment using circular rotation.
Preserves employee order.
Prevents self-assignments and repeated matches.
Modular and extensible design for easy maintenance.



