from flask import Flask, jsonify, request
import os
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
except ImportError:
    pass
import requests
import json
from slugify import slugify, Slugify

from supabase import create_client
import feedparser

import nltk
import numpy
import time
from nltk.corpus import wordnet

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')

try:
    db = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"WARNING: Supabase initialization failed: {e}")
    print("WARNING: Running in offline mode. Database operations will not work.")
    db = None

from newspaper import Article
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import requests
import json


########################  NOTIFICATION START  ######################################################
def notificationPost():
    response = db.table('video').select('*').order('createdAt', desc=True).limit(2).execute()

    newli = {}
    for doc in response.data:
        notification = {'title': doc['title'], 'body': doc['description'],
                        'image': doc['thumbnailUrl'],
                        'click_action': "com.theview.news_notification"}
        data = {
            'image': doc['thumbnailUrl'],
            'description': doc['description'],
            'pageid': doc['id'],
            'url': doc['url'],
            'publish': doc['publisher'],
            'date': doc['publishedAt']
        }

        deviceinfo_response = db.table('deviceinfo').select('*').execute()
        for dc in deviceinfo_response.data:
            newli = {
                'to': dc['token'],
                'notification': notification,
                'data': data
            }

            url = 'https://fcm.googleapis.com/fcm/send'
            headers = {
                'Authorization': 'key=AAAA-_lBP1s:APA91bEJDlr56cMVqNY-Ha_5atDMa_JvpQWnyfvmT4RTceh87FGJV9d0p7ELeKfb-bT5a6gWTk_J-Xwfzh-giddUnodLNyUgo3t1PD0HnMpD0_q8_JoIJaE848bOhpB_dEQVYbZ6iYl7',
                'Content-Type': 'application/json'
            }
            requests.post(url, data=json.dumps(newli), headers=headers)

        time.sleep(10)

    return newli


def notificationNewPost():
    deviceinfo_response = db.table('deviceinfo').select('*').execute()

    for dc in deviceinfo_response.data:
        category_li = dc['category_preference']
        for val in category_li:
            response = db.table('published').select('*').eq('category', val).order('createdAt', desc=True).limit(1).execute()
            for doc in response.data:
                notification = {'title': doc['title'], 'body': doc['description'],
                                'image': doc['urlToImage'],
                                'click_action': "com.theview.news_notification"}
                data = {
                    'image': doc['urlToImage'],
                    'description': doc['description'],
                    'pageid': doc['id'],
                    'url': doc['url'],
                    'publish': doc['publisher'],
                    'date': doc['publishedAt']
                }

                newli = {
                    'to': dc['token'],
                    'notification': notification,
                    'data': data
                }

                url = 'https://fcm.googleapis.com/fcm/send'
                headers = {
                    'Authorization': 'key=AAAA-_lBP1s:APA91bEJDlr56cMVqNY-Ha_5atDMa_JvpQWnyfvmT4RTceh87FGJV9d0p7ELeKfb-bT5a6gWTk_J-Xwfzh-giddUnodLNyUgo3t1PD0HnMpD0_q8_JoIJaE848bOhpB_dEQVYbZ6iYl7',
                    'Content-Type': 'application/json'
                }
                requests.post(url, data=json.dumps(newli), headers=headers)


def notificationKeyPlayer(content):
    deviceinfo_response = db.table('deviceinfo').select('*').execute()

    for dc in deviceinfo_response.data:
        key_li = content['keyplayers']
        for player in key_li:
            print(player)
            if player in dc['key_preference']:
                r = db.table('published').select('*').eq('id', content['id']).execute()
                if r.data:
                    pending_News_dict = r.data[0]

                    notification = {'title': pending_News_dict['title'], 'body': pending_News_dict['description'],
                                    'image': pending_News_dict['urlToImage'],
                                    'click_action': "com.theview.news_notification"}
                    data = {
                        'image': pending_News_dict['urlToImage'],
                        'description': pending_News_dict['description'],
                        'pageid': pending_News_dict['id'],
                        'url': pending_News_dict['url'],
                        'publish': pending_News_dict['publisher'],
                        'date': pending_News_dict['publishedAt']
                    }

                    newli = {
                        'to': dc['token'],
                        'notification': notification,
                        'data': data
                    }
                    url = 'https://fcm.googleapis.com/fcm/send'
                    headers = {
                        'Authorization': 'key=AAAA-_lBP1s:APA91bEJDlr56cMVqNY-Ha_5atDMa_JvpQWnyfvmT4RTceh87FGJV9d0p7ELeKfb-bT5a6gWTk_J-Xwfzh-giddUnodLNyUgo3t1PD0HnMpD0_q8_JoIJaE848bOhpB_dEQVYbZ6iYl7',
                        'Content-Type': 'application/json'
                    }
                    print('Notification sent')
                    requests.post(url, data=json.dumps(newli), headers=headers)
                    break


