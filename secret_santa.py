import pandas as pd
import random
from collections import defaultdict

from parse_csv import ParseCSV


class SecretSanta:
    def __init__(self, employee_file, previous_assignments_file=None):
        self.employee_file = employee_file
        self.previous_assignments_file = previous_assignments_file
        self.employees = self.load_employees()
        self.previous_assignments = (
            self.load_previous_assignments() if previous_assignments_file else {}
        )
        self.assignment_map = self.build_assignment_map()

    def load_employees(self):
        """Load employee data from CSV."""
        parser = ParseCSV(self.employee_file)
        data = parser.load_details("Employee_Name", "Employee_EmailID")
        return {
            row["Employee_EmailID"]: (row["Employee_Name"], row["Employee_EmailID"])
            for row in data
            if "Employee_EmailID" in row
        }

    def load_previous_assignments(self):
        """Load previous year's assignments."""
        parser = ParseCSV(self.previous_assignments_file)
        data = parser.load_details("Employee_EmailID", "Secret_Child_EmailID")
        return {
            row["Employee_EmailID"]: row["Secret_Child_EmailID"]
            for row in data
            if "Employee_EmailID" in row and "Secret_Child_EmailID" in row
        }

    def build_assignment_map(self):
        """Creates a hash table mapping employees to possible secret children."""
        assignment_map = {}
        for email in self.employees:
            possible_choices = set(self.employees.keys()) - {email}
            if email in self.previous_assignments:
                possible_choices.discard(self.previous_assignments[email])
            assignment_map[email] = possible_choices
        return assignment_map

    def assign_santa(self):
        """Assigns Secret Santa using a backtracking approach to avoid deadlocks."""
        ordered_employees = list(self.employees.keys())
        assignments = {}
        used = set()

        def backtrack(index):
            if index == len(ordered_employees):
                return True  # Successfully assigned all

            email = ordered_employees[index]
            choices = list(self.assignment_map[email] - used)
            if not choices:
                return False  # No valid assignment, trigger backtracking

            random.shuffle(choices)  # Shuffle to introduce randomness

            for choice in choices:
                assignments[email] = choice
                used.add(choice)
                if backtrack(index + 1):
                    return True  # If successful, return immediately
                # Undo the assignment (backtrack)
                used.remove(choice)
                del assignments[email]
            return False

        if not backtrack(0):
            raise ValueError("Failed to find a valid Secret Santa assignment.")

        return assignments

    def save_assignments(self, output_file):
        """Save assignments to a CSV file while preserving order."""
        assignments = self.assign_santa()
        ordered_data = [
            (self.employees[k][0], k, self.employees[assignments[k]][0], assignments[k])
            for k in self.employees.keys()
            if k in assignments
        ]
        df = pd.DataFrame(
            ordered_data,
            columns=[
                "Employee_Name",
                "Employee_EmailID",
                "Secret_Child_Name",
                "Secret_Child_EmailID",
            ],
        )
        df.to_csv(output_file, index=False)
        print(f"Assignments saved to {output_file}")
