import json, config
from requests_oauthlib import OAuth1Session
import MeCab
from wordcloud import WordCloud

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

count = input("分析するツイート数を入れてください : ")
screen_name = input("ユーザー名を入れてください：　") 
params ={'count' : int(count), 'screen_name' : screen_name}
req = twitter.get(url, params = params)

if req.status_code == 200:
    timeline = json.loads(req.text)
    tweets = ""
    for tweet in timeline:
        tweets = tweets + tweet['text'] + "\n\n"

    path_w = "twitter.txt"
    with open(path_w, mode="w") as f:
        f.write(tweets)

else:
    print("ERROR: %d" % req.status_code)

# -*- coding: utf-8 -*-

fi = open("twitter.txt",'r').read()
fo = open("mecab.txt",'w')

m = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
keyword = m.parse(fi) 

words = []
for row in keyword.split("\n"):
    word = row.split("\t")[0]
    if word == "EOS":
        break
    else:
        pos = row.split("\t")[1].split(",")[0]
        if pos == "名詞":
                words.append(word)
        else:
            pos = row.split("\t")[1].split(",")[0]
            if pos == "形容詞":
                words.append(word)
            else:
                pos = row.split("\t")[1].split(",")[0]
                if pos == "動詞":
                    words.append(word)

w =','. join(words)
keywords = w.replace(',',' ')

with open('mecab.txt', mode="w") as f:
    f.write(keywords)

def color_func(word, font_size, position, orientation, random_state, font_path):
    return '#00bfff'

with open("mecab.txt") as f:
    for words in f:
        stop_words = ['https','co',u'ある',u'さん',u'する',u'いる',u'こと','RT','デリ',u'てる',u'なる',u'なっ',u'そう',u'これ']
        wordcloud = WordCloud(background_color="#ffffff", color_func=color_func ,max_words=200, font_path="/System/Library/Fonts//ヒラギノ角ゴシック W3.ttc",width=300,height=300,stopwords=set(stop_words)).generate(words)

wordcloud.to_file("wordcloud.jpg")

