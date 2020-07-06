#!/usr/bin/python3
'''
Deletes old tweets.
'''
import sys
import time
import tweepy

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""


def main():
    '''
    main function
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    print("listo")

    def print_tweet(status):
        '''
        prints a tweet
        '''
        print("------------------------------------------------")
        print("Automatically deleting:")
        print(status.id_str)
        print(status.created_at)
        print(status.text)
        api.destroy_status(id = status.id)
        print("")
        print("")

    def fetch_old_tweets(max_id):
        '''
        fetches old tweets
        '''
        time.sleep(5)
        array_tweets = []
        _page=5
        while max_id > 0:
            tweets = api.user_timeline(count=200, page=_page)
            if tweets:
                if tweets.max_id > max_id:
                    print("sigo buscando Max_id:" + str(tweets.max_id) + " " + str(tweets[-1].created_at))
                else:
                    print("encontre Max_id:" + str(tweets.max_id) + " " + str(tweets[-1].created_at))
            _page = _page+1
        pass


        total = 0
        oldest_id = 0

        for status in tweets:
            total = total + 1
            print_tweet(status)
            oldest_id = status.id

        return total, oldest_id

    max_id = XXXXXXXXXXXXXXXXXXX 
   

    if len(sys.argv) >= 2:
        max_id = int(sys.argv[1])
        
    
    oldest_id = 0
    total = 0
    eof = False
    api_calls = 0

    try:
        while not eof:
            api_calls = api_calls + 1
            local_total, oldest_id = fetch_old_tweets(max_id)
            total = total + local_total
            if oldest_id > 0:
                # we had some last result, next time we'll continue from that one
                max_id = oldest_id - 1
            else:
                # just substract maxcount
                max_id = max_id - 200

            eof = max_id <= 0
    finally:
        print("")
        print("Total tweets:", total)
        print("Total api calls:", api_calls)
        print("Max ID:", max_id)
        print("")


if __name__ == "__main__":
    #main()
    text_file = open("/home/user/src/testFile.txt", "r") # <-- Acá va el textfile con los IDs
    lines = text_file.readlines()
    text_file.close()

    if lines:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        count=0
        for line in lines:
            try:
                count = count + 1
                _id=int(line.rstrip("\n"))
                api.destroy_status(id=_id)
                print(str(count) + " - [Eliminado] - " + "ID: " + str(_id) )
                #if count >= 200:
                #    break

            except Exception as e:
                print(str(count) + "<<<< NO SE PUEDE ELIMINAR >>>> "+ "ID: " + str(_id) +" - " + str(e))
                pass
        pass
        print("Finalizado.")
        print("se eliminaron " + str(count) + " tweets.")

