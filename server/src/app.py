import os
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
except ImportError:
    pass
import requests

import nltk
import numpy
from nltk.corpus import wordnet

from flask import Flask, jsonify, request
from flasgger import Swagger
from slugify import slugify, Slugify
import json
from newspaper import Article

import requests
from requests_oauthlib import OAuth1

# Twitter API secrets
api_key = '8SwSOZbcRFyfyz8vqMh9XX2Lt'
api_secret_key = 'Ee4zGRQNHWXkPmzZ6Oe7uhLXnJWJS3To8bQS6tZYmPX6LrKzpN'
access_token = '1265491671648698368-fvByZJyYx1upmrjCsUqiwOyreEhuFj'
access_token_secret = '98z0u5wxxBhTFK1x3fD46ESoyWFSGO5WZ9w6A4jzCIkUU'


def twitter_api(twitter_handles):
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?tweet_mode=extended'
    parameters = {'screen_name': twitter_handles, 'count': 10, 'lang': 'en', 'result_type': 'recent'}
    auth = OAuth1(api_key, api_secret_key, access_token, access_token_secret)
    res = requests.get(url, params=parameters, auth=auth)
    return res.json()


def fetch_twitter_data():
    twitter_handles = ['cnnbrk']
    tweets = twitter_api(twitter_handles)
    output_data = []
    imp_content = ('created_at', 'full_text')
    for i in range(0, len(tweets)):
        final_dict = {x: tweets[i][x] for x in tweets[i] if x in imp_content}
        if "media" in tweets[i]['entities']:
            final_dict['tweet_url'] = tweets[i]['entities']['media'][0]['url']
            final_dict['media_url'] = tweets[i]['entities']['media'][0]['media_url_https']
        final_dict['source_name'] = tweets[i]['user']['name']
        final_dict['story_url'] = tweets[i]['entities']['urls'][0]['expanded_url']
        output_data.append(final_dict)
    return output_data


def video():
    response = db.table('video').select('*').execute()
    pending_news_list = []
    for doc in response.data:
        pending_news_list.append(doc)
    return pending_news_list


def getVideoPaginated(page):
    page = int(page)
    start = page * 10
    response = db.table('video').select('*').order('createdAt', desc=True).range(start, start + 9).execute()
    return response.data


def without_images(content):
    final_content = []
    for i in range(0, len(content)):
        if content[i]['urlToImage']:
            final_content.append((content[i]))
    return final_content


def fetch_news_business():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "business"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


def fetch_news_entertainment():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "entertainment"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


def fetch_news_technology():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "technology"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


def fetch_news_sports():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "sports"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


def fetch_news_health():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "health"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


def fetch_news_general():
    header = {"X-Api-Key": "0d5d496b5ff141a2bfad5bf45d91753c"}
    parameters = {"country": "in", "category": "general"}
    response = requests.get('https://newsapi.org/v2/top-headlines', headers=header, params=parameters)
    response = response.json()
    return without_images(response['articles'])


###########################################################################################

from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

try:
    db = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"WARNING: Supabase initialization failed: {e}")
    print("WARNING: Running in offline mode. Database operations will not work.")
    db = None

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')


def getnewsdataurl(content):
    article = Article(content['url'])
    article.download()
    article.parse()
    article.nlp()

    final_val = {'description': str(article.summary),
                 'urlToImage': article.top_image,
                 'url': content['url'],
                 'hashtags': article.keywords
                 }
    return final_val


def makedict(content):
    print(content)
    print(type(content))
    date = str(datetime.datetime.now(IST))
    newDate = date.split(' ')
    newUpdate = newDate[0].split('-')
    newUpdate[1] = int(newUpdate[1])
    if newUpdate[1] < 10:
        newUpdate[1] = str(newUpdate[1])
        newUpdate[1] = newUpdate[1].lstrip('0')
    content['createdAt'] = newUpdate[0] + '-' + str(newUpdate[1]) + '-' + newUpdate[2] + 'T' + newDate[1] + 'Z'
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
    m = month[newUpdate[1] - 1]
    time = newDate[1].split(':')
    hour = int(time[0])
    zone = ''
    if hour > 12:
        hour = hour - 12
        zone = 'PM'
    else:
        zone = 'AM'
    content['publishedAt'] = m + " " + newUpdate[2] + ", " + newUpdate[0] + " " + str(hour) + ":" + time[1] + " " + zone
    tags = content['hashtags'].split(',')
    hashtags = []
    for val in tags:
        val = val.strip(' ')
        hashtags.append(val)
    content['hashtags'] = hashtags
    return content


