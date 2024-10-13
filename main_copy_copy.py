from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
import random
from tweet_class import Tweet
import re
from collections import deque 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# Set the path to the web driver executable
options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

## Permet de rester connecter
options.add_argument("--user-data-dir=/home/seluser/twitter_scraper/selenium")
options.add_argument("--window-size=900,700")
chrome = webdriver.Chrome(options=options)


ACCOUNT_NAME = "RER_A"
SINCE_DATE = "2024-01-01"
TO_DATE = datetime.now().strftime("%Y-%m-%d")

df = pd.DataFrame(columns=['tweet_id', 'tweet_type', 'time_posted', 'content', 'associated_tweet_id', 'comments', 'retweets', 'likes', 'views', 'extraction_date'])
NB_ROW = 0
ALREADY_DONE_DATES = set()
#URL= f'https://x.com/search?f=live&q=(from%3A{ACCOUNT_NAME})%20until%3A{TO_DATE}%20since%3A{SINCE_DATE}&src=typed_query'
URL = f'https://x.com/search?f=live&q=(from%3A{ACCOUNT_NAME})%20until%3A{TO_DATE}%20since%3A{SINCE_DATE}%20-filter%3Areplies&src=typed_query'
TWEET_ID_ORDER = deque(maxlen=100)
TWEET_TYPE_ORDER = deque(maxlen=100)

now = datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
FILENAME = f'test_{date_string}.csv'



def wait_for_connexion(url, max_nb_try=5):
    chrome.get(url)

    current_nb_try = 0
    while True:

        if current_nb_try >= max_nb_try:
            print("Max number of try reached")
            return False
        try:
            # Replace 'element' with the actual element you want to check
            chrome.find_element('xpath', '//button[@aria-label="Menu du compte"]')
            chrome.find_element('xpath', '//div[@role="presentation"]')
            print("Seems to be connected")
            break
        except Exception as e:
            print("Waiting for user to log in...")
            current_nb_try += 1
            time.sleep(5)
    return True

def scrap_page_unitl_date(delay=5):
    while True:
        try:
            text_to_search = chrome.find_element('xpath', "//*[contains(text(), 'Essayez de recharger la page.')]")
            spans = chrome.find_elements('xpath', "//*[contains(text(), 'Réessayer')]")
            spans[0].click()
        except:
            pass
        time.sleep(delay + random.randint(1, 3))
        try:
            last_date = scrap_page()
        except Exception as e:
            print("Error while scrapping page")
            print(e)
            continue

        if last_date < datetime.strptime(SINCE_DATE, "%Y-%m-%d"):
            break
        else:
            print("Continue scrolling")
            #chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            chrome.execute_script("window.scrollBy(0, 900);")


def scrap_tweet(tweet, type):
    tweet_item = Tweet()
    elements = tweet.find_elements('xpath', './div/div/div')
    content = elements[-1].find_elements('xpath', './div[2]/div')
    header = content[0]
    content_tweet = content[1]
    stats = content[2]
    all_stats = stats.find_elements('xpath', './div/div/div') 
    try:
        tweet_text_div = content_tweet.find_elements('xpath', './/div[@data-testid="tweetText"]')[0]
        div_id = tweet_text_div.get_attribute('id')
        TWEET_ID_ORDER.append(div_id)
    except:
        print("Tweet with no texte, skip")
        return -1
    
    try:
        time_posted = header.find_element('xpath', './/time').get_attribute('datetime')
    except Exception:
        time_posted = tweet.find_element('xpath', './/time').get_attribute('datetime')
    time_posted_conv = datetime.strptime(time_posted, "%Y-%m-%dT%H:%M:%S.%fZ")

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
    tweet_item.type = type
    tweet_item.time_posted = time_posted_conv
    tweet_item.content = content_tweet.text  

    return tweet_item


def scrap_page():
    global NB_ROW

    tweets_on_page = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')

    for tweet in tweets_on_page:

        tweet_time = scrap_tweet(tweet, 'Normal')
        time_posted_conv = tweet_time.time_posted

        if time_posted_conv in ALREADY_DONE_DATES:
            print("Already done")
            continue
        else:
            ALREADY_DONE_DATES.add(time_posted_conv)

        df.loc[NB_ROW] = tweet_item.to_dict()
        NB_ROW += 1

        ActionChains(chrome).key_down(Keys.CONTROL).click(tweet).key_up(Keys.CONTROL).perform()
        chrome.switch_to.window(chrome.window_handles[-1])
        print("Loading")
        time.sleep(4)

        
        subtweets = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')
        for subtweet in subtweets:
            elements = subtweet.find_elements('xpath', './div/div/div')
            content = elements[-1].find_elements('xpath', './div[2]/div')
            header = content[0]

            if ACCOUNT_NAME in header.text:
                print("Réponse intéressante")
            else:
                print('Plus de réponses intéressante...')
                break

            subtweet_item = scrap_tweet(subtweet, 'Réponse')
        
            df.loc[NB_ROW] = subtweet_item.to_dict()
            NB_ROW += 1

        print("Before sleeping")
        time.sleep(1)

        
        # Close the new tab
        chrome.close()

        # Switch back to the original tab
        chrome.switch_to.window(chrome.window_handles[0])

        df.to_csv(FILENAME, index=False)



        break
        print("---------")
        
    return list(ALREADY_DONE_DATES)[-1]



wait_for_connexion(URL)
#scrap_pages(10, 5)
scrap_page_unitl_date(3)
#chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
df.to_csv(FILENAME, index=False)
chrome.quit()
