import json

from logger_config import *
from data_handler import load_valid_file
from pandas_transformer import clean_dataframe
from additional_data_fetcher import enrich_books
from data_persistence import update_and_save_data

logger = logging.getLogger(__name__)


def main():
    with open("config.json") as f:
        config = json.load(f)
        logger.info("Loaded configuration.")

    df = load_valid_file(config["data_folder"], config["acceptable_formats"])
    if df is not None:
        df = clean_dataframe(df)
        df = enrich_books(df)
        df = update_and_save_data(df)
        logger.info("Data processed and saved successfully.")
    else:
        logger.warning("No valid files found.")


if __name__ == "__main__":
    main()
