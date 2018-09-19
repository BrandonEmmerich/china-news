# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import requests
from sqlalchemy import Column, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_urls():
    """A seeding process that gets urls to scrape for our initital database boot"""

    url_list = []
    for i in range(3):
        url = 'https://www.yicai.com/api/ajax/getjuhelist?action=news&page={}&pagesize=50'.format(i)
        url_list.append(url)

    return url_list

def get_yicai(url):
    """Get Yicai news data from api"""
    print url
    right_now = str(datetime.datetime.now())

    res = requests.get(url)
    df = pd.DataFrame(res.json())

    df_clean = df[['NewsID','CreateDate','url','NewsTitle','NewsNotes']]
    df_clean['date_added'] = right_now
    df_clean.columns = df_clean.columns.str.lower()
    df_clean['url'] = 'https://www.yicai.com' + df_clean['url']
    records = df_clean.to_dict(orient = 'records')

    return records

def write_data_to_db(results_list):
    """Write data to the SQL database"""
    flat_list = [item for sublist in results_list for item in sublist]

    engine = create_engine('postgresql://b:@localhost/china_news')
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    class yicai_results(Base):
        __tablename__ = 'yicai_results'
        newsid = Column('newsid', String, primary_key = True)
        createdate = Column('createdate', String)
        url = Column('url', String)
        newstitle = Column('newstitle', String)
        newsnotes = Column('newsnotes', String)
        date_added = Column('date_added', String)

    for story in flat_list:
        row = yicai_results(**story)
        session.merge(row)

    session.commit()
