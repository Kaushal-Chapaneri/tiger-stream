"""
filename : TigerStream.py
This script is the starting point for the execution of this project.

command to run : streamlit run TigerStream.py

This file holds the structure of entire project and
calls the necessary function as per requested page.
"""

import streamlit as st

from user_statistics import user_stats
from user_network import graphistry_similar_user
from user_network import pyviz_similar_user
from recommendation import recommended_movies

from utils import header
from utils import connect_tg
from utils import show_data_info
from utils import load_tooltip_text

header()

page = st.sidebar.selectbox("Select a page",
                            ["Overview", "Movie Recommnedation"])

if page == "Overview":

    st.write("")
    st.write("")

    a1 = "<p style='text-align: justify;font-size:20px;'><a style='text-decoration:none' target=_blank href=https://www.tigergraph.com/>TigerGraph</a> is a platform for advanced analytics and machine learning on connected data.\
        Based on the industry’s first and only distributed native graph database, \
        TigerGraph’s proven technology supports advanced analytics and machine learning applications such as fraud detection, anti-money laundering (AML), entity resolution, customer 360, recommendations, knowledge graph, cybersecurity, supply chain, IoT, and network analysis.</p><br>"
    st.markdown(a1, unsafe_allow_html=True)

    a2 = "<p style='text-align: justify;font-size:20px;'>Recently TigerGrpah organized a <a style='text-decoration:none' target=_blank href=https://tigergraph-web-app-hack.devpost.com/>hackathon</a> called <b>TIGERGRAPH WEB-APP HACK</b> with goal to <b>Build a Web-App with TigerGraph using Streamlit & Graphistry.</b> This application is developed for the submission to this hackathon. It required to choose a <a style='text-decoration:none' target=_blank href=https://www.tigergraph.com/starterkits/>starter-kit</a> from 25+ avilable kit and i chose the <b>Recommendation Engine (Movie Recommendation)</b> kit. It is a Graph-based movie recommendation engine built with public data.</p><br>"
    st.markdown(a2, unsafe_allow_html=True)

    a3 ="<p style='text-align: justify;font-size:20px;'><a style='text-decoration:none' target=_blank href=https://streamlit.io//>Streamlit</a> is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.This web-app is entirely developed with Streamlit.</p>" 
    st.markdown(a3, unsafe_allow_html=True)

elif page == "Movie Recommnedation":

    user_id = st.sidebar.text_input('Enter User id')
    tooltip_text = load_tooltip_text()

    try:
        if user_id:
            conn = connect_tg()
            page2 = st.sidebar.selectbox("Select a page",
                                         ["User Statistics",
                                          "User Network", "Recommendation"])

            if page2 == "User Statistics":
                user_stats(conn, user_id, tooltip_text)

            elif page2 == "User Network":
                page3 = st.sidebar.selectbox("Select a graph",
                                             ["Graph 1", "Graph 2"])

                if page3 == "Graph 1":
                    pyviz_similar_user(conn, user_id, tooltip_text)

                else:
                    graphistry_similar_user(conn, user_id, tooltip_text)
            else:
                recommended_movies(conn, user_id, tooltip_text)
        else:
            show_data_info(tooltip_text)

    except Exception as e:

        st.error('There is some error in processing this request')
        check = st.checkbox("I'm King of NERd, show me the trace")
        if check:
            st.write(e)
