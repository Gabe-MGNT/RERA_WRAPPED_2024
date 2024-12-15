from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
import random
from tweet_class import Tweet
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
REGEX_GET_NUMBER = re.compile(r'\d+')

class TweetScraper:
    """
    Class to scrap tweets from a Twitter account between two dates and return results in csv file
    Request made to Twiter only use user's tweet and not retweet or replies
    """
    def __init__(self, account_name, begin_date, end_date):
        self.account_name = account_name
        self.begin_date = begin_date
        self.end_date = end_date
        self.chrome = None
        self.df = pd.DataFrame(columns=['tweet_type', 'time_posted', 'content', 'thread_id', 'comments', 'retweets', 'likes', 'views', 'extraction_date'])
        self.nb_row = 0
        self.already_done_set = set()
        self.already_done_set_with_threadid = {}
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f'data/test_{date_string}.csv'
        self.url_to_scrape = f'https://x.com/search?f=live&q=(from%3A{self.account_name})+(to%3A{self.account_name})%20until%3A{self.end_date}%20since%3A{self.begin_date}&src=typed_query'
        #self.url_to_scrape = "https://x.com/search?f=live&q=(from%3ARER_A)%20(to%3ARER_A)%20until%3A2024-10-24&src=typed_query"

    def _set_argument(self, data_dir="/home/seluser/twitter_scraper/selenium", window_width=900, window_height=700):
        """
        Set the argument for the webdriver
        Args:
            data_dir (str): Path to the directory where the user data will be stored (allow to keep the user connected to Twitter between multiple executions)
            window_width (int): Control the window width for selenium
            window_height (int): Control the window height for selenium

        Returns:
            options (Options): Return the options to be used by the webdriver
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_experimental_option("detach", True)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(f"--user-data-dir={data_dir}")
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        options.add_argument(f"--window-size={window_width},{window_height}")
        return options

    def _init_webdriver(self):
        """
        Initialize the webdriver with the options set by the _set_argument method
        Returns:
            chrome (webdriver): Return the webdriver
        """
        options = self._set_argument()
        #chrome = webdriver.Chrome(options=options)
        chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return chrome

    def wait_for_connexion(self, chrome, url, max_nb_try=5, delay=30):
        """
        In order to scrap tweet, an account has to be connected to Twitter. This method check if the user is connected, and if not wait until the user is connected.
        The connection is checked by looking for the user's profile picture

        Args:
            chrome (webdriver): The webdriver to use
            url (str): The url to check
            max_nb_try (int): The maximum number of try before returning False and stopping the process
            delay (int): The delay between each try (has to be high enough to let the user connect)

        Returns:
            bool: True if the user is connected, False otherwise
        """
        chrome.get(url)

        time.sleep(5)

        current_nb_try = 0
        while True:
            if current_nb_try >= max_nb_try:
                return False
            try:
                # Find the user profile picture to check if the user is connected
                chrome.find_element('xpath', '//button[@aria-label="Menu du compte"]')
                chrome.find_element('xpath', '//div[@role="presentation"]')
                break
            except Exception as e:
                logging.debug(f"User is not connected, waiting for {delay} seconds before next check ({current_nb_try} try/{max_nb_try})")
                current_nb_try += 1
                time.sleep(delay)
        return True

    def _init_scraping_process(self):
        """
        Initialize the scraping process, by first setting up the webdriver and checking if the user is connected to Twitter
        Once both step are completed, scrapin process can begin otherwise an exception is raised

        Returns:
            chrome (webdriver): The webdriver to use for the scraping process
        """
        logging.info("Init webdriver")
        chrome = self._init_webdriver()
        logging.debug("Checking if user is connected...")
        if not self.wait_for_connexion(chrome, self.url_to_scrape):
            logging.error("Max number of try reached to check user connected")
            chrome.quit()
            raise Exception("User was not connected to Twitter, scrapin aborted")
        logging.info("User is connected")
        return chrome
        
    def scrap_page_unitl_end_date(self, delay_between_page=5):
        """
        Scrap all the tweet from the account between the begin_date and the end_date set in the constructor
        It first initialize the scraping process, if no error was raised then scrap all the tweet until the end date is reached
        Results are saved in a csv file eacht time data are scraped

        Sometime, the page need to be reloaded, in this case, the page is reloaded by catching the button and clicking on it

        As long as the date of the last tweet is superior to the begin_date, the page is scrolled to get more tweet

        Args:
            delay_between_page (int): The delay to wait between each page load (has to be high enough to let the page load - randomized by adding between 1 and 3 seconds)
        """
        chrome = self._init_scraping_process()
        logging.info("Begin scraping process")

        while True:
            try:
                # Reload the page if needed
                text_to_search = chrome.find_element('xpath', "//*[contains(text(), 'Essayez de recharger la page.')]")
                spans = chrome.find_elements('xpath', "//*[contains(text(), 'Réessayer')]")
                spans[0].click()
                logging.info("Had to click on reload page button")
            except:
                pass

            # Wait the page to load
            time.sleep(delay_between_page + random.randint(7, 15))

            # Retrieve all the tweets on the page
            try:
                last_date = self.scrap_page(chrome)
            except Exception as e:
                logging.error(e)
                raise(e)

            # If last tweet date is inferior to the begin date, then stop the process
            if last_date < datetime.strptime(self.begin_date, "%Y-%m-%d"):
                logging.info("Reached end date")
                break
            else:
                chrome.execute_script("window.scrollBy(0, 450);")
        logging.info("Reached end date")
        chrome.quit()

    def scrap_page(self, chrome, delay_between_tweet=3, delay_before_closing_tab=4):
        """
        Retrieve all the tweet on the page and scrap them
        By scraping tweet, it means that the tweet content, the date, the number of comment, retweet, like and views are retrieved as well as as all the subtweet (thread) if any
        Each thread is associated with an ID to link it to the main tweet
        To scrap each tweet, Selenium click on each tweet to access the thread (on a new tab) and then scrap all the tweets inside
        Results are saved each time an item in scraped

        Args:
            chrome (webdriver): The webdriver to use
            delay_between_tweet (int): The delay to wait between each tweet scrapping (has to be high enough to let the page load - randomized by adding between 1 and 3 seconds)
            delay_before_closing_tab (int): The delay to wait before closing the tab (has to be high enough to let the page load - randomized by adding between 1 and 3 seconds)
        Returns:
            datetime: The date of the last tweet scrapped
        """

        tweets_on_page = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')

        main_page = chrome.window_handles[0]
        for tweet in tweets_on_page:


            thread_id = str(uuid.uuid4())

            # Scrap the main tweet informations
            tweet_item = self.scrap_tweet(tweet, 'Réponse')

            
            tweet_item.thread_id = thread_id
            time_posted_conv = tweet_item.time_posted

            print(time_posted_conv)
            print(time_posted_conv in self.already_done_set)
            # Check if the tweet has already been scrapped
            if time_posted_conv in self.already_done_set:
                continue
            self.already_done_set.add(time_posted_conv)



            # Click sur le tweet si adresse est sur X sinon rien
            # Click on the tweet to access the thread
            try:
                """
                tweetContent = tweet.find_element('xpath', './/div[@data-testid="tweetText"]')
                ActionChains(chrome).key_down(Keys.CONTROL).click(tweetContent).key_up(Keys.CONTROL).perform()
                chrome.switch_to.window(chrome.window_handles[-1])
                """
                """
                tweetProfile = tweet.find_element("xpath", './/div[@data-testid="Tweet-User-Avatar"]')
                actions = ActionChains(chrome).key_down(Keys.CONTROL)
                actions.move_to_element_with_offset(tweetProfile, 0, 40)  # Déplacement de 20 pixels vers le bas
                actions.click().key_up(Keys.CONTROL).perform()  # Cliquer à cet endroit
                chrome.switch_to.window(chrome.window_handles[-1])
                """
                tweetThreadLink = tweet.find_element("xpath", './/a[contains(@href, "/status/")]')
                ActionChains(chrome).key_down(Keys.CONTROL).click(tweetThreadLink).key_up(Keys.CONTROL).perform()
                #chrome.click(tweetThreadLink).perform()
                #tweetThreadLink.click()  
                chrome.switch_to.window(chrome.window_handles[-1])  
            except:
                continue

            time.sleep(delay_between_tweet + random.randint(7, 15))

            # Scrap the thread
            try:
                res = self._scrap_thread(chrome, thread_id)
                if res != 0:
                    tweet_item.thread_id = res
            except Exception as e:
                logging.error("Error while scrapping thread")
                #chrome.close()  
                #chrome.switch_to.window(main_page) 
                chrome.back()
                raise e
            

            self.already_done_set_with_threadid[time_posted_conv] = tweet_item.thread_id
            self.df.loc[self.nb_row] = tweet_item.to_dict()
            self.nb_row += 1

            #time.sleep(delay_before_closing_tab + random.randint(4, 7))
            
            self.df.to_csv(self.filename, index=False)
            
            # Close the new tab
            chrome.close()
            #time.sleep(1)
            # Switch back to the original tab
            chrome.switch_to.window(main_page) 
            #chrome.back()
            WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
            )
            time.sleep(delay_before_closing_tab + random.randint(7, 15))



        return list(self.already_done_set)[-1]


    def _scrap_thread(self, chrome, thread_id):
        """
        Scrap all the tweet in a thread belonging to the account mentioned in the constructor
        A thread is a tweet that has been replied to by other tweet

        To check if a tweet in the last from the thread it is either the last tweet of the thread or is followed by a separator
        Args:
            chrome (webdriver): The webdriver to use
            thread_id (str): The ID of the thread to link all the tweet in the thread
        
        Returns:
            None: If everything works, nothing is returned otherwise an error is raised
        """
        subtweets = chrome.find_elements('xpath', '//article[@data-testid="tweet"]')
        for index, subtweet in enumerate(subtweets):

                #last_thread_tweet = subtweet.find_elements('xpath', '../../../div/div/div//text()')
                try:
                    last_thread_tweet = subtweet.find_elements('xpath', './parent::div/parent::div/parent::div/following-sibling::div')[0]


                    elements = subtweet.find_elements('xpath', './div/div/div')
                    content = elements[-1].find_elements('xpath', './div[2]/div')
                    header = content[0]
                except:
                    continue
                
                # Check if the tweet is from the account mentioned in the constructor
                if self.account_name not in header.text:
                    return thread_id

                try:
                    if index==0:
                        subtweet_item = self.scrap_tweet(subtweet, 'Normal')
                    else:
                        subtweet_item = self.scrap_tweet(subtweet, 'Réponse')
                except Exception as e:
                    logging.error("Error while scrapping tweet in thread")
                    logging.error(f"Thread link :{chrome.current_url}, reponse index : {index}")   
                    continue
                

                if subtweet_item.time_posted in self.already_done_set:
                    thread_id =  self.already_done_set_with_threadid.get(subtweet_item.time_posted)
                    continue
                self.already_done_set.add(subtweet_item.time_posted)
                self.already_done_set_with_threadid[subtweet_item.time_posted] = thread_id
 


                subtweet_item.thread_id = thread_id
                self.df.loc[self.nb_row] = subtweet_item.to_dict()
                self.nb_row += 1
                
                #if last_thread_tweet == "" or index == len(subtweets) - 1:
                #    return
                if last_thread_tweet.text == "" or index == len(subtweets) - 1:
                    return thread_id
        return thread_id

    def scrap_tweet(self, tweet, type):
        """
        Scrap a tweet and return a Tweet object with all the information retrieved
        There a special cae when the tweet is a quote tweet, in this case, the tweet content correspond to the date of the quoted tweet
        Args:
            tweet (WebElement): The tweet to scrap
            type (str): The type of tweet (Normal or Réponse)
        Returns:
            Tweet: The tweet object with all the information retrieved
        """
        tweet_item = Tweet()

        try:
            elements = tweet.find_elements('xpath', './div/div/div[2]')
            content = elements[-1].find_elements('xpath', './div[2]/div')
        except Exception as e:
            raise "Couldn't get tweet content"
        
        header = content[0]
        time_posted_conv = self._get_tweet_posted_time(header)

        
        # Check if the tweet is a quote tweet
        try:
            date_cited_tweet = content[-2].find_elements('xpath','.//time')[0].get_attribute('datetime')
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
            pass

        try:
            content_tweet = content[-2]
            elements = content_tweet.find_elements(By.XPATH, "./div//*")
            content_list = []

            for element in elements:
                if element.tag_name == 'span':
                    content_list.append(element.text)
                elif element.tag_name == 'img':
                    content_list.append(element.get_attribute('alt'))
            content_tweet_text = " ".join(content_list)
        except Exception as e:
            raise f"Content was not correctly retrieved of tweet posted at {time_posted_conv}"


        try:
            comment, retweet, like, views = self._get_tweet_stats(content[-1])
        except Exception as e:
            raise f"Stats were not correctly retrieved of tweet posted at {time_posted_conv}"

        tweet_item.type = type
        tweet_item.time_posted = time_posted_conv
        tweet_item.content = content_tweet_text  
        tweet_item.comment = comment
        tweet_item.retweet = retweet
        tweet_item.like = like
        tweet_item.views = views
        return tweet_item
    

    def _get_tweet_stats(self, stats):
        """
        Get tweet stats for a tweet
        Args:
            stats (WebElement): The WebElement containing all the stats for a tweet (comment, retweet, like, views)
        Returns:
            tuple: A tuple containing the number of comment, retweet, like and views
        """

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
        """
        Get the posted time of a tweet
        Args:
            header (WebElement): The header of the tweet    
        Returns:    
            datetime: The posted time of the tweet
        """
        time_posted = header.find_element('xpath', './/time').get_attribute('datetime')
        time_posted_conv = datetime.strptime(time_posted, "%Y-%m-%dT%H:%M:%S.%fZ")
        return time_posted_conv