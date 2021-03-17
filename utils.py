import pyTigerGraphBeta as tg
import streamlit as st
import json
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

@st.cache
def load_config():
    with open('config.json') as f:
        config = json.load(f)
        return config

def connect_tg():

    config = load_config()

    TG_HOST = config["TG_HOST"] 
    TG_USERNAME = config["TG_USERNAME"]
    TG_PASSWORD = config["TG_PASSWORD"]
    TG_GRAPHNAME = config["TG_GRAPHNAME"]
    TG_SECRET = config["TG_SECRET"]

    conn = tg.TigerGraphConnection(host=TG_HOST, username=TG_USERNAME, password=TG_PASSWORD, graphname=TG_GRAPHNAME)

    token = conn.getToken(TG_SECRET)

    return conn

@st.cache
def run_installed_query(conn, query_name, params):

    result = conn.runInstalledQuery(query_name, params=params)

    return result

@st.cache
def load_html():
    html_file = open("asset/profile_with_data_and_skills.html", 'r', encoding='utf-8')
    html_code = html_file.read() 

    return html_code

@st.cache
def user_stats_html(values):

    html_code = load_html()
    soup = BeautifulSoup(html_code, 'html.parser')
    tags = soup.find_all(class_ = 'col-sm-9 text-secondary')
    
    i = 0
    for tag in tags:
        tag.string.replace_with(values[i])
        i += 1

    return str(soup)

@st.cache
def convert_to_df(result):

    df = pd.DataFrame.from_dict(result[0]['PRatedMovies'])

    df = pd.concat([df.drop(['attributes'], axis=1), df['attributes'].apply(pd.Series)], axis=1)

    df['@timestampOfP'] = [','.join(map(str, l)) for l in df['@timestampOfP']]

    df['@timestampOfP'] = df['@timestampOfP'].apply(lambda x: datetime.fromtimestamp(int(x)).strftime('%d-%m-%y'))

    df['@timestampOfP']= pd.to_datetime(df['@timestampOfP'])

    return df

@st.cache
def get_genere_df(df):

    df2 = df['genres'].str.get_dummies(sep='|')

    return df2