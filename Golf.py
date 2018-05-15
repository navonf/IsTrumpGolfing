# This Golf class will be responsible for scraping the latest
# Trump golf outing located on trumpgolfcount.com
from bs4 import BeautifulSoup

import requests
import json
import twitter
import lxml
import pyrebase

config = {
  "apiKey": "AIzaSyB9f7U74SAIXULRwDlNfN98HkbJ332-bQQ",
  "authDomain": "trumpbot-345fd.firebaseapp.com",
  "databaseURL": "https://trumpbot-345fd.firebaseio.com",
  "storageBucket": "trumpbot-345fd.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

api = twitter.Api(
    consumer_key='B2eoLT9FDDWE5CkSUCaTOk9jc',                               # Consumer Key (API Key)
    consumer_secret='MNMQQvPVCrIqkscUgRTsOmT0inXQiI3kbuJAjDrh66hbwVW93z',   # Consumer Secret (API Secret)
    access_token_key='994313959934234629-bPOds39rZrf53heJRlmB1YKpnEq4YdG',  # Acess Token
    access_token_secret='RxO69a6Woo5qHYxW9G3277Jo4OGghd7n7xqMLsFX5AIDu')    # Access Token Secret
    
def main():
    get_latest_outing()

def push_db(data):
    # db.child("time").push(data)
    db.child("time").child("-LCM0jw1YhB_MxPrN5RS").update({"timez" : data})
    print("database has been updated: ", data)

def get_latest_outing():
    url = 'http://trumpgolfcount.com/displayoutings#tablecaption'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    last_outing = soup.find_all('tr')[1]
    golf_info = []

    for text in last_outing:
        if text.string == '\n':
            continue
        elif text.string == None:
            golf_info.append(text.a.string)
        golf_info.append(text.string)

    # make total time in hours and minutes
    # time = golf_info[11].split(":")
    # total_time = time[0] + " hours and " + time[1] + "minutes"

    print("============== template ==============")
    tweet = "Trump went golfing!" + "\n" + "Where: " + str(golf_info[3]) + "\n" + "When: " + str(golf_info[0]) + "- " + str(golf_info[1])+ "\n" + "Total visits to date: " + str(golf_info[9])
    print(golf_info)
    print("======================================")
    is_new(str(golf_info[0]), tweet)

def is_new(new, tweet):
    # we need the key to access the table
    print("accessing db . . .")
    oldkey = list(db.child("time").get().val())[0]
    print("db accessed. success!")
    old = db.child("time").get().val()[oldkey]['timez']
    print("old: ", old)
    print("new: ", new)

    if old == new:
        print("Trump has not gone golfing yet.")
    else:
        print("Trump went golfing, tweet!")
        post_tweet(new, tweet)

def post_tweet(new, text):
    print("posting tweet . . .")
    push_db(new)
    api.VerifyCredentials()
    api.PostUpdate(text)
    print(api.VerifyCredentials())
    print("Tweet has been posted.")



if __name__ == "__main__": main()
