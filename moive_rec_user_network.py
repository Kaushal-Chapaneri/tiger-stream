import pandas as pd
import graphistry
import streamlit.components.v1 as components
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="kaushalchapaneri_graphistry", password="txhQav6xYxFh6vL")

from utils import connect_tg
from utils import run_installed_query
from utils import convert_to_user_network_df
from utils import connect_graphistry

def find_similar_user(user_id):

    conn = connect_tg()

    params = dict()

    params['p'] = user_id

    params['k1'] = 10

    query_response = run_installed_query(conn, "SimilarPeople", params)

    df = convert_to_user_network_df(query_response, user_id)

    iframe_url = graphistry.hypergraph(df)['graph'].plot(render=False)

    components.iframe(iframe_url, width = 800, height = 800,scrolling=False)