import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file = json.load(open(os.path.join(script_dir, 'contractions.txt'), 'r'))
contractions = file


def getCleanedNews_manual(content):
    content = content.lower()
    content = content.split()
    new_content = []
    for word in content:
        if word in contractions:
            new_content.append(contractions[word])
        else:
            new_content.append(word)
    content = " ".join(new_content)

    content = re.sub(r'https?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'&amp;', '', content)
    content = re.sub(r'\<a href', ' ', content)
    content = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', content)
    content = re.sub(r'<br />', ' ', content)
    content = re.sub(r'\'', ' ', content)
    return content


def get_desc_line(content):
    content = content.split()
    content = [word for word in content if not word in set(stopwords.words('english'))]
    lemma_words = []
    for word in content:
        word = WordNetLemmatizer().lemmatize(word)
        lemma_words.append(word)
    return lemma_words


def sentiment_analyse_manual(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score


def addHashtags_manual(newTag, story_id):
    story_id = [story_id]
    newCount = 1
    response = db.table('hashtags').select('*').eq('tag_name', newTag).execute()
    if response.data:
        hash_val = response.data[0]
        story_id.extend(hash_val['ids'])
        newCount = newCount + hash_val['count']
        db.table('hashtags').update({'count': newCount, 'ids': story_id}).eq('tag_name', newTag).execute()
    else:
        db.table('hashtags').insert({'tag_name': newTag, 'count': newCount, 'ids': story_id}).execute()


def get_human_names(text):
    person_list = []
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list


def addKeyPlayers(keyPlayer, story_id, photo):
    story_id = [story_id]
    newCount = 1
    imageUrl = photo
    response = db.table('keyplayer').select('*').eq('name', keyPlayer).execute()
    if response.data:
        hash_val = response.data[0]
        story_id.extend(hash_val['ids'])
        newCount = newCount + hash_val['count']
        db.table('keyplayer').update({
            'count': newCount,
            'ids': story_id,
            'urlToImage': imageUrl
        }).eq('name', keyPlayer).execute()
    else:
        db.table('keyplayer').insert({
            'name': keyPlayer,
            'count': newCount,
            'ids': story_id,
            'urlToImage': imageUrl
        }).execute()


def add_manual_news(content):
    data = makedict(content)

    if data['description']:
        cleaned_text = getCleanedNews_manual(data['description'])
        sentiment_score = sentiment_analyse_manual(cleaned_text)
        if sentiment_score['neg'] > sentiment_score['pos']:
            if sentiment_score['compound'] < -0.5:
                sentiment = 'Highly Negative'
            else:
                sentiment = 'Mild Negative'
        elif sentiment_score['neg'] < sentiment_score['pos']:
            if sentiment_score['compound'] > 0.5:
                sentiment = 'Highly Positive'
            else:
                sentiment = 'Mild Positive'
        else:
            sentiment = 'Neutral'

        data['sentiment_compound'] = sentiment_score['compound']
        data['sentiment'] = sentiment

        custom_slugify = Slugify(to_lower=True)
        data['desc_line'] = custom_slugify(data['title'])
        print("Data: ", data)
        if data['category'] == 'sponsored':
            response = db.table('sponsored').select('*').eq('description', data['description']).execute()
            if response.data:
                print('Sponsored News Available')
            else:
                print("Adding Sponsored News")
                insert_result = db.table('sponsored').insert(data).execute()
                id_post = insert_result.data[0]['id'] if insert_result.data else ''
                for tag in data['hashtags']:
                    addHashtags_manual(tag, id_post)
        else:
            person_list = get_human_names(data['description'])
            person_names = person_list
            for person in person_list:
                person_split = person.split(" ")
                for name in person_split:
                    if wordnet.synsets(name):
                        if name in person:
                            person_names.remove(person)
                            break

            print(person_names)
            data['keyplayers'] = person_names
            response = db.table('published').select('*').eq('description', data['description']).execute()
            if response.data:
                print('News Available')
            else:
                print("Adding News")
                insert_result = db.table('published').insert(data).execute()
                id_post = insert_result.data[0]['id'] if insert_result.data else ''
                for tag in data['hashtags']:
                    addHashtags_manual(tag, id_post)
                for person in person_names:
                    addKeyPlayers(person, id_post, data['urlToImage'])

    return "Database updated Successfully"


def deviceregister(content):
    content['date'] = datetime.datetime.now(IST).isoformat()
    content['category_preference'] = ['trending']
    content['key_preference'] = []
    content['hashtag_preference'] = []
    db.table('deviceinfo').insert(content).execute()


def addPreference(content):
    response = db.table('deviceinfo').select('*').eq('token', content['token']).execute()
    for dc in response.data:
        idToEdit = dc['id']
        category = [content['category'], content['language']]
        key = content['key']
        hashtag = content['hashtag']
        db.table('deviceinfo').update({
            'category_preference': category,
            'key_preference': key,
            'hashtag_preference': hashtag
        }).eq('id', idToEdit).execute()


def getPreference(token):
    response = db.table('deviceinfo').select('*').eq('token', token).execute()
    for dc in response.data:
        return dc['category_preference']


def getPreferenceSetting(token):
    response = db.table('deviceinfo').select('*').eq('token', token).execute()
    for dc in response.data:
        return dc


################### WEBSITE APIS START##################################

def getHomeData():
    response = db.table('published').select('*').eq('category', 'trending').order('createdAt', desc=True).limit(7).execute()
    docs = response.data
    trending_news_list = []
    toptrending = {}
    latestcards = []
    for i in range(0, len(docs)):
        if i == 0:
            toptrending = docs[i]
        elif 1 <= i < 4:
            latestcards.append(docs[i])
        else:
            trending_news_list.append(docs[i])

    response = db.table('video').select('*').order('createdAt', desc=True).limit(9).execute()
    docs = response.data
    row1_video = []
    row2_video = []
    latestvideo = []
    for i in range(0, len(docs)):
        if 0 <= i <= 1:
            d = docs[i]
            videoid = d['contentUrl'].split('=')[1]
            d['contentUrl'] = "https://www.youtube.com/embed/" + videoid
            row1_video.append(d)
        elif 2 <= i <= 3:
            d = docs[i]
            videoid = d['contentUrl'].split('=')[1]
            d['contentUrl'] = "https://www.youtube.com/embed/" + videoid
            row2_video.append(d)
        else:
            d = docs[i]
            videoid = d['contentUrl'].split('=')[1]
            d['contentUrl'] = "https://www.youtube.com/embed/" + videoid
            latestvideo.append(d)

    print(row1_video)
    response = db.table('published').select('*').eq('category', 'entertainment').order('createdAt', desc=True).limit(7).execute()
    docs = response.data
    entertainment_news_list = []
    topentertainment = {}
    latestEcards = []
    for i in range(0, len(docs)):
        if i == 0:
            topentertainment = docs[i]
        elif 1 <= i < 5:
            latestEcards.append(docs[i])
        else:
            entertainment_news_list.append(docs[i])

    response = db.table('keyplayer').select('*').order('count', desc=True).limit(5).execute()
    hash_list = []
    for dc in response.data:
        dic_key = {'keyplayer': dc['name'], 'img': dc['urlToImage']}
        hash_list.append(dic_key)

    final_li = [toptrending, latestcards, trending_news_list, row1_video, row2_video, latestvideo, topentertainment,
                latestEcards, entertainment_news_list, hash_list]
    return final_li


################## WEBSITE APIS END ####################################


################### Published News ADMIN Fetch and Edit START#############################

def get_admin_news_trending_published():
    response = db.table('published').select('*').eq('category', 'trending').order('createdAt', desc=True).limit(50).execute()
    return response.data


def get_admin_news_technology_published():
    response = db.table('published').select('*').eq('category', 'technology').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_business_published():
    response = db.table('published').select('*').eq('category', 'business').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_sports_published():
    response = db.table('published').select('*').eq('category', 'sports').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_world_published():
    response = db.table('published').select('*').eq('category', 'world').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_entertainment_published():
    response = db.table('published').select('*').eq('category', 'entertainment').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_health_published():
    response = db.table('published').select('*').eq('category', 'health').order('createdAt', desc=True).execute()
    return response.data


################### Published News ADMIN Fetch and Edit END############################


################### Unpublished News ADMIN Fetch and Edit START#############################

def get_admin_news_trending():
    response = db.table('unpublished').select('*').eq('category', 'trending').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_technology():
    response = db.table('unpublished').select('*').eq('category', 'technology').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_business():
    response = db.table('unpublished').select('*').eq('category', 'business').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_sports():
    response = db.table('unpublished').select('*').eq('category', 'sports').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_entertainment():
    response = db.table('unpublished').select('*').eq('category', 'entertainment').order('createdAt', desc=True).execute()
    return response.data


def get_admin_news_health():
    response = db.table('unpublished').select('*').eq('category', 'health').order('createdAt', desc=True).execute()
    return response.data


################### Unpublished News ADMIN Fetch and Edit END############################

def deleteUnplishedNews(delete_id):
    db.table('unpublished').delete().eq('id', delete_id).execute()


def deletePublishedNews(delete_id):
    db.table('published').delete().eq('id', delete_id).execute()


def addHashtags(newTag, story_id):
    story_id = [story_id]
    newCount = 1
    response = db.table('hashtags').select('*').eq('tag_name', newTag).execute()
    if response.data:
        hash_val = response.data[0]
        story_id.extend(hash_val['ids'])
        newCount = newCount + hash_val['count']
        db.table('hashtags').update({'count': newCount, 'ids': story_id}).eq('tag_name', newTag).execute()
    else:
        db.table('hashtags').insert({'tag_name': newTag, 'count': newCount, 'ids': story_id}).execute()


def edit_story(content):
    content = json.loads(content)
    id_post = content['id']
    del content['id']
    final_hashtags = content['hashtags'].split(',')
    while "" in final_hashtags:
        final_hashtags.remove("")
    content['hashtags'] = final_hashtags
    db.table('published').upsert({**content, 'id': id_post}).execute()
    deleteUnplishedNews(id_post)
    for tag in final_hashtags:
        addHashtags(tag, id_post)


def edit_story_published(content):
    content = json.loads(content)
    id_post = content['id']
    del content['id']
    db.table('published').update(content).eq('id', id_post).execute()


def getTags():
    response = db.table('hashtags').select('*').order('count', desc=True).limit(20).execute()
    hash_list = []
    for dc in response.data:
        dic_tag = {'tagName': dc['tag_name']}
        hash_list.append(dic_tag)
    return hash_list


################## NEW
def getDataFromHashtag(tagValue):
    response = db.table('hashtags').select('*').eq('tag_name', tagValue).execute()
    story_ids = []
    if response.data:
        story_ids = response.data[0]['ids']

    newsList = []
    for i in range(len(story_ids)):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])

    hash_list = getTags()
    return [newsList, hash_list]


