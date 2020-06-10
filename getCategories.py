import sys
import twitterscraper
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
import re,string
import nltk 
from textblob import TextBlob
from textblob import Word
import json
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
nltk.download('averaged_perceptron_tagger')

positive = 0
negative = 0
neutral = 0
totalTweets = 0
working = 0
secure = 0
charge = 0
time = 0
shipping = 0
delivery = 0
space = 0
location = 0
address = 0
final_res = {
            'Timing of delivery': 0,
             'Space of lockers': 0,
             'Functionality of lockers': 0,
             'Security of lockers': 0,
             'Location of lockers': 0,
             'Charges of locker': 0
             }

def getNegCategories(tweets):
    data=pd.DataFrame(t.__dict__ for t in tweets)
    data.drop_duplicates(subset="text",keep='first',inplace=True)
    data.drop(['has_media', 'hashtags', 'img_urls', 'is_replied','is_reply_to','likes','links','parent_tweet_id','replies','reply_to_users','screen_name','text_html','timestamp','timestamp_epochs','user_id','tweet_url','video_url','retweets','username','tweet_id'],axis=1,inplace=True)
    data.to_csv("uncleanedPART.csv")
 
    dataset= pd.read_csv("uncleanedPART.csv",encoding="utf-8")
    global totalTweets
    totalTweets = len((dataset))
   
    def strip_links(text):
        link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')    
        return text
    
    def strip_all_entities(text):
        entity_prefixes = ['@','#']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
               text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
               if word[0] not in entity_prefixes:
                words.append(word)
        return ' '.join(words)


    def removeNonAscii(s): 
        return "".join(filter(lambda x: ord(x)<128, s))

    with open('cleanedPART.csv','w',encoding="utf-8") as file:
      file.write("text")
      file.write("\n")
      for i in range(0,len(dataset)):
          text=dataset['text'][i]
          review= strip_all_entities(strip_links(text))
          review1=removeNonAscii(review)
          file.write(review1)
          file.write('\n')

    data= pd.read_csv("cleanedPART.csv",encoding="utf-8")
    
    with open('catogoriesNeutral27MAY.csv','w',encoding="utf-8") as file:
        for i in range(0,len(data)):
            blob= TextBlob(data["text"][i])
            x = blob.sentiment.polarity
            if(x<0):
                file.write('0')
                file.write('\n')
                global negative
                negative = negative + 1
            elif(x==0):
                file.write('N')
                file.write('\n')
                global neutral
                neutral = neutral + 1
            else:
                file.write('1')
                file.write('\n')
                global positive
                positive = positive + 1


    dataset= pd.read_csv("cleanedPART.csv",encoding="utf-8")

    # NEGATIVE CATEGORIES

    Item= dict()
    Item['fit']=0
    Item['fraud']=0
    Item['ship']=0
    Item['shipping']=0
    Item['shipped']=0
    Item['deliver']=0
    Item['delivered']=0
    Item['delivery']=0
    Item['storage']=0
    Item['space']=0
    Item['delivered']=0
    Item['full']=0
    Item['tight']=0 
    Item['big']=0
    Item['filled']=0
    Item['available']=0
    Item['time']=0
    Item['ago']=0
    Item['closed']=0
    Item['late']=0
    Item['tomorrow']=0
    Item['long']=0
    Item['location']=0
    Item['remotely']=0
    Item['walk']=0
    Item['far']=0
    Item['located']=0
    Item['broken']=0
    Item['lost']=0
    Item['fraud']=0
    Item['secure']=0
    Item['stolen']=0
    Item['steal']=0
    Item['missing']=0
    Item['fake']=0
    Item['empty']=0
    Item['working']=0
    Item['opening']=0
    Item['code']=0
    Item['work']=0
    Item['secret']=0
    Item['confused']=0
    Item['functional']=0
    Item['address']=0
    Item['expensive']=0
    Item['charge']=0
    Item['price']=0
    Item['paid']=0
    Item['pay']=0
    Item['fee']=0
    Item['free']=0
    Item['worth']=0
    Item['cost']=0

    for i in range(0,len(dataset)):
        T= TextBlob(dataset['text'][i])
        w= T.lower()
        if(w.sentiment.polarity<=0):
           for word in w.words:
               review= Word(word)
               r= review.lemmatize()
               if(r!='amazon' and r!='locker'):
                 if(r in Item):
                    Item[r]+=1
                 else:
                    Item[r]=1
    global shipping             
    shipping =0;
    shipping += Item['ship']+Item['shipping']+ Item['shipped']

    global delivery
    delivery=0;
    delivery+= Item['deliver']+ Item['delivered']+Item['delivery']

    global space
    space=0
    space+= Item['fit']+Item['storage']+Item['space']+Item['delivered']+Item['full']+Item['tight']+ Item['big']+Item['filled']+Item['available']

