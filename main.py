from secret_santa import SecretSanta

if __name__ == "__main__":
    import os

    def get_valid_file(prompt):
        while True:
            file_path = input(prompt).strip()
            if os.path.exists(file_path):
                return file_path
            print("Error: File does not exist. Please enter a valid file path.")

    employee_file = get_valid_file("Enter path to the Employee list file: ")
    previous_year_file = get_valid_file(
        "Enter path to the previous year Secret Santa game results: "
    )

    santa = SecretSanta(employee_file, previous_year_file)
    santa.save_assignments("new_assignments.csv")