def getDataFromHashtagPaginated(tagValue, pg):
    response = db.table('hashtags').select('*').eq('tag_name', tagValue).execute()
    story_ids = []
    if response.data:
        story_ids = response.data[0]['ids']

    newsList = []
    start = int(pg) * 10
    end = int(pg) * 10 + 10
    if end > len(story_ids):
        end = len(story_ids)
    for i in range(start, end):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])
    return newsList


def getDataFromKeyPlayer(keyplayer):
    response = db.table('keyplayer').select('*').eq('name', keyplayer).execute()
    story_ids = []
    if response.data:
        story_ids = response.data[0]['ids']

    newsList = []
    for i in range(len(story_ids)):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])
    return newsList


def getDataFromKeyPlayerPaginated(keyplayer):
    response = db.table('keyplayer').select('*').eq('name', keyplayer).execute()
    story_ids = []
    if response.data:
        story_ids = response.data[0]['ids']

    newsList = []
    for i in range(len(story_ids)):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])
    return newsList


def getSimilarHashtagData(tagValue, actual_post):
    response = db.table('hashtags').select('*').eq('tag_name', tagValue).execute()
    story_ids = []
    if response.data:
        for id_val in response.data[0]['ids']:
            if id_val != actual_post:
                story_ids.append(id_val)

    newsList = []
    for i in range(len(story_ids)):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])
    return newsList


