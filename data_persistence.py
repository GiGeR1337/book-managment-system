import logging
import os
import pickle

import pandas as pd

logger = logging.getLogger(__name__)
SAVE_PATH = "data/archive/data.pkl"


def ensure_save_dir_exists():
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)


def save_data(df: pd.DataFrame):
    ensure_save_dir_exists()
    with open(SAVE_PATH, 'wb') as f:
        pickle.dump(df, f)
    logger.info("Saved data: %d rows", len(df))


def load_data() -> pd.DataFrame:
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, 'rb') as f:
            logger.info("Loaded existing data file.")
            return pickle.load(f)
    logger.info("No existing data file found.")
    return pd.DataFrame()


def update_and_save_data(new_df: pd.DataFrame) -> pd.DataFrame:
    old_df = load_data()
    combined_df = pd.concat([old_df, new_df], ignore_index=True).drop_duplicates()
    save_data(combined_df)
    logger.info("Updated and saved combined data.")
    return combined_df