#####################  NOTIFICATION END ###############################################
def addVideo():
    url = "https://bing-video-search1.p.rapidapi.com/videos/search"

    querystring = {"q": "ndtv", "mkt": "en-IN"}

    headers = {
        'x-rapidapi-key': "397d27d483msh63799df563c8a87p10da81jsnae6f22dd7530",
        'x-rapidapi-host': "bing-video-search1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    for i in range(0, len(response['value'])):
        li = {}
        val = response['value'][i]
        if 'description' in val.keys():
            li['description'] = val['description']
            li['title'] = val['name']
            li['thumbnailUrl'] = val['thumbnailUrl']
            if 'creator' in val.keys():
                li['publisher'] = val['creator']['name']
            else:
                li['publisher'] = val['publisher'][0]['name']
            li['contentUrl'] = val['contentUrl']
            li['url'] = val['webSearchUrl']
            li['createdAt'] = val['datePublished']

            date = str(li['createdAt'])
            newDate = date.split('T')
            newUpdate = newDate[0].split('-')
            newUpdate[1] = int(newUpdate[1])
            if newUpdate[1] < 10:
                newUpdate[1] = str(newUpdate[1])
                newUpdate[1] = newUpdate[1].lstrip('0')
            month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                     'November', 'December']
            newUpdate[1] = int(newUpdate[1])
            m = month[newUpdate[1] - 1]
            time_parts = newDate[1].split(':')
            hour = int(time_parts[0])
            zone = ''
            if hour > 12:
                hour = hour - 12
                zone = 'PM'
            else:
                zone = 'AM'

            li['publishedAt'] = m + " " + newUpdate[2] + ", " + newUpdate[0] + " " + str(hour) + ":" + time_parts[1] + " " + zone

            if li['contentUrl'].split('.')[1] == 'youtube':
                r = db.table('published').select('*').eq('title', li['title']).execute()
                if r.data:
                    print('Video Available')
                else:
                    print('Adding Video')
                    db.table('video').insert(li).execute()


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


_dir = os.path.dirname(os.path.abspath(__file__))
file = json.load(open(os.path.join(_dir, 'contractions.txt'), 'r'))
contractions = file


def getCleanedNews(content):
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


def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    return score


def addHashtags(newTag, story_id):
    story_id = [story_id]
    newCount = 1
    try:
        response = db.table('hashtags').select('*').eq('tag_name', newTag).execute()
        if response.data:
            hash_val = response.data[0]
            story_id.extend(hash_val['ids'])
            newCount = newCount + hash_val['count']
            db.table('hashtags').update({'count': newCount, 'ids': story_id}).eq('tag_name', newTag).execute()
        else:
            try:
                db.table('hashtags').insert({'tag_name': newTag, 'count': newCount, 'ids': story_id}).execute()
            except Exception:
                # Race condition: already inserted, update instead
                db.table('hashtags').update({'count': newCount, 'ids': story_id}).eq('tag_name', newTag).execute()
    except Exception as e:
        print(f"addHashtags error for {newTag}: {e}")


def addKeyPlayers(keyPlayer, story_id, photo):
    story_id = [story_id]
    newCount = 1
    imageUrl = photo
    try:
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
            try:
                db.table('keyplayer').insert({
                    'name': keyPlayer,
                    'count': newCount,
                    'ids': story_id,
                    'urlToImage': imageUrl
                }).execute()
            except Exception:
                # Race condition: already inserted, update instead
                db.table('keyplayer').update({
                    'count': newCount,
                    'ids': story_id,
                    'urlToImage': imageUrl
                }).eq('name', keyPlayer).execute()
    except Exception as e:
        print(f"addKeyPlayers error for {keyPlayer}: {e}")