def getSimilarHashtagDataDescription(tagValue, actual_post):
    response = db.table('hashtags').select('*').eq('tag_name', tagValue).execute()
    story_ids = []
    if response.data:
        for id_val in response.data[0]['ids']:
            if id_val != actual_post:
                story_ids.append(id_val)

    newsList = []
    limit = min(len(story_ids), 15)
    for i in range(0, limit):
        r = db.table('published').select('*').eq('id', story_ids[i]).execute()
        if r.data:
            newsList.append(r.data[0])
    return newsList


def getDescriptionData(newID):
    response = db.table('published').select('*').eq('id', newID).execute()
    final_li = []
    if response.data:
        pending_News_dict = response.data[0]

        hash_list = []
        for tag in pending_News_dict['hashtags']:
            h = getSimilarHashtagDataDescription(tag, pending_News_dict['id'])
            hash_list.extend(h)

        tagData = getTags()
        final_li.append(pending_News_dict)
        final_li.append(hash_list)
        final_li.append(tagData)

    final_li[1] = [i for n, i in enumerate(final_li[1]) if i not in final_li[1][n + 1:]]
    return final_li


def searchTags():
    response = db.table('hashtags').select('*').order('count', desc=True).execute()
    hash_list = []
    for dc in response.data:
        dic_tag = {'tagName': dc['tag_name']}
        hash_list.append(dic_tag)
    return hash_list


