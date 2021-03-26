"""
filename : user_statistics.py

Page : User Statistics

This script is responsible for user stats information card
and genre analysis plots.
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

from utils import run_installed_query
from utils import user_stats_html
from utils import convert_to_user_stats_df
from utils import get_genre_df


def user_stats(conn, user_id):
    """
    Function for User Statistics page, \
        fetches user information and generates plots

    input ::
        - conn : tigergraph connection object
        - user id : for which plot is generated

    output :: html page containing user information, \
    donut plot of user rated movie genres and bar plot of genres rated above 4
    """

    params = dict()
    params['p'] = user_id

    query_response = run_installed_query(conn, "UserStatistics", params)

    df = convert_to_user_stats_df(query_response)

    genre_df = get_genre_df(df)

    genre_stats = genre_df.sum(numeric_only=True, axis=0)
    genre_index = genre_stats.index.tolist()
    genre_values = genre_stats.values.tolist()

    # code for user stats card
    update_values = [str(user_id), str(query_response[2]['@@movieCountOfP']),
                     str(round(query_response[1]['@@ratingAvg'], 1)),
                     str(max(df['@timestampOfP'])),
                     str(len(genre_values)) + " / 19"]

    html_code = user_stats_html(update_values)
    components.html(html_code, width=995, height=400, scrolling=False)

    st.markdown("<b>Genres user has rated</b>", unsafe_allow_html=True)

    # code for donut plot
    labels = genre_index
    values = genre_values

    # to pull genre most rated
    l = [0] * len(values)
    maxpos = values.index(max(values))
    l[maxpos] = 0.1

    fig = go.Figure(data=[go.Pie(labels=labels, values=values,
                    pull=l, hole=.3)])
    fig.update_layout(title_text='Genre wise rating')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<b>Movies user has rated above 4</b>", unsafe_allow_html=True)

    df_4 = df[df['@ratingByP'] >= 4]
    genre_df_4 = df_4['genres'].str.get_dummies(sep='|')

    genre_stats = genre_df_4.sum(numeric_only=True, axis=0)
    genre_index = genre_stats.index.tolist()
    genre_values = genre_stats.values.tolist()

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