################## NDTV NEWS START  ##################################################

def makedict(source_url, category):
    feed = feedparser.parse(source_url)
    finalist = []
    for i in range(len(feed['entries'])):
        try:
            entry = feed['entries'][i]
            newsdict = {}
            newsdict['title'] = entry.get('title', '')
            newsdict['url'] = entry.get('link', '')
            # 'fullimage' is not always present — fall back to media content or empty
            newsdict['urlToImage'] = (
                entry.get('fullimage') or
                entry.get('media_content', [{}])[0].get('url', '') or
                entry.get('media_thumbnail', [{}])[0].get('url', '') or
                ''
            )
            newsdict['publishedAt'] = entry.get('updatedat') or entry.get('published', '')
            newsdict['publisher'] = entry.get('source', {}).get('title', 'NDTV')
            tags = entry.get('tags', [])
            newsdict['hashtags'] = [tags[0]['term']] if tags else [category]

            month = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            update = newsdict['publishedAt'].split(' ')
            if len(update) >= 5 and update[0] in month:
                index = str(month.index(update[0]) + 1)
                if int(index) < 10:
                    index = '0' + index
                if update[4] == 'PM':
                    hr = int(update[3].split(':')[0]) + 12
                    hr = '00' if hr == 24 else str(hr)
                    update[3] = hr + ':' + update[3].split(':')[1]
                newsdict['createdAt'] = update[2] + '-' + index + '-' + update[1].rstrip(',') + 'T' + update[3] + ':00Z'
            else:
                newsdict['createdAt'] = newsdict['publishedAt']

            newsdict['category'] = category
            finalist.append(newsdict)
        except Exception as e:
            print(f"Skipping entry {i}: {e}")
            continue

    return finalist


def fetch_news(source_url, category):
    data = makedict(source_url, category)
    for i in range(0, len(data)):
        if category == 'hindi':
            print('Hindi')
            article = Article(data[i]['url'], language='hi')
        else:
            article = Article(data[i]['url'])
        article.download()
        article.parse()
        article.nlp()

        summary = article.summary
        summary_len = len(summary.split(' '))
        if summary_len > 20:
            data[i]['description'] = summary
            if data[i]['description']:

                r = db.table('published').select('*').eq('title', data[i]['title']).execute()
                if r.data:
                    print('Available')
                else:
                    print('Adding')
                    cleaned_text = getCleanedNews(data[i]['description'])
                    sentiment_score = sentiment_analyse(cleaned_text)

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

                    data[i]['sentiment_compound'] = sentiment_score['compound']
                    data[i]['sentiment'] = sentiment

                    hashtags = get_desc_line(cleaned_text)
                    hashtags = list(dict.fromkeys(hashtags))

                    custom_slugify = Slugify(to_lower=True)
                    data[i]['desc_line'] = custom_slugify(data[i]['title'])

                    person_list = get_human_names(data[i]['description'])
                    person_names = person_list
                    for person in person_list:
                        person_split = person.split(" ")
                        for name in person_split:
                            if wordnet.synsets(name):
                                if name in person:
                                    person_names.remove(person)
                                    break

                    data[i]['keyplayers'] = person_names

                    insert_result = db.table('published').insert(data[i]).execute()
                    id_post = insert_result.data[0]['id'] if insert_result.data else ''
                    content = {}
                    if insert_result.data:
                        content = insert_result.data[0]

                    for tag in data[i]['hashtags']:
                        addHashtags(tag, id_post)

                    for person in person_names:
                        addKeyPlayers(person, id_post, data[i]['urlToImage'])

                    notificationKeyPlayer(content)

    return "Database updated Successfully"


#########################  NDTV NEWS START ####################################

#########################  BING NEWS START  ####################################

