"""
filename : utils.py

This script contains common functions called from different scripts.
"""

import pyTigerGraphBeta as tg
import streamlit as st
import streamlit.components.v1 as components

import json
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import base64
import uuid
import re


def header():
    """function to display header on every page"""

    st.markdown("""<h1 style='text-align: center; color: black;'><a id="top">
    TigerStream</a></h1>""", unsafe_allow_html=True)
    st.markdown("""<h1 style='text-align: center; color: black;'>
    Movie Recommendation</h1>""", unsafe_allow_html=True)
    st.write("")
    st.write("")


@st.cache
def load_config():
    """
    function to load all credentials stored in config.json

    return :: json object containing all credentials
    """

    with open('config.json') as f:
        config = json.load(f)
        return config


def load_html(path):
    """
    function to load html files present in asset directory.
    This function is called from User statistics, Movie Recommendation,
    and User Network page.

    input :: path of html file

    output :: html code read from file
    """

    html_file = open(path, 'r', encoding='utf-8')
    html_code = html_file.read()

    return html_code


def show_data_info(tooltip_text):
    """
    This function displays information on Movie Recommnedation page
    located in root navidation, data stats is shown from statics html page
    and data sample is loaded from asset folder.
    """

    st.markdown(tooltip("<b>Dataset Information</b>",
                        tooltip_text["dataset_info"]),
                unsafe_allow_html=True)

    html_code = load_html('asset/data_info.html')
    components.html(html_code, width=995, height=300, scrolling=False)

    st.markdown("<b>Sample of movies.csv</b>", unsafe_allow_html=True)
    movie_header = pd.read_csv('asset/movies_head.csv')
    movie_header.index += 1
    st.table(movie_header)

    st.markdown("<b>Sample of ratings.csv</b>", unsafe_allow_html=True)
    rating_header = pd.read_csv('asset/ratings_head.csv')
    rating_header.index += 1
    st.table(rating_header)


@st.cache(allow_output_mutation=True)
def connect_tg():
    """
    function to connect with tigergraph

    return :: connection object to make API call
    """

    config = load_config()

    TG_HOST = config["TG_HOST"]
    TG_USERNAME = config["TG_USERNAME"]
    TG_PASSWORD = config["TG_PASSWORD"]
    TG_GRAPHNAME = config["TG_GRAPHNAME"]
    TG_SECRET = config["TG_SECRET"]

    conn = tg.TigerGraphConnection(host=TG_HOST,
                                   username=TG_USERNAME,
                                   password=TG_PASSWORD,
                                   graphname=TG_GRAPHNAME)

    token = conn.getToken(TG_SECRET)
    print(token)
    return conn


@st.cache
def run_installed_query(conn, query_name, params):
    """
    function to run installed queries written in GraphStudio

    input ::
        - conn : TigerGraph connection object
        - query_name : name of the query written in GraphStudio
        - params : paramters required to run installed query

    Output :: JSON object of query response
    """

    result = conn.runInstalledQuery(query_name, params=params)
    return result


@st.cache
def user_stats_html(values):
    """
    function is used in User Statistics page,
    it reads template and updates with fetched user details.

    input :: list containing values like no. of movies rated,
    avg rating, timestamp etc

    output :: html code updated with input values
    """

    path = "asset/user_profile.html"
    html_code = load_html(path)
    soup = BeautifulSoup(html_code, 'html.parser')
    tags = soup.find_all(class_='col-sm-9 text-secondary')

    i = 0
    for tag in tags:
        tag.string.replace_with(values[i])
        i += 1

    return str(soup)


@st.cache
def convert_to_user_stats_df(result):
    """
    function to convert UserStatstics query response to pandas dataframe

    input :: query response

    output :: pandas dataframe of reponse with processed fields
    """

    df = pd.DataFrame.from_dict(result[0]['PRatedMovies'])

    df = pd.concat([df.drop(['attributes'], axis=1),
                    df['attributes'].apply(pd.Series)], axis=1)

    df['@timestampOfP'] = [','.join(map(str, ts)) for ts in df['@timestampOfP']]
    df['@timestampOfP'] = df['@timestampOfP'].apply(lambda x: datetime.fromtimestamp(int(x)).strftime('%d-%m-%y'))
    df['@timestampOfP'] = pd.to_datetime(df['@timestampOfP'])

    return df


