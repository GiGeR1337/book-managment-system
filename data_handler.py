import logging
import os
import re
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def is_valid_file(filename: str, patterns: list[str]) -> bool:
    return any(re.fullmatch(p, filename) for p in patterns)


def load_valid_file(folder: str, patterns: list[str]) -> Optional[pd.DataFrame]:
    valid_files = []
    logger.info("Checking files in folder: %s", folder)

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        if is_valid_file(file, patterns):
            logger.info("Valid file found: %s", file)
            valid_files.append(file_path)
        else:
            logger.warning("Deleting invalid file: %s", file)
            os.remove(file_path)

    for file_path in valid_files:
        try:
            if file_path.endswith(".xlsx"):
                return pd.read_excel(file_path)
            elif file_path.endswith(".csv"):
                return pd.read_csv(file_path)
        except Exception as e:
            logger.error("Failed to load file %s: %s", file_path, e)

    return None