def getKeyPlayer():
    response = db.table('keyplayer').select('*').order('count', desc=True).execute()
    hash_list = []
    for dc in response.data:
        dic_key = {'keyplayer': dc['name'], 'img': dc['urlToImage']}
        hash_list.append(dic_key)
    return hash_list


############################################################################################


def get_news_trending():
    response = db.table('published').select('*').eq('category', 'trending').order('createdAt', desc=True).limit(20).execute()
    newli = [response.data, getTags()]
    return newli


def get_news_hindi():
    response = db.table('published').select('*').eq('category', 'hindi').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_world():
    response = db.table('published').select('*').eq('category', 'world').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_paginated(category, page):
    page = int(page)
    val = page * 10
    response = db.table('published').select('*').eq('category', category).order('createdAt', desc=True).range(val, val + 9).execute()
    post_list = list(response.data)

    sponsored_response = db.table('sponsored').select('*').eq('category', 'sponsored').order('createdAt', desc=True).range(page, page).execute()
    for doc in sponsored_response.data:
        print("In Sponsered")
        print(doc)
        post_list.append(doc)

    return post_list


def get_news_technology():
    response = db.table('published').select('*').eq('category', 'technology').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_business():
    response = db.table('published').select('*').eq('category', 'business').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_sports():
    response = db.table('published').select('*').eq('category', 'sports').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_entertainment():
    response = db.table('published').select('*').eq('category', 'entertainment').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


def get_news_health():
    response = db.table('published').select('*').eq('category', 'health').order('createdAt', desc=True).limit(27).execute()
    return [response.data, getTags()]


########## NEW API ##################

def get_news(categoryName):
    response = db.table('published').select('*').eq('category', categoryName).order('createdAt', desc=True).limit(25).execute()
    return [response.data, getTags()]


def get_admin_news(categoryName):
    response = db.table('published').select('*').eq('category', categoryName).order('createdAt', desc=True).limit(100).execute()
    return response.data


def get_admin_unpublished_news(categoryName):
    response = db.table('unpublished').select('*').eq('category', categoryName).order('createdAt', desc=True).limit(100).execute()
    return response.data


############################################################################################
app = Flask(__name__)
Swagger(app)


@app.route('/getVideo', methods=['GET'])
def getVideo():
    return jsonify(video())


@app.route('/getvideopaginated', methods=['GET'])
def getvideopaginated():
    page = request.args.get('pg')
    print(page)
    return jsonify(getVideoPaginated(page))


@app.route('/registerdevice', methods=['POST'])
def registerdevice():
    content = request.json
    content = json.dumps(content)
    content = json.loads(content)
    deviceregister(content)
    return "Device Registered Successfully"


@app.route('/toptags', methods=['GET'])
def toptags():
    """
                                           This is the top hashtag list API
                                           Call this api without passing any parameters. This API will return a list of 20 top hashtags.
                                           ---
                                           tags:
                                             - Service APIs

                                           responses:
                                             500:
                                               description: Error getting result
                                             200:
                                                description: The result will contain list of hashtags
                                                schema:
                                                    id: searchtag
                                                    properties:
                                                        tagName:
                                                            type: string
                                                            description : Name of the tag

                                    """
    return jsonify(getTags())


