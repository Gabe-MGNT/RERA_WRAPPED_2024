from scraper import TweetScraper 
from datetime import datetime

ACCOUNT_NAME = "RER_A"
SINCE_DATE = "2024-01-01"

#TO_DATE = datetime.now().strftime("%Y-%m-%d")
TO_DATE = "2024-10-24"

scraper = TweetScraper(ACCOUNT_NAME, SINCE_DATE, TO_DATE)
scraper.scrap_page_unitl_end_date()

