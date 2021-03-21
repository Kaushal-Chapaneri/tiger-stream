import pandas as pd
import graphistry
import streamlit.components.v1 as components
import streamlit as st
from pyvis.network import Network

from utils import connect_tg
from utils import run_installed_query
from utils import convert_to_graphistry_df
from utils import convert_to_pyviz_df
from utils import load_config
from utils import load_html

def graphistry_similar_user(user_id):

    conn = connect_tg()

    config = load_config()

    graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username=config['GRAPHISTRY_USERNAME'], password=config['GRAPHISTRY_PASSWORD'])

    params = dict()

    params['p'] = user_id

    params['k1'] = 10

    query_response = run_installed_query(conn, "SimilarPeople", params)

    df = convert_to_graphistry_df(query_response, user_id)

    iframe_url = graphistry.hypergraph(df)['graph'].plot(render=False)

    components.iframe(iframe_url, width = 800, height = 600,scrolling=False)

@st.cache(allow_output_mutation=True)
def pyviz_prepare_data(user_id):
    
    conn = connect_tg()

    config = load_config()

    params = dict()
    params['p'] = user_id
    params['k1'] = 5

    query_response = run_installed_query(conn, "SimilarPeople", params)

    main_df = convert_to_pyviz_df(query_response, user_id)

    for i in range(len(main_df)):

        params = dict()
        params['p'] = main_df['v_id'][i]
        params['k1'] = 5

        query_response = run_installed_query(conn, "SimilarPeople", params)

        df = convert_to_pyviz_df(query_response, main_df['v_id'][i])

        main_df = main_df.append(df, ignore_index = True)

    return main_df


# @st.cache
def pyviz_plot(df, source_vertex, main_vertices):

    net = Network(height='600px', width='800px', bgcolor='white', font_color='black')

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

    for node in net.nodes:
        node['title'] += '<br>Neighbors: ' + ', '.join(neighbor_map[node['id']])

        if node['id'] == source_vertex:
            node['color'] = '#ef4f4f'
        
        elif node['id'] in main_vertices:
            node['color'] ='#ffcda3'

        else:
            node['color'] ='#74c7b8'
        
        similar = [val['value'] for val in neighbor_values if val['to']==node['id']]
        if similar:
            node['title'] += '<br>Similar movies: '+ similar[0]

    net.set_options('{"nodes": {"borderWidth": 0,"shadow": {"enabled": true}},"edges": {"arrows": {"middle": {"enabled": true}},"color": {"inherit": true},"smooth": false},"interaction": {"hideEdgesOnDrag": true,"hover": true,"navigationButtons": true},"physics": {"enabled": false,"minVelocity": 0.75}}')

    # net.save_graph('asset/'+str(source_vertex)+'_network.html')
    net.write_html('asset/'+str(source_vertex)+'_network.html', notebook=False)


def pyviz_similar_user(user_id):

    df = pyviz_prepare_data(user_id)

    main_vertices = df['v_type'].unique().tolist()
    source_vertex = user_id 
    main_vertices.remove(source_vertex)

    pyviz_plot(df, source_vertex, main_vertices)

    path = "asset/"+str(user_id)+'_network.html'
    html_code = load_html(path)
 
    components.html(html_code, width = 900, height=700)