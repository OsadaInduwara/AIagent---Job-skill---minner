import json
import os
from typing import Dict, Any
from datetime import datetime


class StorageService:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def save_results(self, filename: str, data: Dict[str, Any]) -> str:
        try:
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Results saved to {filepath}")
            return filepath

        except Exception as e:
            print(f"Failed to save results: {e}")
            raise

    def load_results(self, filename: str) -> Dict[str, Any]:
        try:
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, 'r') as f:
                data = json.load(f)

            return data

        except Exception as e:
            print(f"Failed to load results: {e}")
            return {}

    def export_to_csv(self, data: Dict[str, Any], filename: str) -> str:
        import pandas as pd

        try:
            jobs_data = data.get("jobs_with_skills", [])

            if jobs_data:
                df = pd.DataFrame(jobs_data)
                csv_path = os.path.join(self.data_dir, f"{filename}.csv")
                df.to_csv(csv_path, index=False)
                return csv_path

        except Exception as e:
            print(f"Failed to export CSV: {e}")
            return ""