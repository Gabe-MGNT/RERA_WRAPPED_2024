from scraper import TweetScraper 
from datetime import datetime
import pandas as pd
ACCOUNT_NAME = "RER_A"
SINCE_DATE = "2024-01-01"

#TO_DATE = datetime.now().strftime("%Y-%m-%d")
TO_DATE = "2024-10-24"

df_tweets = pd.read_csv("data/part1.csv")
df_tweets['time_posted'] = pd.to_datetime(df_tweets['time_posted'], format="%Y-%m-%d %H:%M:%S")
last_date = df_tweets["time_posted"].iloc[-1]
last_date.strftime("%Y-%m-%d")
TO_DATE = last_date 


df_tweets = pd.read_csv("part1.csv")
last_date = df_tweets["time_posted"].iloc[-1]

scraper = TweetScraper(ACCOUNT_NAME, SINCE_DATE, TO_DATE)
scraper.scrap_page_unitl_end_date()

