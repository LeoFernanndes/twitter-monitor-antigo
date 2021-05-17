import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


def mysql_rds_database_authentication(database):

    mydb = mysql.connector.connect(
        host = os.environ.get('MYSQL_TWITTER_HOST'),
        user = os.environ.get('MYSQL_TWITTER_USER'),
        port = os.environ.get('MYSQL_TWITTER_PORT'),
        password = os.environ.get('MYSQL_TWITTER_PASSWORD'),
        database = database
    )

    return mydb

    


database = os.environ.get('MYSQL_TWITTER_DATABASE')
mydb = mysql_rds_database_authentication(database)

cursor = mydb.cursor()

cursor.execute(
    f"""
    USE {database};
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOt EXISTS `tweets` (
      id VARCHAR(50) PRIMARY KEY,
      name TEXT,
      arroba TEXT,
      retweetS INT,
      likes INT,
      text TEXT,
      date DATETIME,
      location TEXT,
      hashtags TEXT,
      links TEXT,
      language TEXT,
      search TEXT
    );
    """
)