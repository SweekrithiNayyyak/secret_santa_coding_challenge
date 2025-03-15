# import pandas as pd

# class ParseCSV:
#     def __init__(self, file_path):
#         self.file = file_path

#     def load_details(self, **rows_required):
#         df = pd.read_csv(self.file)
#         if not rows_required:
#             return df.to_dict(
#                 orient="records"
#             )  # Return all rows as a list of dictionaries

#         return df[list(rows_required.keys())].to_dict(orient="records")

import pandas as pd
import random
from collections import defaultdict


class ParseCSV:
    def __init__(self, file_path):
        self.file = file_path

    def load_details(self, *columns):
        """Load CSV and return data of each row with specified columns."""
        try:
            df = pd.read_csv(self.file)
        except FileNotFoundError:
            print(f"Error: File {self.file} not found.")
            return []
        except pd.errors.EmptyDataError:
            print(f"Error: File {self.file} is empty.")
            return []
        except pd.errors.ParserError:
            print(f"Error: File {self.file} is not a valid CSV.")
            return []

        if not columns:
            return df.to_dict(
                orient="records"
            )  # Return all rows as a list of dictionaries

        valid_columns = [col for col in columns if col in df.columns]
        if not valid_columns:
            print("Warning: None of the requested columns are present in the file.")
            return []

        return df[valid_columns].to_dict(orient="records")
