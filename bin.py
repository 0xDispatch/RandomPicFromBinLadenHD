# Import the libraries
import tweepy
import requests
import random
import traceback
import time 

#here's a list id with some gimmick accounts 
#you can create a list and add whoever you want and change the id to ur list
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

def read_file(filename):
  with open(filename, "r") as f:

    lines = f.readlines()
  # Return the list of lines
  return lines


def download_image(url, filename):
  # Send a GET request to the URL
  response = requests.get(f"https://www.cia.gov/library/abbottabad-compound/{url}")
  if response.status_code == 200:
    with open(filename, "wb") as f:
      f.write(response.content)
    return filename
  else:

    return False


def tweet_image(img, text, tweet_id):
  try:
    media = api.media_upload(img)
    m=[]
    m.append(media.media_id)
    api.update_status(status=f"pic name: {text}", in_reply_to_status_id=tweet_id, media_ids=m, auto_populate_reply_metadata=True)

    return True
  except Exception as e:

    traceback.print_exc()
    return False

# Define the main function that runs the bot
def main(tweet_id):
  lines = read_file("images.txt")
  line = random.choice(lines)[1:].strip()
  print(line)
  ext = line[len(line)-4:]
  text=line[38:]
  img = download_image(line, f"r{ext}")
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
#loop
while True:
    check()
    time.sleep(10)            
