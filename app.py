import streamlit as st

from moive_rec_user_stats import user_statistics
from moive_rec_user_network import find_similar_user

page = st.sidebar.selectbox("Select a page", ["Overview", "Movie Recommnedation"])

if page == "Overview":

    pass

elif page == "Movie Recommnedation":

    page2 = st.sidebar.selectbox("Select a page", ["User Statistics", "User Network", "Recommendation"])

    user_id = st.sidebar.text_input('Enter User id')

    if user_id:

        if page2 == "User Statistics":

            user_statistics(user_id)

        if page2 == "User Network":

            find_similar_user(user_id)