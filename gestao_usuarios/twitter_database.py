import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


def mysql_rds_database_authentication(database=None):
  
    if database:
        mydb = mysql.connector.connect(
            host = os.environ.get('MYSQL_TWITTER_HOST'),
            user = os.environ.get('MYSQL_TWITTER_USER'),
            port = os.environ.get('MYSQL_TWITTER_PORT'),
            password = os.environ.get('MYSQL_TWITTER_PASSWORD'),
            database = database
        )

        return mydb

    else:
        mydb = mysql.connector.connect(
            host = os.environ.get('MYSQL_TWITTER_HOST'),
            user = os.environ.get('MYSQL_TWITTER_USER'),
            port = os.environ.get('MYSQL_TWITTER_PORT'),
            password = os.environ.get('MYSQL_TWITTER_PASSWORD')
        )

        return mydb

    