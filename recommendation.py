"""
filename : recommendation.py

Page : Recommendation

This script displays table of recommendation with pagination and download
option and bar plot of recommended genre plot
"""

import streamlit as st
import plotly.graph_objects as go
from math import ceil

from utils import run_installed_query
from utils import convert_to_user_rec_df
from utils import get_genre_df
from utils import filter_results
from utils import download_file
from utils import adjust_style


def recommended_movies(conn, user_id):
    """
    Function for Recommendation page, shows recommended movie table
    and plot of recommende genre count bar plot

    input ::
        - conn:tigergraph connection object
        - user id for which plot is generated

    output :: table of recommendations with button to save table as csv
    and bar plot of genre count
    """

    st.markdown("<b>Recommended Movies</b>", unsafe_allow_html=True)

    user_num = st.slider("Select Number of User", 5, 100)

    similar_movies = st.slider("Select Number of Similar Movies", 5, 100)

    st.write("")

    params = dict()
    params['p'] = user_id
    params['k1'] = user_num
    params['k2'] = similar_movies

    query_response = run_installed_query(conn, "RecommendMovies", params)

    df = convert_to_user_rec_df(query_response)

    df.reset_index(inplace=True, drop=True)
    df.index += 1

    # pagination
    page_size = 20
    page_number = st.number_input(
        label="Page Number",
        min_value=1,
        max_value=ceil(len(df)/page_size),
        step=1,
    )
    current_start = (page_number-1)*page_size
    current_end = page_number*page_size

    filter_table = filter_results(df, current_start, current_end)

    filter_table = filter_table.to_html(escape=False)

    filter_table = adjust_style(filter_table)

    st.write(filter_table, unsafe_allow_html=True)
    st.write("")
    st.write("")

    # download button
    filename = str(user_id)+"_recommended_movie.csv"
    download_button_str = download_file(df, filename)
    st.markdown(download_button_str, unsafe_allow_html=True)

    genre_df = get_genre_df(df)

    genre_stats = genre_df.sum(numeric_only=True, axis=0)
    genre_index = genre_stats.index.tolist()
    genre_values = genre_stats.values.tolist()

    st.write("")
    st.markdown("<b>Recommended genres</b>", unsafe_allow_html=True)

    # green bar with max value highlighting
    colors = ['cornflowerblue'] * len(genre_index)
    maxval = max(genre_values)
    ind = [i for i, v in enumerate(genre_values) if v == maxval]

    for i in ind:
        colors[i] = 'green'
        layout = dict(
            xaxis=dict(title='Genre', ticklen=5, zeroline=False),
            yaxis=dict(title='No. of ratings', ticklen=5, zeroline=False)
            )

    fig = go.Figure(data=[go.Bar(
            x=genre_index,
            y=genre_values,
            marker_color=colors
        )], layout=layout)

    fig.update_layout(title_text='Genre wise movie rating count')
    st.plotly_chart(fig, use_container_width=True)

    href = f"""<a href="#top">Back to top</a>"""
    st.markdown(href, unsafe_allow_html=True)
