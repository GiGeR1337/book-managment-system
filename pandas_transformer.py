import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how="all")
    logger.debug("Dropped all-NaN rows: shape %s", df.shape)

    df.columns = [col.lower() for col in df.columns]
    logger.debug("Standardized column names.")

    df = df.drop(columns=[col for col in df.columns if "internal" in col.lower()], errors='ignore')
    logger.debug("Dropped internal columns if present.")

    if 'name' in df.columns and 'surname' in df.columns and 'author' not in df.columns:
        df['author'] = df['name'].astype(str).str.strip() + ' ' + df['surname'].astype(str).str.strip()
        logger.info("Created 'author' column from 'name' and 'surname'.")

    if 'author' in df.columns:
        df['author'] = df['author'].astype(str).str.title()
        logger.debug("Standardized author names.")

    if 'publisher' in df.columns and 'author' in df.columns:
        original_shape = df.shape
        df = df[
            df['publisher'].str.contains("Penguin Random House|Random House", case=False, na=False) |
            df['author'].str.contains("Stephen King", case=False, na=False)
            ]
        logger.info("Filtered publishers and authors: %s -> %s", original_shape, df.shape)

    df = df[~df.astype(str).apply(lambda row: row.str.contains(r'[\u4e00-\u9fff]').any(), axis=1)]
    logger.debug("Removed rows containing Chinese characters.")

    df = df.drop_duplicates()
    logger.info("Dropped duplicates: final shape %s", df.shape)

    return df