@app.route('/searchtags', methods=['GET'])
def complete_tags():
    """
                                           This is the hashtag list API
                                           Call this api without passing any parameters. This API will return a list of all the hashtags.
                                           ---
                                           tags:
                                             - Service APIs

                                           responses:
                                             500:
                                               description: Error getting result
                                             200:
                                                description: The result will contain list of hashtags
                                                schema:
                                                    id: searchtag
                                                    properties:
                                                        tagName:
                                                            type: string
                                                            description : Name of the tag

                                    """
    return jsonify(searchTags())


@app.route('/getkeyplayerslist', methods=['GET'])
def key_player_list():
    """
                                           This is the keyplayer list API
                                           Call this api without passing any parameters. This API will return a list of all the keyplayers.
                                           ---
                                           tags:
                                             - Service APIs

                                           responses:
                                             500:
                                               description: Error getting result
                                             200:
                                                description: The result will contain list of keyplayers
                                                schema:
                                                    id: Important
                                                    properties:
                                                        keyplayer:
                                                            type: string
                                                            description : Player Name
                                                        img:
                                                            type: string
                                                            description : Url To Image

                                    """
    return jsonify(getKeyPlayer())


@app.route('/v1/showtags', methods=['GET'])
def show_tags():
    tag = request.args.get('tagName')
    return jsonify(getDataFromHashtag(tag))


@app.route('/v1/showtagspaginated', methods=['GET'])
def show_tags_paginated():
    tag = request.args.get('tagName')
    page = request.args.get('pg')
    return jsonify(getDataFromHashtagPaginated(tag, page))


@app.route('/v1/showplayers', methods=['GET'])
def show_players():
    player = request.args.get('playerName')
    return jsonify(getDataFromKeyPlayer(player))


@app.route('/v1/delete_news', methods=['POST'])
def del_news():
    content = request.json
    content = json.loads(content)
    deleteUnplishedNews(content['id'])
    return 'DONE'


@app.route('/v1/addpreference', methods=['POST'])
def addpreference():
    content = request.json
    content = json.dumps(content)
    content = json.loads(content)
    addPreference(content)
    return 'DONE'


@app.route('/v1/getpreference', methods=['POST'])
def getpreference():
    content = request.json
    content = json.dumps(content)
    content = json.loads(content)
    return jsonify(getPreference(content['token']))


@app.route('/v1/settingspreference', methods=['POST'])
def settingspreference():
    content = request.json
    content = json.dumps(content)
    content = json.loads(content)
    return jsonify(getPreferenceSetting(content['token']))


@app.route('/v1/delete_news_published', methods=['POST'])
def del_news_published():
    content = request.json
    content = json.loads(content)
    deletePublishedNews(content['id'])
    return 'DONE'


@app.route('/description', methods=['GET'])
def desc_view():
    idToView = request.args.get('id')
    return jsonify(getDescriptionData(idToView))


@app.route('/v1/edit_news_story', methods=['POST'])
def edit_news_story():
    content = request.json
    edit_story(content)
    return "Got it!"


@app.route('/v1/addnews', methods=['POST'])
def addnews():
    content = request.json
    content = json.loads(content)
    return add_manual_news(content)


@app.route('/v1/getsummaryfromurl', methods=['POST'])
def summaryfromurl():
    content = request.json
    content = json.loads(content)
    return jsonify(getnewsdataurl(content))


@app.route('/v1/edit_news_story_published', methods=['POST'])
def edit_news_story_published():
    content = request.json
    edit_story_published(content)
    return "Got it!"


####################### UNPUBLISHED NEWS #########################

@app.route('/getadminnewsunpublished', methods=['GET'])
def getadminnewsunpublished():
    categoryName = request.args.get('category')
    return jsonify(get_admin_unpublished_news(categoryName))


@app.route('/getAdminValueTrending', methods=['GET'])
def getadminvaluetrending():
    return jsonify(get_admin_news_trending())


@app.route('/getAdminValueBusiness', methods=['GET'])
def getadminvaluebusiness():
    return jsonify(get_admin_news_business())


