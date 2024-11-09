from datetime import datetime

class Tweet:
    def __init__(self, type="", time_posted="", content="", thread_id="", comment=0, retweet=0, like=0, views=0):
        self.type = type
        self.time_posted = time_posted
        self.content = content
        self.thread_id = thread_id
        self.comment = comment
        self.retweet = retweet
        self.like = like
        self.views = views
        self.extraction_date = datetime.now()

    def __str__(self):
        return (f"Type: {self.type}\n"
                f"Time Posted: {self.time_posted}\n"
                f"Content: {self.content}\n"
                f"Associated Tweet ID: {self.associated_tweet_id}\n"
                f"Comments: {self.comment}\n"
                f"Retweets: {self.retweet}\n"
                f"Likes: {self.like}\n"
                f"Views: {self.views}\n"
                f"Extraction Date: {self.extraction_date}")

    def to_dict(self):
        return {
            'tweet_type': self.type,
            'time_posted': self.time_posted,
            'content': self.content,
            'thread_id': self.thread_id,
            'comments': self.comment, 
            'retweets': self.retweet, 
            'likes': self.like, 
            'views': self.views,
            'extraction_date': self.extraction_date
        }
    

