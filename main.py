# main.py

import logging
import os
import pandas as pd

from src.scraper import scrape_tweets
from src.data_processor import process_data
from src.analysis import perform_analysis
from config import PARQUET_FILE_PATH, OUTPUT_DATA_DIR

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def main():
    """
    Main function to run the end-to-end data pipeline.
    """
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)
        logging.info(f"Created directory: {OUTPUT_DATA_DIR}")

    # --- 1. Data Collection ---
    logging.info("Starting Step 1: Data Collection")
    raw_tweets = scrape_tweets()
    if not raw_tweets:
        logging.error("Scraping returned no data. Exiting pipeline.")
        return

    # --- 2. Data Processing & Storage ---
    logging.info("Starting Step 2: Data Processing")
    processed_df = process_data(raw_tweets)

    if not processed_df.empty:
        try:
            processed_df.to_parquet(PARQUET_FILE_PATH, engine='pyarrow', index=False)
            logging.info(f"Data successfully saved to {PARQUET_FILE_PATH}")
        except Exception as e:
            logging.error(f"Failed to save data to Parquet file: {e}")
            return
    else:
        logging.warning("Processed DataFrame is empty. Nothing to save or analyze.")
        return

    # --- 3. Analysis & Insights ---
    logging.info("Starting Step 3: Analysis & Insights")
    # Read from the saved file to simulate a real pipeline
    df_for_analysis = pd.read_parquet(PARQUET_FILE_PATH)
    perform_analysis(df_for_analysis)
    
    logging.info("Pipeline executed successfully.")


if __name__ == "__main__":
    main()