def makeBingdict(content, categoryName):
    data = {}
    date = str(content['datePublished'])
    newDate = date.split('T')
    newUpdate = newDate[0].split('-')
    newUpdate[1] = int(newUpdate[1])
    if newUpdate[1] < 10:
        newUpdate[1] = str(newUpdate[1])
        newUpdate[1] = newUpdate[1].lstrip('0')
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']
    m = month[newUpdate[1] - 1]
    time_parts = newDate[1].split(':')
    hour = int(time_parts[0])
    zone = ''
    if hour > 12:
        hour = hour - 12
        zone = 'PM'
    else:
        zone = 'AM'
    data['publishedAt'] = m + " " + newUpdate[2] + ", " + newUpdate[0] + " " + str(hour) + ":" + time_parts[1] + " " + zone
    print(content)
    data['category'] = categoryName
    data['createdAt'] = content['datePublished']
    data['description'] = content['description']

    if "about" in content:
        for val in range(len(content['about'])):
            if val == 0:
                data['keyplayers'] = [content['about'][val]['name']]
                data['hashtags'] = [content['about'][val]['name']]
            else:
                data['keyplayers'].append(content['about'][val]['name'])
                data['hashtags'].append(content['about'][val]['name'])
    else:
        data['keyplayers'] = ''
        data['hashtags'] = ''

    data['publisher'] = content['provider'][0]['name']
    data['title'] = content['name']
    if "ampUrl" in content:
        data['url'] = content['ampUrl']
    elif "url" in content:
        data['url'] = content['url']
    if "image" in content:
        data['urlToImage'] = content['image']['thumbnail']['contentUrl']
    else:
        data['urlToImage'] = content['provider'][0]['image']['thumbnail']['contentUrl']

    cleaned_text = getCleanedNews(data['description'])
    sentiment_score = sentiment_analyse(cleaned_text)

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

    hashtags = get_desc_line(cleaned_text)
    hashtags = list(dict.fromkeys(hashtags))

    data['desc_line'] = ''
    for j in range(len(hashtags)):
        if j != len(hashtags) - 1:
            data['desc_line'] = data['desc_line'] + hashtags[j] + '-'
        else:
            data['desc_line'] = data['desc_line'] + hashtags[j]

    return data


def fetchBingNews(categoryType, categoryName):
    url = "https://rapidapi.p.rapidapi.com/news"

    querystring = {"mkt": "en-IN", "safeSearch": "Off", "category": categoryType, "textFormat": "Raw"}
    headers = {
        'x-bingapis-sdk': "true",
        'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
        'x-rapidapi-key': "397d27d483msh63799df563c8a87p10da81jsnae6f22dd7530"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    content_list = json.loads(response.text)
    content_list = content_list['value']
    print(len(content_list))
    for i in range(0, len(content_list)):
        data = makeBingdict(content_list[i], categoryName)

        r = db.table('published').select('*').eq('title', data['title']).execute()
        if r.data:
            print('Available')
        else:
            print("Adding")
            insert_result = db.table('published').insert(data).execute()
            id_post = insert_result.data[0]['id'] if insert_result.data else ''
            content = {}
            if insert_result.data:
                content = insert_result.data[0]

            for tag in data['hashtags']:
                addHashtags(tag, id_post)

            for person in data['keyplayers']:
                addKeyPlayers(person, id_post, data['urlToImage'])

            notificationKeyPlayer(content)

    return "Database updated Successfully"


####################  BING NEWS END  #################################

def bingnewsUpdate():
    category = [{'categoryType': 'World', 'categoryname': 'world'}]
    print("Bing News")
    for i in range(0, len(category)):
        fetchBingNews(category[i]['categoryType'], category[i]['categoryname'])


def ndtvnewsUpdate():
    ndtv_li = [
        {'api': 'https://feeds.feedburner.com/ndtvnews-trending-news', 'category': 'trending', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/ndtvprofit-latest', 'category': 'business', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/gadgets360-latest', 'category': 'technology', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/ndtvcooks-latest', 'category': 'health', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/ndtvsports-latest', 'category': 'sports', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/ndtvmovies-latest', 'category': 'entertainment', 'provider': 'ndtv'},
        {'api': 'https://feeds.feedburner.com/ndtvkhabar-latest', 'category': 'hindi', 'provider': 'ndtv'}]

    for i in range(len(ndtv_li)):
        print(ndtv_li[i]['category'])
        fetch_news(ndtv_li[i]['api'], ndtv_li[i]['category'])

    addVideo()
    bingnewsUpdate()

    return "Database updated Successfully"


############################################################################################
app = Flask(__name__)


@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    return ndtvnewsUpdate()


@app.route('/getNotificationupdate', methods=['GET'])
def getnotificationupdate():
    notificationNewPost()
    return jsonify(notificationPost())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5050)))
