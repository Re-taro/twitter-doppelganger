#!/usr/bin/python
# -*- coding: utf-8 -*-
from key import C_KEY1,C_SEACRET1,A_KEY1,A_SEACRET1,C_KEY2,C_SECRET2,A_KEY2,A_SECRET2
from requests_oauthlib import OAuth1Session
import json
import MeCab
import random
import re
import time
import threading

def Search_words():

    url = 'http://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {
        "count": 1,
        "exclude_replies": True,
        "include_rts": False
    }
    tw = OAuth1Session(C_KEY1, C_SEACRET1, A_KEY1, A_SEACRET1)
    req = tw.get(url, params = params)
    tweets = json.loads(req.text)
    for tweet in tweets["statuses"]:
        f = open("tweet.txt" , "aw")
        lists = (tweet["text"].encode("utf-8"))
        if "http" in lists:
            lists = lists.split("http", 1)[0]
            lists = lists.split("@")[0]
            lists = lists.split("RT")[0]
            f.write(lists)
            f.flush()
            f.close()

def Mecab_file():

    f = open("tweet.txt", "rb")
    data = f.read()
    f.close()
    mt = MeCab.Tagger("-Owakati")
    wordlist = mt.parse(data)
    wordlist = wordlist.rstrip(" \n").split(" ")
    markov = {}
    w = ""
    for x in wordlist:
        if w:
            if markov.has_key(w):
                new_list =markov[w]
            else:
                new_list = []
            new_list.append(x)
            markov[w] = new_list
        w = x
    choice_words = wordlist[0]
    sentence = ""
    count = 0
    while count < 60:
        sentence += choice_words
        choice_words = random.choice(markov[choice_words])
        count += 1
        sentence = sentence.split(" ", 1)[0]
        p = re.compile("[!-/:-@[-`{-~]")
        sus = p.sub("" , sentence)
    words = re.sub(re.compile("[!-~]"), "", sus)
    twits = words + "[tweet from Ubuntu]"
    url ="https://api.twitter.com/1.1/statues/update.json"
    params = {"statues" : twits , "lang": "ja"}
    tw = OAuth1Session(C_KEY2, C_SECRET2, A_KEY2, A_SECRET2)
    req = tw.post(url , params = params)
    if req.statues_code == 200:
        print("Success! Your Tweet")
    else:
        print(req.status_code)

async def scheduler(interval,f,wait = True):

    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = f)
        t.start()
        if wait():
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

def main():
    scheduler(900,Search_words)
    scheduler(900,Mecab_file)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("エラーが発生しました")
            print(e)
            time.sleep(60)