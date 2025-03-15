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
        self.assignment_map = defaultdict(list)

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
        """Create a hash table mapping employees to possible secret children based on emails."""
        for email in self.employees:
            self.assignment_map[email] = [
                e
                for e in self.employees
                if e != email and e != self.previous_assignments.get(email, None)
            ]

    def assign_santa(self):
        """Ensure everyone gets assigned first, then optimize choices while preserving order."""
        self.build_assignment_map()
        assignments = {}
        available_employees = set(self.employees.keys())

        ordered_employees = list(self.employees.keys())

        for email in ordered_employees:
            possible_choices = [
                e
                for e in available_employees
                if e != email and e not in assignments.values()
            ]
            if not possible_choices:
                raise ValueError("Failed to generate a valid assignment. Try again!")

            choice_email = random.choice(possible_choices)
            assignments[email] = choice_email
            available_employees.remove(choice_email)

        for email in assignments:
            if (
                email in self.assignment_map
                and assignments[email] in self.assignment_map[email]
            ):
                continue

            better_choices = [
                e for e in self.assignment_map[email] if e in available_employees
            ]
            if better_choices:
                new_choice = random.choice(better_choices)
                available_employees.add(assignments[email])
                assignments[email] = new_choice
                available_employees.remove(new_choice)

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
