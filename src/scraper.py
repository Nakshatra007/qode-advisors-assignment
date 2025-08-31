# src/scraper.py

import logging
import random
import time
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from config import SEARCH_QUERY, TARGET_TWEET_COUNT, HEADLESS_MODE, SCRAPING_TIMEOUT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AUTH_STATE_FILE = "auth_state.json"

def scrape_tweets():
    """
    Scrapes tweets by mimicking human behavior: navigating to the homepage,
    using the search bar, and clicking the 'Latest' tab.
    """
    if not os.path.exists(AUTH_STATE_FILE):
        logging.error(f"Authentication file '{AUTH_STATE_FILE}' not found.")
        logging.error("Please run 'python login_setup.py' first to log in and create the file.")
        return []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS_MODE)
        context = browser.new_context(storage_state=AUTH_STATE_FILE)
        page = context.new_page()
        
        try:
            logging.info("Navigating to the Twitter/X homepage.")
            page.goto("https://x.com/", timeout=SCRAPING_TIMEOUT)

            search_box_selector = 'input[data-testid="SearchBox_Search_Input"]'
            logging.info("Waiting for the search input box to appear.")
            page.wait_for_selector(search_box_selector, timeout=15000)
            
            logging.info(f"Typing search query: '{SEARCH_QUERY}'")
            page.fill(search_box_selector, SEARCH_QUERY)
            page.press(search_box_selector, 'Enter')

            # --- UPDATED AND MORE ROBUST SELECTOR FOR 'LATEST' TAB ---
            # We are now looking for a clickable tab element that has the text "Latest".
            # This is much more resilient to website changes.
            latest_tab_selector = 'a[role="tab"]:has-text("Latest")'
            logging.info("Waiting for the 'Latest' tab on the search results page.")
            # Increased timeout to 30 seconds to handle slower page loads.
            page.wait_for_selector(latest_tab_selector, timeout=30000)
            page.click(latest_tab_selector)
            logging.info("Clicked the 'Latest' tab to get real-time tweets.")
            
        except PlaywrightTimeoutError as e:
            logging.error(f"A timeout occurred during the navigation/search phase: {e}")
            browser.close()
            return []

        scraped_tweets = []
        tweet_ids = set()
        logging.info(f"Starting to scrape for {TARGET_TWEET_COUNT} tweets...")
        
        last_height = page.evaluate('document.body.scrollHeight')
        
        while len(scraped_tweets) < TARGET_TWEET_COUNT:
            try:
                page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
                articles = page.query_selector_all('article[data-testid="tweet"]')
                
                for article in articles[-15:]:
                    tweet_data = parse_tweet(article)
                    if tweet_data and tweet_data['tweet_id'] not in tweet_ids:
                        tweet_ids.add(tweet_data['tweet_id'])
                        scraped_tweets.append(tweet_data)

                logging.info(f"Scraped {len(scraped_tweets)} / {TARGET_TWEET_COUNT} unique tweets.")

                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(random.uniform(2, 4))
                
                new_height = page.evaluate('document.body.scrollHeight')
                if new_height == last_height:
                    logging.warning("Scrolled to the bottom of the page. No more tweets to load.")
                    break
                last_height = new_height

            except PlaywrightTimeoutError:
                logging.warning("Reached timeout waiting for new tweets. This may be the end of the results.")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred during scraping: {e}")
                break

        browser.close()
        logging.info(f"Finished scraping. Total unique tweets collected: {len(scraped_tweets)}")
        return scraped_tweets

def parse_tweet(article):
    """
    Parses a single tweet article element to extract required information.
    """
    try:
        permalink_element = article.query_selector('a[href*="/status/"]')
        if not permalink_element: return None
            
        href = permalink_element.get_attribute('href')
        tweet_id = href.split('/')[-1]

        username = article.query_selector('div[data-testid="User-Name"] span').inner_text()
        timestamp = article.query_selector('time').get_attribute('datetime')
        
        content_element = article.query_selector('div[data-testid="tweetText"]')
        content = content_element.inner_text() if content_element else ""
        
        replies = get_engagement_metric(article, 'reply')
        retweets = get_engagement_metric(article, 'retweet')
        likes = get_engagement_metric(article, 'like')

        hashtags = [el.inner_text() for el in article.query_selector_all('a[href*="/hashtag/"]')]
        mentions = [el.inner_text() for el in article.query_selector_all('a[href*="/"][dir="ltr"]') if el.inner_text().startswith('@')]

        return {
            'tweet_id': tweet_id,
            'username': username,
            'timestamp': timestamp,
            'content': content,
            'engagement_replies': replies,
            'engagement_retweets': retweets,
            'engagement_likes': likes,
            'hashtags': hashtags,
            'mentions': mentions
        }
    except Exception:
        # It's common for some elements not to parse (e.g., ads, deleted tweets), so we return None.
        return None

def get_engagement_metric(article, metric_type):
    """
    Extracts engagement metrics (replies, retweets, likes) which can be in 'K' or 'M' format.
    """
    try:
        selector = f'div[data-testid="{metric_type}"] span[data-testid="app-text-transition-container"]'
        element = article.query_selector(selector)
        text = element.inner_text().strip() if element else '0'
        
        if 'K' in text:
            return int(float(text.replace('K', '')) * 1000)
        elif 'M' in text:
            return int(float(text.replace('M', '')) * 1000000)
        else:
            return int(text) if text else 0
    except (ValueError, TypeError):
        return 0