@st.cache
def get_genre_df(df):
    """
    function to generate dummies from '|' seperated genres

    input :: dataframe generated from convert_to_user_stats_df function

    output :: dummies dataframe, where 1 and 0 will be present in each
    genre column for each movie
    """

    df2 = df['genres'].str.get_dummies(sep='|')

    return df2


@st.cache(allow_output_mutation=True)
def convert_to_graphistry_df(result, user_id):
    """
    function to convert SimilarUser query response to pandas dataframe
    for graphistry visualization

    input :: query response and user id

    output :: pandas dataframe of reponse with processed fields
    """

    df = pd.DataFrame.from_dict(result[0]['PeopleRatedSameMovies'])
    df['v_type'] = user_id
    df[['movieCount', 'movieList']] = pd.json_normalize(df['attributes'])
    del df['attributes']

    return df


def convert_to_pyviz_df(result, user_id):
    """
    function to convert UserStatstics query response to pandas dataframe
    for pyviz visualization

    input :: query response of similar people, user id

    output :: pandas dataframe of reponse with processed fields
    """

    df = pd.DataFrame.from_dict(result[0]['PeopleRatedSameMovies'])
    df['v_type'] = user_id
    df[['movieCount', 'movieList']] = pd.json_normalize(df['attributes'])
    df['v_type'] = df['v_type'].astype(str)
    df['movieCount'] = df['movieCount'].astype(str)
    del df['attributes']

    return df


@st.cache(allow_output_mutation=True)
def convert_to_user_rec_df(result):
    """
    function to convert MovieRecommendation query response to pandas dataframe

    input :: query response

    output :: pandas dataframe of reponse with processed fields
    """

    df = pd.DataFrame.from_dict(result[0]['RecommendedMovies'])
    df = pd.concat([df.drop(['attributes'], axis=1),
                    df['attributes'].apply(pd.Series)], axis=1)

    df = df.drop(columns=['timestamp', '@dotProductAB', '@cosineSimilarity',
                          '@ratingByP', '@lengthASqr', '@lengthBSqr',
                          '@rated', 'v_type', '@recommendScore', 'v_id'])

    return df


def filter_results(results, start, end) -> pd.DataFrame:
    """
    function used in Recommendation page to display datafrae rows
    based on input range

    input ::
        - results : dataframe on which range needs to apply
        - start : number from where filtering starts
        - end : number to which filtering need

    output :: dataframe with input range applied
    """

    results = results[start:end]

    return results


def download_file(df, name):
    """
    function used in Recommendation page to download table of recommended movie

    input ::
        - df : dataframe / table needs to be downloaded
        - name : by name file needs to store

    output :: html code to download file,
    will be placed in markdown in Recommendation page
    """

    object_to_download = df.to_csv(index=False)
    try:
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError:
        b64 = base64.b64encode(object_to_download).decode()

    button_text = 'Download Table'
    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }}
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{name}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link


def adjust_style(table):
    """
    function used in Recommendation Page to make table header
    and rows to align in center and apply effect on hover

    input :: dataframe converted in html, effects will be added in this

    output :: updated html code of table
    """

    style = "<style>tr, th, td {text-align: center;}tr:hover {background-color:#f63366;}</style>"

    result = "<html><head>"+style+"</head><body>"+table+"</body></html>"

    return result


@st.cache
def load_tooltip_text():
    """
    Function loads tooltip file which contains text to display on hover

    returns :: dictionary of tooltip
    """

    with open('tooltip_text.json') as f:
        tooltip_text = json.load(f)
        return tooltip_text


def tooltip(title, tip):
    """
    Function to show toolotip on hover.

    input ::
        - title : text on which tooltip will be displayed.
        - tip : text that will be visible on hover

    output :: html code with title and tooltip value
    """

    html = """
    <style>
    .tooltip {{
    position: relative;
    display: inline-block;

    }}
    .tooltip .tooltiptext {{
    visibility: hidden;
    width: 200%;
    background-color: black;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    bottom: 100%;
    left: 50%;
    margin-left: -80px;
    font-size: 13px;
    font-weight: bold;
    }}
    .tooltip:hover .tooltiptext {{
    visibility: visible;
    }}

    </style>

    <div class="tooltip"><h3>{}</h3>
    <span class="tooltiptext">{}</span>
    </div> """
    return html.format(title, tip)
