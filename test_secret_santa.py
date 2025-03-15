import pytest
import os
import pandas as pd
from parse_csv import ParseCSV
from secret_santa import SecretSanta

# Test CSV file directory
TEST_DIR = "test_data/"
os.makedirs(TEST_DIR, exist_ok=True)


# Helper function to create test CSV files
def create_test_csv(filename, data):
    filepath = os.path.join(TEST_DIR, filename)
    with open(filepath, "w") as f:
        f.write(data)
    return filepath


#  Ensure correct CSV parsing
def test_parse_csv():
    employee_csv = create_test_csv(
        "employees.csv",
        """Employee_Name,Employee_EmailID
    John Doe,john.doe@example.com
    Jane Smith,jane.smith@example.com""",
    )

    parser = ParseCSV(employee_csv)
    data = parser.load_details("Employee_Name", "Employee_EmailID")
    assert len(data) == 2
    assert data[0]["Employee_EmailID"] == "john.doe@example.com"
    os.remove(employee_csv)


# Ensure everyone gets assigned
def test_secret_santa_assignments():
    employee_csv = create_test_csv(
        "employees.csv",
        """Employee_Name,Employee_EmailID
    John Doe,john.doe@example.com
    Jane Smith,jane.smith@example.com
    Alice Brown,alice.brown@example.com
    Bob White,bob.white@example.com""",
    )

    previous_csv = create_test_csv(
        "previous.csv",
        """Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
John Doe,john.doe@example.com,Alice Brown,alice.brown@example.com
Jane Smith,jane.smith@example.com,Bob White,bob.white@example.com
Alice Brown,alice.brown@example.com,John Doe,john.doe@example.com
Bob White,bob.white@example.com,Jane Smith,jane.smith@example.com
""",
    )

    santa = SecretSanta(employee_csv, previous_csv)
    assignments = santa.assign_santa()
    assert len(assignments) == 4
    for employee, assigned in assignments.items():
        assert employee != assigned
        assert assigned not in [santa.previous_assignments.get(employee, "")]

    os.remove(employee_csv)
    os.remove(previous_csv)


#  Ensure output CSV is created
def test_output_csv():
    employee_csv = create_test_csv(
        "employees.csv",
        """Employee_Name,Employee_EmailID
    John Doe,john.doe@example.com
    Jane Smith,jane.smith@example.com""",
    )
    previous_csv = create_test_csv(
        "previous.csv", "Employee_EmailID,Secret_Child_EmailID"
    )
    output_csv = os.path.join(TEST_DIR, "output.csv")

    santa = SecretSanta(employee_csv, previous_csv)
    santa.save_assignments(output_csv)
    assert os.path.exists(output_csv)
    df = pd.read_csv(output_csv)
    assert len(df) == 2
    os.remove(employee_csv)
    os.remove(previous_csv)
    os.remove(output_csv)


# Edge case - Single employee (should raise error)
def test_single_employee():
    employee_csv = create_test_csv(
        "single_employee.csv",
        """Employee_Name,Employee_EmailID
    John Doe,john.doe@example.com""",
    )

    with pytest.raises(ValueError):
        santa = SecretSanta(employee_csv)
        santa.assign_santa()

    os.remove(employee_csv)


def test_right_output():
    """Test if Secret Santa assignments follow the rules."""
    print("Starting test_right_output")

    # Create employee CSV
    employee_csv = create_test_csv(
        "employees.csv",
        """Employee_Name,Employee_EmailID
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
Alice Brown,alice.brown@example.com
Bob White,bob.white@example.com""",
    )

    # Create previous assignments CSV
    previous_csv = create_test_csv(
        "previous.csv",
        """Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
John Doe,john.doe@example.com,Alice Brown,alice.brown@example.com
Jane Smith,jane.smith@example.com,Bob White,bob.white@example.com
Alice Brown,alice.brown@example.com,John Doe,john.doe@example.com
Bob White,bob.white@example.com,Jane Smith,jane.smith@example.com""",
    )

    output_file = os.path.join(TEST_DIR, "output.csv")

    # Run Secret Santa assignment
    santa = SecretSanta(employee_csv, previous_csv)
    santa.save_assignments(output_file)

    assert os.path.exists(output_file), "Output file was not created"

    df = pd.read_csv(output_file)

    employees = {
        row["Employee_EmailID"]: row["Employee_Name"]
        for _, row in pd.read_csv(employee_csv).iterrows()
    }
    previous_assignments = {
        row["Employee_EmailID"]: row["Secret_Child_EmailID"]
        for _, row in pd.read_csv(previous_csv).iterrows()
    }

    assigned_set = set()

    # Validate each row
    for index, row in df.iterrows():
        employee_email = row["Employee_EmailID"]
        assigned_child_email = row["Secret_Child_EmailID"]

        #  Employee cannot be assigned to themselves
        assert (
            employee_email != assigned_child_email
        ), f"Error: {employee_email} assigned to themselves."

        #  Employee cannot be assigned their previous year's match
        assert assigned_child_email != previous_assignments.get(
            employee_email, None
        ), f"Error: {employee_email} assigned to last year's match {assigned_child_email}."

        # Each employee should be assigned only once
        assert (
            assigned_child_email not in assigned_set
        ), f"Error: {assigned_child_email} assigned more than once."
        assigned_set.add(assigned_child_email)

    os.remove(output_file)


# Run the tests
if __name__ == "__main__":
    pytest.main()