#2
    global time
    time=0;
    time+= Item['time']+Item['ago']+Item['closed']+Item['late']+Item['tomorrow']+Item['long']

#4
    global charge
    charge=0;
    charge+= Item['expensive']+Item['charge']+Item['cost']+Item['price']+Item['paid']+Item['pay']+ Item['fee']+ Item['free']+ Item['worth']

#5
    global location
    location=0;
    location+=Item['location']+ Item['remotely']+Item['walk']+Item['far']+Item['located']

#3
    global secure
    secure =0;
    secure+=Item['broken']+Item['lost']+Item['fraud']+Item['secure']+Item['stolen']+Item['steal']+Item['missing']+Item['fake']+Item['empty']

#1
    global working
    working=0;
    working+= Item['working']+Item['opening']+Item['code']+Item['work']+Item['secret']+ Item['confused']+Item['functional']

#6
    global address
    address=0;
    address+= Item['address']



# POSITIVE CATEGORIES

def getPosCategories(tweets):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    wordnet_lemmatizer = WordNetLemmatizer()
# Creating a dataframe
    data = pd.DataFrame(t.__dict__ for t in tweets)

    data.drop(['username', 'user_id', 'tweet_id', 'timestamp', 'retweets', 'screen_name', 'text_html', 'tweet_url',
           'links', 'hashtags', 'timestamp_epochs',
           'has_media', 'img_urls', 'video_url', 'likes',
           'replies', 'is_replied', 'is_reply_to', 'parent_tweet_id', 'reply_to_users'],
          axis=1, inplace=True)

# To remove url
    data['text'] = data['text'].replace(to_replace=r'https?:\/\/.*[\r\n]*', value='', regex=True)

# punctuations removal
    RE_PUNCTUATION = '|'.join([re.escape(x) for x in string.punctuation])
    data['text'] = data['text'].str.replace(RE_PUNCTUATION, "")

# duplicate rows are removed
    data.drop_duplicates(subset="text", keep='first', inplace=True)

    data.reset_index(inplace=True, drop=True)

# For textBlob to segregate as positive, negative and neutral
    count_pos = 0
    count_neg = 0
    count_neut = 0

    address = []
    for i in range(len(data)):
        address.append(0)

    data['Address'] = address

    for i in range(len(data)):
        sent = TextBlob(str(data.loc[i, 'text']))
        if (sent.sentiment.polarity > 0):
            count_pos = count_pos + 1
            data.loc[i, 'Address'] = 1


        elif (sent.sentiment.polarity < 0):
            count_neg = count_neg + 1
            data.loc[i, 'Address'] = -1


        else:
            count_neut += 1
            data.loc[i, 'Address'] = 0

# To drop negative tweets
    for i in range(len(data)):
        data.drop(data[data.Address == -1].index, inplace=True)

# To remove stopwords
    stop = stopwords.words('english')
    pat = r'\b(?:{})\b'.format('|'.join(stop))
    data['tweet'] = data['text'].str.replace(pat, '')
    data['tweet'] = data['tweet'].str.replace(r'\s+', ' ')

# to drop text column
    data.drop(['text'], axis=1, inplace=True)

