"""
filename : user_network.py

Page : User Network

This script displays network graph of similar people of input user, \
     generates Graphistry plot and pyviz plot
"""

import graphistry
import streamlit.components.v1 as components
import streamlit as st
from pyvis.network import Network

from utils import run_installed_query
from utils import convert_to_graphistry_df
from utils import convert_to_pyviz_df
from utils import load_config
from utils import load_html
from utils import tooltip


def pyviz_prepare_data(conn, query_response, user_id,
                       second_level, user_number):
    """
    Function used in SimilarPeople to prepare data for graph plot using pyviz

    input ::
        - conn : tigergraph connection object
        - query_response : query response received for similar people query
        - user_id : user id for which data is fetched
        - second_level : boolean generate second level plot if True
        - user_number : no. of similar user in plot

    output :: dataframe of query response
    """

    main_df = convert_to_pyviz_df(query_response, user_id)

    if second_level:

        for i in range(len(main_df)):

            params = dict()
            params['p'] = main_df['v_id'][i]
            params['k1'] = user_number

            query_response = run_installed_query(conn, "SimilarPeople", params)

            df = convert_to_pyviz_df(query_response, main_df['v_id'][i])

            main_df = main_df.append(df, ignore_index=True)

    return main_df


def pyviz_plot(df, source_vertex, main_vertices, effect):
    """
    Function to generate plot of similar people network using pyviz

    input ::
        - df : datafame of query response
        - source_vertex : id of source vertx i.e user id
        - main_vertices : ids of first level neighbour of source vertex
        - effect : boolean apply physics effect if True

    output :: html file under asset/user_network containing plot for given user
    """

    net = Network(height='600px', width='800px',
                  bgcolor='white', font_color='black')

    data = df

    sources = data['v_type']
    targets = data['v_id']
    weights = data['movieCount']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:

        src = e[0]
        dst = e[1]
        w = e[2]

        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst)
        net.add_edge(src, dst, value=w)

    neighbor_map = net.get_adj_list()
    neighbor_values = net.get_edges()

    # code for information shown on hover effect, and decides color of a node
    for node in net.nodes:
        node['title'] += '<br>Neighbors: ' + ', '.join(neighbor_map[node['id']])

        if node['id'] == source_vertex:
            node['color'] = '#ef4f4f'
        elif node['id'] in main_vertices:
            node['color'] = '#ffcda3'

        else:
            node['color'] = '#74c7b8'

        similar = [val['value'] for val in neighbor_values if val['to'] == node['id']]
        if similar:
            node['title'] += '<br>Similar movies: ' + similar[0]

    # Enable/Disable physics effects in pyviz plot, see difference in physics key in below json
    if effect:
        net.set_options('{"nodes": {"borderWidth": 0,"shadow": {"enabled": true}},"edges": {"arrows": {"middle": {"enabled": true}},"color": {"inherit": true},"smooth": false},"interaction": {"hideEdgesOnDrag": true,"hover": true,"navigationButtons": true},"physics": {"enabled": true,"minVelocity": 0.75}}')
    else:
        net.set_options('{"nodes": {"borderWidth": 0,"shadow": {"enabled": true}},"edges": {"arrows": {"middle": {"enabled": true}},"color": {"inherit": true},"smooth": false},"interaction": {"hideEdgesOnDrag": true,"hover": true,"navigationButtons": true},"physics": {"enabled": false,"minVelocity": 0.75}}')

    net.write_html('asset/user_network/' + str(source_vertex) + '_network.html', notebook=False)


def pyviz_similar_user(conn, user_id, tooltip_text):
    """
    Function for Graph 1 Page, generates plot using pyviz

    input ::
        - conn : tigergraph connection object
        - user id for which plot is generated

    output :: Similar User network graph plot
    """

    st.markdown(tooltip("<b>Similar user network</b>",
                tooltip_text["similar_user"]),
                unsafe_allow_html=True)

    user_number = st.slider("Select no. of similar users", 5, 10)

    left, right = st.beta_columns(2)
    with left:
        second_level = st.checkbox('Second level users')
    with right:
        effect = st.checkbox('Apply Physics')

    params = dict()
    params['p'] = user_id
    params['k1'] = user_number

    query_response = run_installed_query(conn, "SimilarPeople", params)

    df = pyviz_prepare_data(conn, query_response, user_id,
                            second_level, user_number)

    main_vertices = df['v_type'].unique().tolist()
    source_vertex = user_id
    main_vertices.remove(source_vertex)

    pyviz_plot(df, source_vertex, main_vertices, effect)

    path = "asset/user_network/"+str(user_id)+'_network.html'
    html_code = load_html(path)

    components.html(html_code, width=900, height=700)


def graphistry_similar_user(conn, user_id, tooltip_text):
    """
    Function for Graph 2 page in User Network page, \
        Graphistry Visualization function for similar user

    input ::
        - conn : tigergraph connection object
        - user id for which plot is generated

    output :: Graphistry plot for given user with selected range of similar user
    """

    config = load_config()

    st.markdown(tooltip("<b>Similar user network with Graphistry</b><br>",
                tooltip_text["similar_user_graphistry"]),
                unsafe_allow_html=True)

    user_number = st.slider("Select Number of Similar Users", 5, 10)

    graphistry.register(api=3, protocol="https",
                        server="hub.graphistry.com",
                        username=config['GRAPHISTRY_USERNAME'],
                        password=config['GRAPHISTRY_PASSWORD'])

    params = dict()
    params['p'] = user_id
    params['k1'] = user_number

    query_response = run_installed_query(conn, "SimilarPeople", params)

    df = convert_to_graphistry_df(query_response, user_id)

    iframe_url = graphistry.hypergraph(df)['graph'].plot(render=False)

    components.iframe(iframe_url, width=800, height=600, scrolling=False)
