import streamlit as st
import plotly.graph_objects as go
from math import ceil

from utils import connect_tg
from utils import run_installed_query
from utils import convert_to_user_rec_df
from utils import get_genere_df
from utils import filter_results
from utils import download_file
from utils import adjust_style

def recommended_movies(user_id):
    """
    Function for Recommendation page, shows recommended movie table and plot of recommende genere count bar plot

    input :: user id

    output :: table of recommendations with button to save as table as csv and bar plot of genere count
    """
    
    conn = connect_tg()

    st.markdown("<b>Recommended Movies</b>",unsafe_allow_html=True)

    user_num = st.slider("Select Number of User", 5, 100)

    similar_movies = st.slider("Select Number of Similar Movies", 5, 100)

    st.write("")

    params = dict()
    params['p'] = user_id
    params['k1'] = user_num
    params['k2'] = similar_movies

    query_response = run_installed_query(conn, "RecommendMovies", params)

    df = convert_to_user_rec_df(query_response)

    df.reset_index(inplace=True,drop=True)
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

    filename = str(user_id)+"_recommended_movie.csv"
    download_button_str = download_file(df, filename)
    st.markdown(download_button_str, unsafe_allow_html=True)

    genere_df = get_genere_df(df)

    genere_stats = genere_df.sum(numeric_only=True, axis=0)
    genere_index = genere_stats.index.tolist()
    genere_values = genere_stats.values.tolist()

    st.write("")
    st.markdown("<b>Recommended generes</b>",unsafe_allow_html=True)
    colors = ['cornflowerblue',] * len(genere_index)
    maxval = max(genere_values)
    ind = [i for i, v in enumerate(genere_values) if v == maxval]

    for i in ind:
        colors[i] = 'green'
        layout = dict(
            xaxis= dict(title= 'Genere',ticklen= 5,zeroline= False),
            yaxis= dict(title= 'No. of ratings',ticklen= 5,zeroline= False)
            )

    fig = go.Figure(data=[go.Bar(
            x=genere_index,
            y=genere_values,
            marker_color=colors # marker color can be a single color value or an iterable
        )],layout=layout)
    fig.update_layout(title_text='Genere wise movie rating count')
    st.plotly_chart(fig,use_container_width=True)

    href = f"""<a href="#top">Back to top</a>"""
    st.markdown(href,unsafe_allow_html=True)
