
import os
import pandas as pd
from loguru import logger
from pathlib import Path


class RecipesDataset:
    DATASET_URL = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    DATASET_FILE_NAME = "recipes.json"

    def download(self, output_file):
        """"Downloads the dataset from the specified URL."""
        df = pd.read_json(self.DATASET_URL, lines=True)
        df.to_json(output_file, orient='records', indent=4)
        logger.info(f"Dataset downloaded to {output_file}")
        return

    def load(self, file_path):
        """"Loads the dataset from a local JSON file."""
        df =  pd.read_json(file_path)
        logger.info(f"Dataset loaded from {file_path}")
        return df
    
    def is_downloaded(self, file_path):
        """"Checks if the dataset file already exists locally."""
        if os.path.exists(file_path):
            logger.info(f"Dataset found at {file_path}")
            return True
        return False
    
    def get_dataset(self):
        """"Gets the dataset, downloading it if necessary."""
        output_file = Path(__file__).parent / self.DATASET_FILE_NAME

        if not self.is_downloaded(output_file):
            self.download(output_file)
    
        df = self.load(output_file)
        return df