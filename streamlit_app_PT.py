#pip install streamlit
#streamlit run streamlit_app_PT.py

import streamlit as st
import streamlit.web.cli as stcli
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="TheStatsWay",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('🔍 TheStatsWay - Scouting Talent in Portugal 🔍',
         text_alignment = "center")

df = pd.read_csv('DATA.csv')
df1 = df
df2 = df
df3 = df

#SIDEBAR NAVIGATION
st.sidebar.divider()
st.sidebar.header("🔍 Page Selection 🔍")
st.sidebar.write("")
page = st.sidebar.radio("Pages:", ["Instructions & Abbreviations","Player Stats - Player Overview","Player Stats - Team Overview","Player Comparison Tool"])
st.sidebar.divider()
st.sidebar.write("𝐯𝟏.𝟎.𝟎")
st.sidebar.write("Data Last Updated: Feb 11, 2025")

#PAGE: 1 - Player Overview
if page == "Player Stats - Player Overview":
    st.write("""---""")
    st.title("1 - Player Overview")
    st.write("Browse through the players performance metrics.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    # League Filters
    League_filter1 = st.selectbox("League:", 
                                df1['League'].unique())
    
    df1_LF = df1[df1['League']== League_filter1]

    # Team Filters
    TeamFilter1 = st.multiselect("Team Filter:",
                                options=df1_LF["Team"].unique(),
                                default=df1_LF["Team"].unique())

    if TeamFilter1:
        df1_TF = df1_LF[df1_LF["Team"].isin(TeamFilter1)]

    # Position Filter
    Position_filter1 = st.selectbox("Position:", 
                                df1['Position'].unique())
    
    df1_PF = df1_TF[df1_TF['Position']== Position_filter1]

    
    # Age Filter
    min_age1 = int(df1['Age'].min())
    max_age1 = int(df1['Age'].max())
    
    age_range1 = st.slider("Age Range:",
                        min_value=min_age1,
                        max_value=max_age1,
                        value=(min_age1, max_age1))

    df1_AF = df1_PF[(df1_PF['Age'] >= age_range1[0]) & (df1_PF['Age'] <= age_range1[1])]

    # Grade Filter
    Gradefilter1 = st.multiselect("Grade", 
                                  options=df1_AF['Grade'].unique(), 
                                  default=df1_AF['Grade'].unique())
    df1_GF = df1_AF[df1_AF['Grade'].isin(Gradefilter1)]

    filtered_df1 = df1_GF.sort_values(by=['PosRank'], 
                                    ascending=True)

    st.dataframe(filtered_df1, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)


#PAGE: 0 - Instructions & Abbreviations
elif page == "Instructions & Abbreviations":
    st.write("""---""")
    st.title("0 - Instructions & Abbreviations")
    st.write("")
    st.info("Position Abreviations:", icon="ℹ️")
    st.write("""---
    GK: Goalkeepers
    CB: Centre-Backs
    FB & WB: Full-Backs & Wing-Backs
    MF: Midfielders
    AM & W: Attacking-Mids & Wingers
    CF: Centre-Fowards""")
    st.write("""---""")
    st.info("Grading Values:", icon="ℹ️")
    st.write("""---
    Our Grade value is based on a formula that evaluates player data adjusted for their position group.
    We normalize the data so that we scale the values to a standardized range.
    Therefore, we opted for the following intervals to this Grading System:
             
    S - Elite Output in the Competition
    A - Good Output in the Competition
    B - Above Average Output in the Competition
    C - Average Output in the Competition
    D - Below Average Output in the Competition
    E - Poor Output in the Competition
    F - Very Poor Output in the Competition""")
    st.write("""---""")

#PAGE: 2 - Team Overview
if page == "Player Stats - Team Overview":
    st.write("""---""")
    st.title("2 - Team Overview")
    st.write("Browse through the players performance metrics in a specific team.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    # League Filters
    League_filter2 = st.selectbox("League:", 
                                df2['League'].unique())
    
    df2_LF = df2[df2['League']== League_filter2]

    # Team Filters
    Team_filter2 = st.selectbox("Team:", 
                               df2_LF['Team'].unique())

    df2_TF = df2_LF[df2_LF['Team']== Team_filter2]

    # Position Filters
    Position_Filter2 = st.multiselect("Position Filter:",
                                     options=df2_TF["Position"].unique(),
                                     default=df2_TF["Position"].unique())
    
    df2_PF = df2_TF[df2_TF['Position'].isin(Position_Filter2)]

    # Age Filter
    min_age2 = int(df2['Age'].min())
    max_age2 = int(df2['Age'].max())
    
    age_range2 = st.slider("Age Range:",
                        min_value=min_age2,
                        max_value=max_age2,
                        value=(min_age2, max_age2))

    df2_AF = df2_PF[(df2_PF['Age'] >= age_range2[0]) & (df2_PF['Age'] <= age_range2[1])]

    filtered_df2 = df2_AF.sort_values(by=['PosRank'], 
                                     ascending=True)

    st.dataframe(filtered_df2, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)
    
#PAGE: 3 - PLAYER COMPARATOR
elif page == "Player Comparison Tool":
    st.write("""---""")
    st.title("3 - Player Head-to-Head")
    st.write("Create Performance Radars on the Outfield players based on our 4 metrics: Attack, Possession, Defense, Physical.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    #Dropping GK Data
    df3 = df3[df3.Position != "GK"]
    df3 = df3.drop(columns=['Goalkeeping'])

    #League Filter
    League_filter3 = st.selectbox("League:", 
                                df3['League'].unique())
    
    df3_LF = df3[df3['League']== League_filter3]
    df4_LF = df3[df3['League']== League_filter3]

    #Position Filter
    Position_filter3 = st.selectbox("Position:", 
                                df3['Position'].unique())

    df3_PF = df3_LF[df3_LF['Position']== Position_filter3]
    df4_PF = df4_LF[df4_LF['Position']== Position_filter3]

    #Columns Team
    col1, col2 = st.columns(2)

    with col1:       
        t1 = st.selectbox("Select Team:", 
            df3_PF['Team'].unique())
        
        df3_TF = df3_PF[df3_PF['Team']== t1]

    with col2:
        t2 = st.selectbox("Select Team:", 
                          df4_PF['Team'].unique(), 
                          index=1)
       
        df4_TF = df4_PF[df4_PF['Team']== t2]
    

    #Columns Players
    col3, col4 = st.columns(2)
    
    with col3:       
        p1 = st.selectbox("Select Player 1", 
                          df3_TF['Player'].unique(), 
                          index=0)

    with col4:
        p2 = st.selectbox("Select Player 2", 
                          df4_TF['Player'].unique(), 
                          index=1)


    # Stats for the radar chart
    categories = ['Attack', 'Possession', 'Defense', 'Physical']

    def get_player_stats1(player_name1):
        return df3_TF[df3_TF['Player'] == player_name1][categories].values.flatten().tolist()

    def get_player_stats2(player_name2):
        return df4_TF[df4_TF['Player'] == player_name2][categories].values.flatten().tolist()
    
    stats1 = get_player_stats1(p1)
    stats2 = get_player_stats2(p2)

    #RADAR CHART
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=stats1,
        theta=categories,
        fill='toself',
        name=p1,
        line_color='blue'
    ))
    fig.add_trace(go.Scatterpolar(
        r=stats2,
        theta=categories,
        fill='toself',
        name=p2,
        line_color='red'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"{p1} vs {p2} Performance Radar"
    )

    st.plotly_chart(fig, width="stretch")
    # Comparison Table
    st.subheader("Direct Comparison Table")
    
    comparison_df3 = df3_TF[df3_TF['Player'].isin([p1])].set_index('Player')
    comparison_df4 = df4_TF[df4_TF['Player'].isin([p2])].set_index('Player')
    
    comparison_df = pd.concat([comparison_df3, comparison_df4])

    st.table(comparison_df)

