import time
from playwright.sync_api import sync_playwright

def run_login_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://twitter.com/login")
        print("\n" + "="*50)
        print("Please log in to your Twitter/X account in the browser window.")
        print("After you have successfully logged in, press Enter in this terminal.")
        print("="*50 + "\n")
        input()
        storage_state_path = "auth_state.json"
        context.storage_state(path=storage_state_path)
        print(f"Authentication state successfully saved to '{storage_state_path}'")
        print("You can now close the browser window and run the main.py script.")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run_login_setup()