#streamlit run streamlit_app_PT.py
import streamlit as st
import streamlit.web.cli as stcli
import pandas as pd
import numpy as np
import plotly as plt
import plotly.graph_objects as go
import plotly.express as px
from mplsoccer import VerticalPitch
import matplotlib.pyplot as plt
import io
import seaborn as sns

st.set_page_config(
    page_title="TheStatsWay",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title('🔍 TheStatsWay - Scouting Talent in Portugal 🔍',
         text_alignment = "center")

df = pd.read_csv('DATA.csv')

def get_grade_color(grade):
    if grade == "S":
        return '#1b5e20' # Elite
    elif grade == "A":
        return "#36A348" # Good
    elif grade == "B":
        return "#89ff3b" # Above Average
    elif grade == "C":
        return "#eafb00" # Average
    elif grade == "D":
        return '#fb8c00' # Below Average
    elif grade == "E":
        return "#fb6400" # Poor
    elif grade == "F":
        return "#f43636" # Very Poor
    else:
        return "#3936f4" # Error

def style_grade_column(val):
    color = get_grade_color(val)
    text_color = "white" if val in ["S", "A", "E", "F"] else "black"
    return f'background-color: {color}; color: {text_color}; font-weight: bold;'

grade_order = ['S', 'A', 'B', 'C', 'D', 'E', 'F']

st.sidebar.divider()
st.sidebar.header("🔍 Page Selection 🔍")
st.sidebar.write("")
page = st.sidebar.radio("Pages:", ["Instructions & Abbreviations","Player Stats - Player Overview","Player Stats - Team Overview","Player Comparison Tool","Lineup Builder","Graph - Simple Plot","Graph - Interactive Plot"])
st.sidebar.divider()
st.sidebar.write("𝐯𝟏.𝟎.𝟎𝟐")
st.sidebar.write("Data Last Updated: Feb 11, 2025")

df1 = df
df2 = df
df3 = df
df4 = df
df5 = df
df6 = df

if page == "Instructions & Abbreviations":
    st.write("""---""")
    st.title("0 - Instructions & Abbreviations")
    st.write("")
    st.info("Position Abreviations:", icon="ℹ️")
    st.write("""---
    Position Group:
             
    GK: Goalkeepers
    CB: Centre-Backs
    FB & WB: Full-Backs & Wing-Backs
    MF: Midfielders
    AM & W: Attacking-Mids & Wingers
    CF: Centre-Fowards""")
    st.write("""---""")
    st.info("Player Output Metrics:", icon="ℹ️")
    st.write("""---
    The Player Output Metrics are calculation values adjusted for their position group.
    To calculate our outputs, we have done calculations based on the variables & weights that fall within each area that we considered relevant to that analysis.
             
    Example:
        A Player (Centre-Back) with a High Goal-Scoring Output is one of the best players in his position group (CB) for that metric.""")
    st.write("""---""")
    st.info("Grading Values:", icon="ℹ️")
    st.write("""---
    Our Grade value is based on a formula that evaluates player data (our Player Metrics) adjusted for their position group.
    We normalize the data so that we scale the values to a standardized range.
    Therefore, we opted for the following intervals to this Grading System and respective colors:
             
    S - Elite Output in the Competition (Dark Green)
    A - Good Output in the Competition (Green)
    B - Above Average Output in the Competition (Light Green)
    C - Average Output in the Competition (Yellow)
    D - Below Average Output in the Competition (Orange)
    E - Poor Output in the Competition (Dark Orange)
    F - Very Poor Output in the Competition (Red)""")
    st.write("""---""")

elif page == "Player Stats - Player Overview":
    st.write("""---""")
    st.title("1 - Player Overview")
    st.write("Browse through the players performance metrics.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    Season_filter1 = st.selectbox("Season:", 
                                df1['Season'].unique())
    
    df1_SF = df1[df1['Season']== Season_filter1]

    League_filter1 = st.selectbox("League:", 
                                df1_SF['League'].unique())
    
    df1_LF = df1_SF[df1_SF['League']== League_filter1]

    teams1 = df1_LF['Team'].unique().tolist()
    sorted_teams1 = sorted(teams1)
    TeamFilter1 = st.multiselect("Team Filter:",
                                 options=sorted_teams1,
                                default=sorted_teams1)

    if TeamFilter1:
        df1_TF = df1_LF[df1_LF["Team"].isin(TeamFilter1)]
    
    Position_filter1 = st.selectbox("Position:", 
                                df1_TF['Position'].unique())
    
    df1_PF = df1_TF[df1_TF['Position']== Position_filter1]

    min_age1 = int(df1_PF['Age'].min())
    max_age1 = int(df1_PF['Age'].max())
    
    age_range1 = st.slider("Age Range:",
                        min_value=min_age1,
                        max_value=max_age1,
                        value=(min_age1, max_age1))

    df1_AF = df1_PF[(df1_PF['Age'] >= age_range1[0]) & (df1_PF['Age'] <= age_range1[1])]

    unique_grade1 = df['Grade'].unique().tolist()

    sorted_grades1 = sorted(unique_grade1, 
                            key=lambda x: grade_order.index(x) if x in grade_order else 999)

    Gradefilter1 = st.multiselect("Grade", 
                                  options=sorted_grades1,
                                  default=sorted_grades1)

    df1_GF = df1_AF[df1_AF['Grade'].isin(Gradefilter1)]
  
    df1_GF['Grade'] = pd.Categorical(df1_GF['Grade'], categories=grade_order, ordered=True)
    filtered_df1 = df1_GF.sort_values(by=['Grade','PosRank'],ascending=True).reset_index(drop=True)

    styled_df = filtered_df1.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical','Goalkeeping'])

    st.dataframe(styled_df, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)

elif page == "Player Stats - Team Overview":
    st.write("""---""")
    st.title("2 - Team Overview")
    st.write("Browse through the players performance metrics in a specific team.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Player Settings")

    Season_filter2 = st.selectbox("Season:", 
                                df2['Season'].unique())
    
    df2_SF = df2[df2['Season']== Season_filter2]

    League_filter2 = st.selectbox("League:", 
                                df2_SF['League'].unique())
    
    df2_LF = df2_SF[df2_SF['League']== League_filter2]

    teams2 = df2_LF['Team'].unique().tolist()
    sorted_teams2 = sorted(teams2)

    Team_filter2 = st.selectbox("Team:", 
                                options=sorted_teams2)

    df2_TF = df2_LF[df2_LF['Team']== Team_filter2]

    Position_Filter2 = st.multiselect("Position Filter:",
                                     options=df2_TF["Position"].unique(),
                                     default=df2_TF["Position"].unique())
    
    df2_PF = df2_TF[df2_TF['Position'].isin(Position_Filter2)]

    min_age2 = int(df2_PF['Age'].min())
    max_age2 = int(df2_PF['Age'].max())
    
    age_range2 = st.slider("Age Range:",
                        min_value=min_age2,
                        max_value=max_age2,
                        value=(min_age2, max_age2))

    df2_AF = df2_PF[(df2_PF['Age'] >= age_range2[0]) & (df2_PF['Age'] <= age_range2[1])]

    df2_AF['Grade'] = pd.Categorical(df2_AF['Grade'], categories=grade_order, ordered=True)
    filtered_df2 = df2_AF.sort_values(by=['Grade','PosRank'],ascending=True).reset_index(drop=True)

    styled_df2 = filtered_df2.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical','Goalkeeping'])
    
    st.dataframe(styled_df2, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)
    
elif page == "Player Comparison Tool":
    st.write("""---""")
    st.title("3 - Player Head-to-Head")
    st.write("Create a performance radar comparison on the outfield players based on our 4 metrics: Attack, Possession, Defense, Physical.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Player Settings")
    df3 = df3[df3.Position != "GK"]
    df3 = df3.drop(columns=['Goalkeeping'])

    Season_filter3 = st.selectbox("Season:", 
                                df3['Season'].unique())
    
    df3_SF = df3[df3['Season']== Season_filter3]

    League_filter3 = st.selectbox("League:", 
                                df3_SF['League'].unique())
    
    df3_LF = df3_SF[df3_SF['League']== League_filter3]
    df4_LF = df3_SF[df3_SF['League']== League_filter3]

    Position_filter3 = st.selectbox("Position:", 
                                df3['Position'].unique())

    df3_PF = df3_LF[df3_LF['Position']== Position_filter3]
    df4_PF = df4_LF[df4_LF['Position']== Position_filter3]

    teams3 = df3_PF['Team'].unique().tolist()
    sorted_teams3 = sorted(teams3)

    teams4 = df4_PF['Team'].unique().tolist()
    sorted_teams4 = sorted(teams4)

    col1, col2 = st.columns(2)

    with col1:       
        t1 = st.selectbox("Select Team:", 
                          options=sorted_teams3)
        
        df3_TF = df3_PF[df3_PF['Team']== t1]

    with col2:
        t2 = st.selectbox("Select Team:", 
                          sorted_teams4,
                          index=1)
       
        df4_TF = df4_PF[df4_PF['Team']== t2]
    
    players3 = df3_TF['Player'].unique().tolist()
    sorted_players3 = sorted(players3)

    players4 = df4_TF['Player'].unique().tolist()
    sorted_players4 = sorted(players4)
    
    col3, col4 = st.columns(2)
    
    with col3:       
        p1 = st.selectbox("Select Player 1", 
                          sorted_players3, 
                          index=0)

    with col4:
        p2 = st.selectbox("Select Player 2", 
                          sorted_players4, 
                          index=1)

    categories = ['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical']

    def get_player_stats1(player_name1):
        return df3_TF[df3_TF['Player'] == player_name1][categories].values.flatten().tolist()

    def get_player_stats2(player_name2):
        return df4_TF[df4_TF['Player'] == player_name2][categories].values.flatten().tolist()
    
    stats1 = get_player_stats1(p1)
    stats2 = get_player_stats2(p2)

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
    st.subheader("Direct Comparison Table")
    
    comparison_df3 = df3_TF[df3_TF['Player'].isin([p1])].set_index('Player')
    comparison_df4 = df4_TF[df4_TF['Player'].isin([p2])].set_index('Player')
    comparison_df = pd.concat([comparison_df3, comparison_df4])

    styled_df3 = comparison_df.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical'])
    
    st.dataframe(styled_df3, 
                 width="stretch", 
                 hide_index=True,
                 height = 110)

elif page == "Lineup Builder":
    st.write("""---""")
    st.title("4 - Build Your Teams Eleven")
    st.write("Create a teams lineup graph with their grades.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    
    formations = {
    "4-3-3": {
        "GK": (11, 40),
        "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
        "RCM": (64, 60),"CM": (52, 40),"LCM": (64, 20),
        "RW": (85, 67),"CF": (100, 40),"LW": (85, 13),
    },
    "4-4-2": {
        "GK": (11, 40),
        "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
        "RCM": (60, 55),"LCM": (60, 25), "RM": (74, 67),"LM": (74, 13),
        "RS": (100, 55), "LS": (100, 25)
    },
     "4-2-3-1": {
        "GK": (11, 40),
        "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
        "RCM": (60, 55),"LCM": (60, 25),
        "RW": (85, 67), "AM": (85, 40), "LW": (85, 13),
        "CF": (100, 40)
    },
    "5-2-2-1": {
        "GK": (11, 40),
        "RCB": (33, 60), "CCB": (26,40), "LCB": (33, 20), "RWB": (48, 70), "LWB": (48, 10),
        "RCM": (60, 55), "LCM": (60, 25),
        "RW": (85, 67), "LW": (85, 13),
        "CF": (100, 40)
    }}

    PositionIndex = {
         "GK": "GK",
         "CCB": "CB",
         "RCB": "CB",
         "LCB": "CB",
         "LB": "FB & WB",
         "RB": "FB & WB",
         "LWB": "FB & WB",
         "RWB": "FB & WB",
         "CM": "MF",
         "RCM": "MF",
         "LCM": "MF",
         "LM": "AM & W",
         "RM": "AM & W",
         "AM": "AM & W",
         "LW": "AM & W",
         "RW": "AM & W",
         "LS": "CF",
         "RS": "CF",
         "CF": "CF"
    }

    st.subheader("🛠️ Lineup Settings")

    Season_filter4 = st.selectbox("Season:", 
                                df4['Season'].unique())
    
    df4_SF = df4[df4['Season']== Season_filter4]

    League_filter4 = st.selectbox("League:", 
                                df4_SF['League'].unique())
    
    df4_LF = df4_SF[df4_SF['League']== League_filter4]

    teams4 = df4_LF['Team'].unique().tolist()
    sorted_teams4 = sorted(teams4)

    Team_filter4 = st.selectbox("Team:", 
                                options=sorted_teams4)
    
    df4_TF = df4_LF[df4_LF['Team']== Team_filter4]

    if 'current_formation' not in st.session_state:
        st.session_state.current_formation = "4-3-3"
    if 'lineup' not in st.session_state:
        st.session_state.lineup = {}

    def reset_lineup():
        st.session_state.lineup = {}

    st.subheader("📋 Select Your Eleven")

    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")

    footer_tag = "@TheStatsWay"

    selected_formation = st.selectbox("Choose Formation", 
                                    options=list(formations.keys()), 
                                    on_change=reset_lineup)


    plot_data = {}

    for pos,coords in formations[selected_formation].items():

        broad_category = PositionIndex.get(pos)
    
        filtered_players = df4_TF[df4_TF['Position'] == broad_category]['Player'].tolist()

        taken_elsewhere = [name for p, name in st.session_state.lineup.items() if p != pos]
        available = [p for p in filtered_players if p not in taken_elsewhere]

        current_selection = st.session_state.lineup.get(pos, "Select Player")
        
        if current_selection not in available:
            current_selection = "Select Player"

        choice = st.selectbox(f"{pos}", 
                            options=["Select Player"] + available,
                            index=0 if current_selection == "Select Player" else available.index(current_selection) + 1,
                            key=f"sel_{selected_formation}_{pos}")

        if choice != "Select Player":
            st.session_state.lineup[pos] = choice
            grade = df4_TF[df4_TF['Player'] == choice]['Grade'].iloc[0]
            plot_data[pos] = {"name": choice, 
                              "grade": grade, 
                              "x": coords[0], 
                              "y": coords[1]}
        
    st.title(f"Formation Selected: {selected_formation}")

    pitch = VerticalPitch(pitch_type='statsbomb', 
                          pitch_color="#1a7953", 
                          line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(6, 7))

    for pos, info in plot_data.items():

        grade_color = get_grade_color(info['grade'])
        ax.set_title(f"{Team_filter4} - {Team_filter4} - {selected_formation}", color='Black', fontsize=16, fontweight='bold', pad=20)
        ax.text(0.92, 0.98, "https://thestatsway-scouting-talent-in-portugal-app.streamlit.app/", transform=ax.transAxes, 
        color='Black', fontsize=7, fontweight='bold',
        ha='right', va='bottom', alpha=0.7)
                
        pitch.scatter(info['x'], 
                      info['y'], 
                      c=grade_color,
                      s=800,  
                      edgecolors='white', 
                      linewidth=1, 
                      ax=ax, 
                      zorder=3)
    
        pitch.annotate(str(info['grade']), 
                    xy=(info['x'], info['y']), 
                    va='center', ha='center', 
                    color='black', fontsize=14, fontweight='bold', ax=ax, zorder=4)
        
        pitch.annotate(info['name'], xy=(info['x'] - 6, info['y']), 
                    va='center', ha='center', color='black', 
                    fontsize=10, fontweight='bold', ax=ax, zorder=4)
    
        pitch.annotate(pos, xy=(info['x'] - 9, info['y']), 
                    va='center', ha='center', color="black",
                    fontsize=9, ax=ax, zorder=4)
        
        pitch.annotate(pos, 
                    xy=(info['x'] - 9, info['y']), 
                    va='center', ha='center', color="black",
                    fontsize=9, ax=ax, zorder=4)

        ax.text(0.9475, 0.04, footer_tag, transform=ax.transAxes, 
        color='Black', fontsize=7, fontweight='bold',
        ha='right', va='bottom', alpha=0.7)

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Lineup Image",
            data=buf.getvalue(),
            file_name=f"{Team_filter4}_lineup.png",
            mime="image/png")
    
elif page == "Graph - Simple Plot":
    st.write("""---""")
    st.title("5 - Build Your Graph")
    st.write("Create a graph with the desired combination of the variables.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")
    
    df5 = df5[df5.Position != "GK"]
    df5 = df5.drop(columns=['Goalkeeping'])

    Season_filter5 = st.selectbox("Season:", 
                                df5['Season'].unique())
    
    df5_SF = df5[df5['Season']== Season_filter5]

    League_filter5 = st.selectbox("League:", 
                                df5_SF['League'].unique())
    
    df5_LF = df5_SF[df5_SF['League']== League_filter5]

    Position_filter5 = st.selectbox("Position:", 
                                df5_LF['Position'].unique())
    
    df5_PF = df5_LF[df5_LF['Position']== Position_filter5]

    min_age5 = int(df5_PF['Age'].min())
    max_age5 = int(df5_PF['Age'].max())
    
    age_range5 = st.slider("Age Range:",
                        min_value=min_age5,
                        max_value=max_age5,
                        value=(min_age5, max_age5))

    df5_AF = df5_PF[(df5_PF['Age'] >= age_range5[0]) & (df5_PF['Age'] <= age_range5[1])]

    teams5 = df5_AF['Team'].unique().tolist()
    sorted_teams5 = sorted(teams5)
    TeamFilter5 = st.multiselect("Team Filter:",
                                options=sorted_teams5,
                                default=sorted_teams5)

    if TeamFilter5:
        df5_TF = df5_AF[df5_AF["Team"].isin(TeamFilter5)]

    st.subheader("📊 Plot Settings")
    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")
    allowed_metrics = ["Goal-Scoring","Attack", "Possession", "Defense","Physical","Age"]
    variables = [m for m in allowed_metrics if m in df5_TF.columns]
    
    x_axis1 = st.selectbox("X-Axis (Horizontal)", 
                        variables, 
                        index=0)

    y_axis1 = st.selectbox("Y-Axis (Vertical)", 
                                  variables, 
                                  index=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#333333")
    ax.set_facecolor("#f7f7f7")

    for i, row in df5_TF.iterrows():
        ax.scatter(row[x_axis1], row[y_axis1], 
                color= get_grade_color(row['Grade']), 
                s=200, 
                edgecolors='black', 
                alpha=0.8)
        
        ax.text(row[x_axis1], row[y_axis1]-2.5, 
                row['Player'], 
                color='black', 
                ha='center', fontsize=7)

    ax.set_title(f"{Position_filter5}s in {League_filter5}: {x_axis1} & {y_axis1} Analysis", color='white', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel(x_axis1, color='white', fontsize=12,fontweight='bold')
    ax.set_ylabel(y_axis1, color='white', fontsize=12,fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)

    plt.figtext(0.9, 0.02, "@TheStatsWay", ha="right", fontsize=10, color='White', fontweight='bold')
    plt.figtext(0.35, 0.01, "https://thestatsway-scouting-talent-in-portugal-app.streamlit.app/",ha="right", fontsize=6, color='White', fontweight='bold')
    
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Lineup Image",
            data=buf.getvalue(),
            file_name=f"{League_filter5}_{Position_filter5}_{x_axis1}_{y_axis1}_Analysis.png",
            mime="image/png")
    
elif page == "Graph - Interactive Plot":
    st.write("""---""")
    st.title("6 - Build Your Graph")
    st.write("Create an interactive graph with the desired combination of the variables.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    Season_filter6 = st.selectbox("Season:", 
                                df5['Season'].unique())
    
    df6_SF = df6[df6['Season']== Season_filter6]

    League_filter6 = st.selectbox("League:", 
                                df6_SF['League'].unique())
    
    df6_LF = df6_SF[df6_SF['League']== League_filter6]

    Position_filter6 = st.selectbox("Position:", 
                                df6_LF['Position'].unique())
    
    df6_PF = df6_LF[df6_LF['Position']== Position_filter6]

    variables = df6_PF.select_dtypes(include=['float64', 'int64']).columns.tolist()

    st.subheader("📊 Plot Settings")
    st.write("Map your variables to the chart axes:")

    x_axis = st.selectbox("X-Axis (Horizontal)", 
                        variables, 
                        index=0)

    y_axis = st.selectbox("Y-Axis (Vertical)", 
                                  variables, 
                                  index=1)
    
    size_var = st.selectbox("Bubble Size", 
                            variables, 
                            index=2)
    
    color_var = st.selectbox("Bubble Color", 
                            variables,
                            index=3)

    st.subheader("⚽ Data Explorer")
    st.write(f"Analyzing **{x_axis}** vs **{y_axis}** (Size: {size_var}, Color: {color_var})")

    fig = px.scatter(
        df6_PF,
        x=x_axis,
        y=y_axis,
        size=size_var,
        color=color_var,
        hover_name="Player",
        text="Player",
        size_max=40,
        color_continuous_scale=px.colors.sequential.Viridis,
        template="simple_white"
    )

    fig.update_traces(textposition='top center')

    st.plotly_chart(fig, width='stretch')

    with st.expander("View Raw Data"):
        st.dataframe(df6_PF)
