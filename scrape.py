import tweepy
import datetime
from plot import Map

class Scraper:
    def __init__(self, bearer_token, filename="tweets.txt"):
        self.token = bearer_token
        self.client = tweepy.Client(bearer_token)
        self.query = ""
    
    def _get_user_id(self,username):
        user = self.client.get_user(username=username)
        return user.data.id

    def _write_tweets(self, tweets, filename, verbose=False):
        for tweet in tweets.data:
            if verbose:
                print(str(tweet.text.encode('utf-8').decode('ascii','ignore')))
            with open(filename,"a") as f:
                f.write(str(tweet.text.encode('utf-8').decode('ascii','ignore')))
                f.write("\n")

    
    def update_query(self, hashtags, keywords, preposition, add_args ="-is:retweet"):
        print("Query updated!")
        str1 = f"({' OR '.join(hashtags)})"
        str2 = f"({' OR '.join(keywords)})"
        str3 = f"({' OR '.join(preposition)})"
        str4 = add_args
        self.query = " ".join([str1,str2,str3,str4])
    
    def scrap_query(self, filename="tweets.txt", time_limit=10, verbose=False, **kwargs):
        if not self.query:
            print("Please update query first!")
            return
        now = datetime.datetime.now(datetime.timezone.utc)
        start = now -  datetime.timedelta(minutes=time_limit)
        start = start.isoformat(timespec="seconds")
        tweets = self.client.search_recent_tweets(self.query, start_time=start, **kwargs)
        self._write_tweets(tweets, filename, verbose)
        print("Done scraping query.")

    def scrape_users(self, usernames, filename="tweets.txt", time_limit=10, verbose=False, **kwargs):
        now = datetime.datetime.now(datetime.timezone.utc)
        start = now -  datetime.timedelta(minutes=time_limit)
        start = start.isoformat(timespec="seconds")
        for user in usernames:
            user_id =  self._get_user_id(user)
            tweets = self.client.get_users_tweets(user_id, start_time=start, **kwargs)
            if tweets.data is None:
                print(f"No tweets for {user} in the given time limit!")
                continue
            self._write_tweets(tweets, filename, verbose)
            print("Done scraping users.")
    def plot_map(self, tweet_filename="tweets.txt", save="map.html"):
        print("Creating Map...")
        uk = Map(tweet_filename)
        uk.generate_map()
        uk.add_borders()
        uk.save_map(save)
        print("Plotted!")
        del uk

# EXAMPLE
if __name__ == "__main__":
    # Add your twitter token here
    bearer_token = "ADD YOUR TOKEN HERE"
    s = Scraper(bearer_token)
    hashtags = ["#ukraine","#russianarmy"]
    prepositions = ['near', '"south of"', '"north of"', '"east of"', '"west of"']
    key_words = ['spotted', 'movement', 'soldiers', 'attacks', 'army', 'military', 'vehicles', 'aircraft', 'plane', 'shoot', 'shell', 'fight', 'invaders', 'strike', 'tank']
    s.update_query(hashtags,key_words,prepositions)
    s.scrap_query(time_limit=100)
    s.scrape_users(["COUPSURE","OsintUpdates"],filename="tweets.txt",time_limit=200)
    s.plot_map(save="map.html")


        


    