import streamlit as st

from moive_rec_user_stats import user_statistics

page = st.sidebar.selectbox("Select a page", ["Overview", "Movie Recommnedation"])

if page == "Overview":

    pass

elif page == "Movie Recommnedation":

    page2 = st.sidebar.selectbox("Select a page", ["User Statistics", "User Network", "Recommendation"])

    user_id = st.sidebar.selectbox("Select a user", [1,2,3,4])

    if page2 == "User Statistics":

        user_statistics(user_id)

