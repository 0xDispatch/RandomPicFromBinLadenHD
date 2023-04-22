# Import the libraries
import tweepy
import requests
import random
import traceback
import time 

#here's a list id with some gimmick accounts 
#https://twitter.com/i/lists/1648058838115921920
list_id = "1648058838115921920"

# Define the credentials for Twitter API
CK = "NEVER GONNA GIVE YOU UP"
CS="goofy ahhh hardcode"
AT = "idk"
AS = "another idk"

# Create an authentication object
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

# Create an API object
api = tweepy.API(auth)


#yes.. a whole function for just reading , I'm professional yo lmao
def read_file(filename):
  with open(filename, "r") as f:

    lines = f.readlines()
  # return the list of lines duh
  return lines


def download_image(url, filename):
  # Send a GET request to the URL
  response = requests.get(f"https://www.cia.gov/library/abbottabad-compound/{url}")
  if response.status_code == 200:
    with open(filename, "wb") as f:
      f.write(response.content)
    return filename


def tweet_image(img, text, tweet_id):
    media = api.media_upload(img)
    m=[]
    m.append(media.media_id)
    tweet = api.update_status(status=f"pic name: {text}", in_reply_to_status_id=tweet_id, media_ids=m, auto_populate_reply_metadata=True)
    time.sleep(3)
    api.retweet(id=tweet.id)
   
# Define the main function that runs the bot
def main(tweet_id):
  lines = read_file("images.txt")
  line = random.choice(lines)[1:].strip()
  text=line[37:]
  img = download_image(line, text)
  tweet_image(img=img, text=text, tweet_id=tweet_id)
 
#who needs a database anyway 
replied = []
def check():
        for tweet in api.list_timeline(list_id=list_id, count=1, tweet_mode="extended"):
            try:
                tweet_id = dict(tweet._json)["id"]
                tweet_text = dict(tweet._json)["full_text"]
                favorited= dict(tweet._json)["favorited"]
                #some lazy checks
                if favorited or tweet_id in replied or tweet_text.startswith("RT @"):
                    return True
                else:
                    main(tweet_id)
                    api.create_favorite(tweet_id)
                    replied.append(tweet_id)
                    print(replied)
            except Exception as err:
                traceback.print_exc()
#loop(isn't that obvious)
while True:
    check()
    #you can change the sleep, it was 10s but some gimmick accounts tweet a lot so 300s is fine
    time.sleep(300)            