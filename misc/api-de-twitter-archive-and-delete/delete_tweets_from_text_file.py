import tweepy

CONSUMER_KEY = "PUT HERE CONSUMER KEY"
CONSUMER_SECRET = "PUT HERE CONSUMER SECRET"
ACCESS_TOKEN_KEY = "PUT HERE TOKEN KEY"
ACCESS_TOKEN_SECRET = "PUT HERE TOKEN SECRET"

if __name__ == "__main__":
    text_file = open("tweets.txt", "r") #This is where you should put the path of your text file
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
                print(str(count) + " - [Tweet Deleted] - " + "ID: " + str(_id) )
                #if count >= 200:
                #    break

            except Exception as e:
                print(str(count) + "<<<< I can't delete >>>> "+ "ID: " + str(_id) +" - " + str(e))
                pass
        pass
        print("Finalized.")
        print("I deleted " + str(count) + " tweets.")