@app.route('/getAdminValueTechnology', methods=['GET'])
def getadminvaluetechnology():
    return jsonify(get_admin_news_technology())


@app.route('/getAdminValueEntertainment', methods=['GET'])
def getadminvalueentertainment():
    return jsonify(get_admin_news_entertainment())


@app.route('/getAdminValueHealth', methods=['GET'])
def getadminvaluehealth():
    return jsonify(get_admin_news_health())


@app.route('/getAdminValueSports', methods=['GET'])
def getadminvaluesports():
    return jsonify(get_admin_news_sports())


################ Published Section ADMIN PANEL

@app.route('/getadminnews', methods=['GET'])
def getadminnews():
    categoryName = request.args.get('category')
    return jsonify(get_admin_news(categoryName))


@app.route('/getAdminValueTrendingPublished', methods=['GET'])
def getadminvaluetrendingpublished():
    return jsonify(get_admin_news_trending_published())


@app.route('/getAdminValueBusinessPublished', methods=['GET'])
def getadminvaluebusinesspublished():
    return jsonify(get_admin_news_business_published())


@app.route('/getAdminValueTechnologyPublished', methods=['GET'])
def getadminvaluetechnologypublished():
    return jsonify(get_admin_news_technology_published())


@app.route('/getAdminValueEntertainmentPublished', methods=['GET'])
def getadminvalueentertainmentpublished():
    return jsonify(get_admin_news_entertainment_published())


@app.route('/getAdminValueHealthPublished', methods=['GET'])
def getadminvaluehealthpublished():
    return jsonify(get_admin_news_health_published())


@app.route('/getAdminValueSportsPublished', methods=['GET'])
def getadminvaluesportspublished():
    return jsonify(get_admin_news_sports_published())


@app.route('/getAdminValueWorldPublished', methods=['GET'])
def getadminvalueworldpublished():
    return jsonify(get_admin_news_world_published())


##########################################################################
### User-End Flask API


@app.route('/getnews', methods=['GET'])
def getnews():
    categoryName = request.args.get('category')
    return jsonify(get_news(categoryName))


@app.route('/getValueTrending', methods=['GET'])
def getvaluetrending():
    return jsonify(get_news_trending())


@app.route('/getpaginatedvalue', methods=['GET'])
def getpaginatedtrendingvalue():
    page = request.args.get('pg')
    category = request.args.get('category')
    return jsonify(get_news_paginated(category, page))


@app.route('/getValueBusiness', methods=['GET'])
def getvaluebusiness():
    return jsonify(get_news_business())


@app.route('/getValueTechnology', methods=['GET'])
def getvaluetechnology():
    return jsonify(get_news_technology())


@app.route('/getValueEntertainment', methods=['GET'])
def getvalueentertainment():
    return jsonify(get_news_entertainment())


@app.route('/getValueHealth', methods=['GET'])
def getvaluehealth():
    return jsonify(get_news_health())


@app.route('/getValueSports', methods=['GET'])
def getvaluesports():
    return jsonify(get_news_sports())


@app.route('/getValueWorld', methods=['GET'])
def getvalueworld():
    return jsonify(get_news_world())


@app.route('/getValueHindi', methods=['GET'])
def getvaluehindi():
    return jsonify(get_news_hindi())


@app.route('/homepage', methods=['GET'])
def homepage():
    return jsonify(getHomeData())


###########################################################################

@app.route('/fetch_newsapi/general', methods=['GET'])
def fetch_newsapi_general():
    return jsonify(fetch_news_general())


@app.route('/fetch_newsapi/health', methods=['GET'])
def fetch_newsapi_health():
    return jsonify(fetch_news_health())


@app.route('/fetch_newsapi/sports', methods=['GET'])
def fetch_newsapi_sports():
    return jsonify(fetch_news_sports())


@app.route('/fetch_newsapi/technology', methods=['GET'])
def fetch_newsapi_technology():
    return jsonify(fetch_news_technology())


@app.route('/fetch_newsapi/entertainment', methods=['GET'])
def fetch_newsapi_entertainment():
    return jsonify(fetch_news_entertainment())


@app.route('/fetch_newsapi/business', methods=['GET'])
def fetch_newsapi_business():
    return jsonify(fetch_news_business())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
