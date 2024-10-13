from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
import random
from tweet_class import Tweet
import re

# Set the path to the web driver executable
options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_experimental_option("detach", True)

## Permet de rester connecter
options.add_argument("--user-data-dir=/home/seluser/twitter_scraper/selenium")
options.add_argument("--window-size=900,700")
chrome = webdriver.Chrome(options=options)


TWITTER_URL_ACCOUNT = "https://x.com/RER_A"


df = pd.DataFrame(columns=['tweet_id', 'tweet_type', 'time_posted', 'content', 'associated_tweet_id', 'comments', 'retweets', 'likes', 'views', 'extraction_date'])
NB_ROW = 0
already_done_dates = set()


# Navigate to the website
chrome.get(TWITTER_URL_ACCOUNT)


## Wait to connect to twitter
while True:
    try:
        # Replace 'element' with the actual element you want to check
        chrome.find_element('xpath', '//button[@aria-label="Menu du compte"]')
        chrome.find_element('xpath', '//div[@role="presentation"]')
        print("Seems to be connected")
        break
    except Exception as e:
        print("Waiting for user to log in...")
        time.sleep(5)



def scrap_pages(nb_scrolls=None, delay=5, to_date=None):

    if to_date:
        print("The number of scrolls will not be taken into account as the to_date is not null")
        to_date_converted = datetime.strptime(to_date, "%Y-%m-%d")
        while True:
            #chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Waiting loading")
            time.sleep(delay + random.uniform(-2, 2))
            oldest_tweet_date = scrap_page()
            chrome.execute_script("window.scrollBy(0, 900);")
            time.sleep(delay + random.uniform(-2, 2))

            if oldest_tweet_date < to_date_converted:
                print("Date reached, scraping will stop")
                break
            print("Current oldest date :", oldest_tweet_date)
    else:
        for i in range(nb_scrolls):
            if i==0:
                time.sleep(delay + random.uniform(-2, 2))
            else:
                #chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                chrome.execute_script("window.scrollBy(0, 900);")
                time.sleep(delay + random.uniform(-2, 2))
            print("Waiting loading")
            time.sleep(delay + random.uniform(-2, 2))
            scrap_page()



from collections import deque 


tweet_id_order = deque(maxlen=100)
tweet_type_order = deque(maxlen=100)
    

def scrap_page():
    global NB_ROW

    tweets_on_page = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')

    for tweet in tweets_on_page:

        tweet_item = Tweet()
        
        elements = tweet.find_elements('xpath', './div/div/div')

        content = elements[-1].find_elements('xpath', './div[2]/div')

        try:
            tweet_text_div = content[1].find_elements('xpath', './/div[@data-testid="tweetText"]')[0]
        except Exception as e:
            print("Error while getting tweet text")
            print(content[1].text)
            continue
        div_id = tweet_text_div.get_attribute('id')
        tweet_id_order.append(div_id)

        header = content[0]
        time_posted = header.find_element('xpath', './/time').get_attribute('datetime')
        time_posted_conv = datetime.strptime(time_posted, "%Y-%m-%dT%H:%M:%S.%fZ")


        if time_posted_conv in already_done_dates:
            print("Already done")
            continue
        else:
            already_done_dates.add(time_posted_conv)

        balise = elements[0].text
        balise_with_divs = elements[0].find_elements('xpath', './/div')


        if balise == "Épinglé":
            tweet_item.type = "Epinglé"
            tweet_type_order.append("epingle")
        elif "a reposté" in balise:
            tweet_item.type = "Repost"
            tweet_type_order.append("repost")
        elif len(balise_with_divs) == 2:
            tweet_item.type = 'Normal'
            tweet_type_order.append("normal")
        elif len(balise_with_divs) > 2:
            tweet_item.type = 'Réponse'
            last_normal_index = max(idx for idx, val in enumerate(tweet_type_order) if val == 'normal')
            main_tweet = tweet_id_order[last_normal_index] 
            tweet_item.main_tweet = main_tweet
            tweet_type_order.append("reponse")
                


        content_tweet = content[1]
        stats = content[-1]

        all_stats = stats.find_elements('xpath', './div/div/div')   


        get_number_re = re.compile(r'\d+')

        comment = all_stats[0].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if get_number_re.search(comment):
            tweet_item.comment = int(get_number_re.search(comment).group())
        
        retweet = all_stats[1].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if get_number_re.search(retweet):
            tweet_item.retweet = int(get_number_re.search(retweet).group())

        like = all_stats[2].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if get_number_re.search(like):
            tweet_item.like = int(get_number_re.search(like).group())

        views = all_stats[3].find_elements('xpath', './a')[0].get_attribute('aria-label')
        if get_number_re.search(views):
            tweet_item.views = int(get_number_re.search(views).group())
 


        tweet_item.tweet_id = div_id
        tweet_item.time_posted = time_posted_conv
        tweet_item.content = content_tweet.text


        df.loc[NB_ROW] = tweet_item.to_dict()
        NB_ROW += 1
        print("---------")
        
    return time_posted_conv

now = datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
file_name = f'test_{date_string}.csv'

scrap_pages(10, 5, "2024-01-01")
#scrap_pages(10, 5)
#chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
df.to_csv(file_name, index=False)
chrome.quit()
