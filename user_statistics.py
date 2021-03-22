import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

from utils import connect_tg
from utils import run_installed_query
from utils import user_stats_html
from utils import convert_to_user_stats_df
from utils import get_genere_df

def user_stats(user_id):
    """
    Function for User Statistics page, fetches user information and generates plots

    input :: user id

    output :: html page containing user information, donut plot of user rated movie generes and bar plot of generes rated above 4
    """
    
    conn = connect_tg()

    params = dict()
    params['p'] = user_id

    query_response = run_installed_query(conn, "UserStatistics", params)

    df = convert_to_user_stats_df(query_response)

    genere_df = get_genere_df(df)
    
    genere_stats = genere_df.sum(numeric_only=True, axis=0)
    genere_index = genere_stats.index.tolist()
    genere_values = genere_stats.values.tolist()

    # code for user stats card
    update_values = [str(user_id), str(query_response[2]['@@movieCountOfP']), str(round(query_response[1]['@@ratingAvg'], 1)), 
                    str(max(df['@timestampOfP'])), str(len(genere_values))+ " / 19"]

    html_code = user_stats_html(update_values)
    components.html(html_code, width = 995, height = 400,scrolling=False)

    st.markdown("<b>Generes user has rated</b>",unsafe_allow_html=True)

    # code for donut plot
    labels = genere_index
    values = genere_values

    # to pull genere most rated
    l = [0] * len(values)
    maxpos = values.index(max(values))
    l[maxpos] = 0.1

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=l, hole=.3)])
    fig.update_layout(title_text='Genere wise rating')
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("<b>Movies user has rated above 4</b>",unsafe_allow_html=True)

    df_4 = df[df['@ratingByP']>=4]
    genere_df_4 = df_4['genres'].str.get_dummies(sep='|')

    genere_stats = genere_df_4.sum(numeric_only=True, axis=0)
    genere_index = genere_stats.index.tolist()
    genere_values = genere_stats.values.tolist()
    
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