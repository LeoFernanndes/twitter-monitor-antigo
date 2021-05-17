from twitter_database import mysql_rds_database_authentication
import pandas as pd
import os
from twitter_api import twitter_authentication
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
load_dotenv()




inicio = datetime.now()
api = twitter_authentication()

id, name, arroba, retweets, likes, text, date, location, hashtags, links, language, search = [], [], [], [], [], [], [], [], [], [], [], []


mydb = mysql_rds_database_authentication(os.environ.get('MYSQL_TWITTER_DATABASE'))
users = set(pd.read_sql('SELECT arroba FROM gestao_usuarios_arrobamodel;', con=mydb)['arroba'].values)
mydb.close()

count = 0

for userID in users:

  mydb = mysql_rds_database_authentication(os.environ.get('MYSQL_TWITTER_DATABASE'))
  
  try:
    newest_date = pd.read_sql(f"SELECT date FROM tweets where arroba = '{userID}' order by date desc limit 1;", con=mydb).date[0]
  except:
    newest_date = datetime(2020, 1, 1)

  
  mydb.close()

  tweets = api.user_timeline(screen_name=userID, 
                              # 200 is the maximum allowed count
                              count=1,
                              include_rts = True,
                              # Necessary to keep full_text 
                              # otherwise only the first 140 words are extracted
                              tweet_mode = 'extended'
                              )

  oldest_id = tweets[-1].id

  while len(tweets) > 0:
    
    count += 1
    if count % 50 == 0:
      time.sleep(10)

    
    mydb = mysql_rds_database_authentication(os.environ.get('MYSQL_TWITTER_DATABASE'))
    cursor = mydb.cursor()
    

    tweets = api.user_timeline(screen_name=userID, 
                              # 200 is the maximum allowed count
                              count=200,
                              include_rts = True,
                              # Necessary to keep full_text 
                              # otherwise only the first 140 words are extracted
                              max_id = int(oldest_id),
                              tweet_mode = 'extended',
                              )

    if len(tweets) == 0:
      continue
    

    for tweet in tweets:
      if hasattr(tweet, "quoted_status"):
        full_text = "QT {} \n QUOTED: {}".format(tweet.full_text, tweet.quoted_status.full_text)    
      if hasattr(tweet, "retweeted_status") is False:
        full_text = "{}".format(tweet.full_text)
      if hasattr(tweet, "retweeted_status") is True:
        full_text = "RT @{}: {}".format(tweet.retweeted_status.user.screen_name, tweet.retweeted_status.full_text)

      id.append(tweet.id_str), name.append(tweet.user.name), arroba.append(tweet.user.screen_name),
      retweets.append(tweet.retweet_count), likes.append(tweet.favorite_count), text.append(full_text),
      date.append(tweet.created_at - timedelta(hours=3)), location.append(tweet.user.location),
      hashtags.append(str(tweet.entities.get("hashtags"))), links.append(str(tweet.entities.get("urls"))),
      language.append(tweet.lang), search.append(userID)


      sql =  """
          INSERT IGNORE INTO `tweets` (id, name, arroba, retweets, likes, text, date, location, hashtags, links, language, search)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
          """

      cursor.execute(
              sql, (tweet.id_str, tweet.user.name, tweet.user.screen_name, tweet.retweet_count, tweet.favorite_count, full_text,
                    tweet.created_at - timedelta(hours=3), tweet.user.location, str(tweet.entities.get("hashtags")), str(tweet.entities.get("urls")), tweet.lang, userID)
          )

    mydb.commit()
    mydb.close()
    print(len(id))

     
    print(len(id), date[-1], date[0], oldest_id, id[-1], date[-1], newest_date)
    
    oldest_id = tweets[-1].id - 1

    if date[-1] < newest_date:
      break


tweets_df = pd.DataFrame({
    'id': id,
    'name': name,
    'arroba': arroba,
    'retweets': retweets,
    'likes': likes,
    'text': text,
    'date': date,
    'location': location,
    'hashtags': hashtags,
    'links': links,
    'language': language,
    'search': search
})

final = datetime.now()
print(final - inicio)

tweets_df

print(tweets_df.shape)