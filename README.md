# Real-Time Market Intelligence System

## Project Overview

This project is a data collection and analysis system designed to gather real-time market intelligence from Twitter/X. It scrapes tweets related to Indian stock market discussions, processes the data, performs sentiment analysis to generate trading signals, and visualizes the results.

This system is built as a response to the Technical Assignment for a Software Developer Position at Qode Advisors LLP.

## Features

- **Data Collection**: Scrapes Twitter/X for tweets containing specified hashtags (`#nifty50`, `#sensex`, etc.) without using paid APIs.
- **Robust Scraping**: Uses Playwright for browser automation to handle dynamic content, infinite scrolling, and anti-bot measures.
- **Data Processing**: Cleans and normalizes raw tweet data, handles Unicode, and removes duplicates.
- **Efficient Storage**: Saves the processed data in the efficient Parquet format.
- **Analysis & Insights**: Converts textual data into quantitative signals using VADER for sentiment analysis.
- **Visualization**: Generates a time-series plot of the aggregated market sentiment.
- **Production-Ready**: Features modular code, configuration management, logging, and error handling.

## Project Structure

qode-advisors-assignment/
│
├── .gitignore
├── README.md # You are here
├── requirements.txt # Project dependencies
│
├── config.py # Central configuration for hashtags, file paths, etc.
├── login_setup.py # One-time script to create the authentication file
├── main.py # Main script to run the entire data pipeline
│
└─── src/
├── init.py
├── scraper.py # The core web scraping logic using Playwright
├── data_processor.py # Data cleaning, normalization, and transformation
└── analysis.py # Sentiment analysis and plot generation


---

## How to Run This Project

### Prerequisites

- Python 3.8+
- A throwaway ("burner") Twitter/X account for the one-time login. **It is strongly recommended not to use a personal account.**

### Step 1: Clone the Repository

```bash
git clone <your_repository_url>
cd qode-advisors-assignment
```
Step 2: Set Up the Virtual Environment (Optional)

Step 3: Install Dependencies
Install all the required Python libraries and the necessary browser binaries for Playwright.

# Install Python packages
```
pip install -r requirements.txt
```
# Download browser binaries for Playwright (one-time setup)
```
playwright install
```

Step 4: One-Time Authentication Setup
This step creates the auth_state.json file that allows the scraper to run as a logged-in user. You only need to do this once.
Run the login setup script:
```
python login_setup.py
```
A Chromium browser window will open to the Twitter/X login page.
Log in using your burner account credentials.
Once you are successfully logged in, return to your terminal and press the Enter key.
The script will save the session state to auth_state.json and close.


Step 5: Execute the Main Data Pipeline
You are now ready to run the entire project.
```
python main.py
```
The script will perform the following actions:
1. Launch a browser in the background (headless mode).
2. Use the saved authentication state to log in.
3. Navigate, search, and scrape the latest tweets.
4. Process and save the data to data/tweets.parquet.
5. Generate a sentiment analysis plot and save it to data/market_sentiment_analysis.png.
6. The output files will be located in the data/ directory.
   <img width="1500" height="700" alt="image" src="https://github.com/user-attachments/assets/cc7f9271-a48f-48f0-9c72-28c7b28545fa" />