# To remove numbers from tweet column
    data['tweet'] = data['tweet'].str.replace('\d+', '')

    data["tweet"] = data["tweet"].str.lower()

    data.drop_duplicates(subset="tweet", keep='first', inplace=True)


# to lemmatize data
    def nltk_tag_to_wordnet_tag(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None


    def lemmatize_sentence(sentence):
    # tokenize the sentence and find the POS tag for each token
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    # tuple of (token, wordnet_tag)
        wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
            # if there is no available tag, append the token as is
                lemmatized_sentence.append(word)
            else:
            # else use the tag to lemmatize the token
                lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
        return " ".join(lemmatized_sentence)


    data['Lemmatize'] = data['tweet'].apply(lambda x: lemmatize_sentence(x))

    data.drop_duplicates(subset="Lemmatize", keep='first', inplace=True)

# To tokenize column Lemmatize and form new cloumn text
    data['Text'] = data.apply(lambda row: nltk.word_tokenize(row['Lemmatize']), axis=1)
    data.drop(['tweet', 'Lemmatize'], axis=1, inplace=True)

# Categories to classify tweets
    timing = ['ontime', 'beforetime', 'before', 'within', 'withintime', 'time', 'early']
    space = ['space', 'storage', 'large', 'huge', 'spacious', 'big', 'giant']
    functionality = ['comfort', 'good', 'handy', 'easy', 'convenient', 'smooth', 'pick', 'enjoy', 'clean', 'genius',
                 'excite',
                 'great', 'recommend', 'love', 'satisfy', 'happy', 'awesome', 'sharingiscaring', 'awesomeness',
                 'cool''amuse', 'surprise', 'interesting', 'use', 'locker']
    security = ['secure', 'lock', 'trust', 'safe', 'locksystem', 'codeword']
    location = ['nearby', 'close', 'marketplace', 'walk', 'near', 'around', 'corner',
            'locate', 'neighborhood', 'nearest', 'location']
    charge = ['money', 'charge', 'affordable', 'price', 'minimal', 'minimum', 'less', 'cheap']

    for r1 in data['Text']:
        for i in r1:
            if i in timing:
                final_res['Timing of delivery'] += 1
                break

            elif i in space:
                final_res['Space of lockers'] += 1
                break

            elif i in security:
                final_res['Security of lockers'] += 1
                break

            elif i in location:
                final_res['Location of lockers'] += 1
                break

            elif i in charge:
                final_res['Charges of locker'] += 1
                break

            elif i in functionality:
                final_res['Functionality of lockers'] += 1
                break

            else:
                continue


if __name__ == "__main__":
    startDate = sys.argv[1]
    endDate = sys.argv[2]
    startYear = int(startDate.split('-')[0])
    startMonth = int(startDate.split('-')[1])
    startdate = int(startDate.split('-')[2])
    endYear = int(endDate.split('-')[0])
    endMonth = int(endDate.split('-')[1])
    enddate = int(endDate.split('-')[2])
    bd=dt.date(startYear,startMonth,startdate)
    ed=dt.date(endYear,endMonth,enddate)
    ln = 'english'
    limit =100000
    tweets = query_tweets("amazon locker",
                      begindate=bd,
                      enddate=ed,
                      limit=limit, lang=ln)
    getNegCategories(tweets)
    getPosCategories(tweets)
    resp = {
        'Total tweets' :  totalTweets,
        'Positive tweets' : positive,
        'Negative tweets' : negative,
        'Neutral tweets' :  neutral,
        "working": working,
        "secure": secure,
        "charge":charge,
        "time":time,
        "shipping":shipping,
        "delivery":delivery,
        "space":space,
        "location":location,
        "address":address,
        'Timing of delivery': final_res['Timing of delivery'],
        'Space of lockers': final_res['Space of lockers'],
        'Functionality of lockers': final_res['Functionality of lockers'],
        'Security of lockers': final_res['Security of lockers'],
        'Location of lockers': final_res['Location of lockers'],
        'Charges of locker': final_res['Charges of locker']
    }
    print(json.dumps(resp))
    

