import streamlit as st

from moive_rec_user_stats import user_statistics
from moive_rec_user_network import graphistry_similar_user
from moive_rec_user_network import pyviz_similar_user

page = st.sidebar.selectbox("Select a page", ["Overview", "Movie Recommnedation"])

if page == "Overview":

    pass

elif page == "Movie Recommnedation":

    page2 = st.sidebar.selectbox("Select a page", ["User Statistics", "User Network", "Recommendation"])

    user_id = st.sidebar.text_input('Enter User id')

    if user_id:

        if page2 == "User Statistics":

            user_statistics(user_id)

        elif page2 == "User Network":

            page3 = st.sidebar.selectbox("Select a graph", ["Graph 1", "Graph 2"])

            if page3 == "Graph 1":

                pyviz_similar_user(user_id)

            else:
                graphistry_similar_user(user_id)

        else:

            pass

    else:

        pass