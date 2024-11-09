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
import uuid
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
REGEX_GET_NUMBER = re.compile(r'\d+')

class TweetScraper:
    def __init__(self, account_name, begin_date, end_date):
        self.account_name = account_name
        self.begin_date = begin_date
        self.end_date = end_date
        self.chrome = None
        self.df = pd.DataFrame(columns=['tweet_id', 'tweet_type', 'time_posted', 'content', 'thread_id', 'comments', 'retweets', 'likes', 'views', 'extraction_date'])
        self.nb_row = 0
        self.already_done_set = set()

        self.tweet_id_order = deque(maxlen=100)
        self.tweet_type_order = deque(maxlen=100)

        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f'test_{date_string}.csv'

        self.url_to_scrape = f'https://x.com/search?f=live&q=(from%3A{self.account_name})%20until%3A{self.end_date}%20since%3A{self.begin_date}%20-filter%3Areplies&src=typed_query'


    
    def _set_argument(self, data_dir="/home/seluser/twitter_scraper/selenium", window_width=900, window_height=700):
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_experimental_option("detach", True)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(f"--user-data-dir={data_dir}")
        options.add_argument(f"--window-size={window_width},{window_height}")
        return options

    def _init_webdriver(self):
        options = self._set_argument()
        chrome = webdriver.Chrome(options=options)
        return chrome

    def _init_scraping_process(self):
        logging.info("Init webdriver")
        chrome = self._init_webdriver()

        if not self.wait_for_connexion(chrome, self.url_to_scrape):
            chrome.quit()
            raise Exception("User not connected")
        return chrome
        

    def scrap_page_unitl_end_date(self, delay_between_page=5):
        chrome = self._init_scraping_process()
        logging.infoé("Begin scraping process")


        while True:

            # Check if the page need to be reloaded
            try:
                text_to_search = chrome.find_element('xpath', "//*[contains(text(), 'Essayez de recharger la page.')]")
                spans = chrome.find_elements('xpath', "//*[contains(text(), 'Réessayer')]")
                spans[0].click()
            except:
                pass

            # Attendre que la page charge
            logging.info("wait for loading next page")
            time.sleep(delay_between_page + random.randint(1, 3))
            logging.debug("scrap page")

            # Recupère tous les tweet (et thread) de la page
            try:
                last_date = self.scrap_page(chrome)
            except Exception as e:
                logging.error("Error while scrapping page")
                logging.error(e)
                raise(e)

            # Si la date du dernier tweet est inférieur à la date de début, alors on arrête le scrapping
            # Sinon scroll sur la page
            if last_date < datetime.strptime(self.begin_date, "%Y-%m-%d"):
                logging.info("Reached end date")
                break
            else:
                logging.debug("Continue scrapping, scrolling page")
                chrome.execute_script("window.scrollBy(0, 900);")

    def wait_for_connexion(self, chrome, url, max_nb_try=5, delay=30):
        logging.debug("Checking if user is connected...")
        chrome.get(url)

        time.sleep(5)

        current_nb_try = 0
        while True:
            if current_nb_try >= max_nb_try:
                logging.error("Max number of try reached to check user connected")
                return False
            try:
                chrome.find_element('xpath', '//button[@aria-label="Menu du compte"]')
                chrome.find_element('xpath', '//div[@role="presentation"]')
                logging.info("User is connected")
                break
            except Exception as e:
                logging.debug("User is not connected, waiting for 5 seconds before next check")
                current_nb_try += 1
                time.sleep(delay)
        return True


    def scrap_page(self, chrome, delay_between_tweet=3, delay_before_closing_tab=2):

        tweets_on_page = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')

        for tweet in tweets_on_page:

            thread_id = str(uuid.uuid4())

            try:
                tweet_item = self.scrap_tweet(tweet, 'Normal')
            except Exception as e:
                logging.error("Error while scrapping main tweet")
                logging.error(e)
                raise e
            tweet_item.thread_id = thread_id
            time_posted_conv = tweet_item.time_posted

            if time_posted_conv in self.already_done_set:
                logging.info("Already done")
                continue
            else:
                logging.info("New tweet to scrap")
                self.already_done_set.add(time_posted_conv)

            self.df.loc[self.nb_row] = tweet_item.to_dict()
            self.nb_row += 1

            ActionChains(chrome).key_down(Keys.CONTROL).click(tweet).key_up(Keys.CONTROL).perform()
            chrome.switch_to.window(chrome.window_handles[-1])

            logging.info("Loading thread")
            time.sleep(delay_between_tweet + random.randint(1, 3))

            try:
                self._scrap_thread(chrome, thread_id)
            except Exception as e:
                logging.error("Error while scrapping thread")
                logging.error(e)
                raise e

            logging.info("Thread scrapper, waiting before closing tab")
            time.sleep(delay_before_closing_tab + random.randint(1, 3))
            
            
            self.df.to_csv(self.filename, index=False)
            
            # Close the new tab
            chrome.close()

            # Switch back to the original tab
            chrome.switch_to.window(chrome.window_handles[0]) 
        return list(self.already_done_set)[-1]


    def _scrap_thread(self, chrome, thread_id):
        subtweets = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')
        for index, subtweet in enumerate(subtweets[1:]):

                last_thread_tweet = subtweet.find_elements('xpath', '../../../div/div/div//text()')
                    

                elements = subtweet.find_elements('xpath', './div/div/div')
                content = elements[-1].find_elements('xpath', './div[2]/div')
                header = content[0]

                if self.account_name in header.text:
                    logging.info("Réponse intéressante")
                else:
                    logging.info('Plus de réponses intéressante...')
                    return

                try:
                    subtweet_item = self.scrap_tweet(subtweet, 'Réponse')
                except Exception as e:
                    logging.error("Error while scrapping subtweet")
                    logging.error(e)
                    raise(e)
                subtweet_item.thread_id = thread_id
            
                self.df.loc[self.nb_row] = subtweet_item.to_dict()
                self.nb_row += 1

                if last_thread_tweet == "" or index == len(subtweets) - 1:
                    logging.debug("Last tweet of the thread")
                    return

    def scrap_tweet(self, tweet, type):
        tweet_item = Tweet()
        elements = tweet.find_elements('xpath', './div/div/div')

        content = elements[-1].find_elements('xpath', './div[2]/div')
        header = content[0]
        content_tweet = content[1]

        try:
            # Si le tweet contient un tweet cité, alors mettre la date du tweet cité
            date_cited_tweet = content[2].find_elements('xpath','.//time')[0].get_attribute('datetime')
            time_posted_conv = datetime.strptime(date_cited_tweet, "%Y-%m-%dT%H:%M:%S.%fZ")
            tweet_item.type = type
            tweet_item.time_posted = self._get_tweet_posted_time(header)
            tweet_item.content = f"Citation du tweet du {time_posted_conv}"  
            comment, retweet, like, views = self._get_tweet_stats(content[-1])
            tweet_item.comment = comment
            tweet_item.retweet = retweet
            tweet_item.like = like
            tweet_item.views = views
            return tweet_item 
        except Exception as e:
            print("Tweet contains normal text")
            pass

        time_posted_conv = self._get_tweet_posted_time(header)
        comment, retweet, like, views = self._get_tweet_stats(content[-1])
        
        tweet_item.type = type
        tweet_item.time_posted = time_posted_conv
        tweet_item.content = content_tweet.text  
        tweet_item.comment = comment
        tweet_item.retweet = retweet
        tweet_item.like = like
        tweet_item.views = views
        return tweet_item
    

    def _get_tweet_stats(self, stats):

        all_stats = stats.find_elements('xpath', './div/div/div')

        comment = all_stats[0].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if REGEX_GET_NUMBER.search(comment):
            #tweet_item.comment = int(REGEX_GET_NUMBER.search(comment).group())
            comment = int(REGEX_GET_NUMBER.search(comment).group())

        retweet = all_stats[1].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if REGEX_GET_NUMBER.search(retweet):
            #tweet_item.retweet = int(REGEX_GET_NUMBER.search(retweet).group())
            retweet = int(REGEX_GET_NUMBER.search(retweet).group())

        like = all_stats[2].find_elements('xpath', './button')[0].get_attribute('aria-label')
        if REGEX_GET_NUMBER.search(like):
            #weet_item.like = int(REGEX_GET_NUMBER.search(like).group())
            like = int(REGEX_GET_NUMBER.search(like).group())
        views = all_stats[3].find_elements('xpath', './a')[0].get_attribute('aria-label')
        if REGEX_GET_NUMBER.search(views):
            #tweet_item.views = int(REGEX_GET_NUMBER.search(views).group())
            views = int(REGEX_GET_NUMBER.search(views).group())

        return comment, retweet, like, views

    def _get_tweet_posted_time(self, header):
        time_posted = header.find_element('xpath', './/time').get_attribute('datetime')
        time_posted_conv = datetime.strptime(time_posted, "%Y-%m-%dT%H:%M:%S.%fZ")
        return time_posted_conv