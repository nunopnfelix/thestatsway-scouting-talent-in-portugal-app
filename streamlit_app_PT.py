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
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

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
page = st.sidebar.radio("Pages:", ["Instructions & Abbreviations","Player Stats - Player Overview","Player Stats - Team Overview","Player Comparison Tool","Lineup Builder","Graph - Simple Plot","Graph - Interactive Plot","Player Report Card","Player Similarity Tool"])
st.sidebar.divider()
st.sidebar.write("𝐯𝟏.𝟎.𝟎𝟒")
st.sidebar.write("Data Last Updated: Feb 11, 2025")

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

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)
    TeamFilter = st.multiselect("Team Filter:",
                                options=sorted_teams,
                                default=sorted_teams)

    if TeamFilter:
        df_TF = df_LF[df_LF["Team"].isin(TeamFilter)]
    
    Position_filter = st.selectbox("Position:", 
                                df_TF['Position'].unique())
    
    df_PF = df_TF[df_TF['Position']== Position_filter]

    min_age = int(df_PF['Age'].min())
    max_age = int(df_PF['Age'].max())
    
    age_range = st.slider("Age Range:",
                        min_value=min_age,
                        max_value=max_age,
                        value=(min_age, max_age))

    df_AF = df_PF[(df_PF['Age'] >= age_range[0]) & (df_PF['Age'] <= age_range[1])]

    unique_grade = df['Grade'].unique().tolist()

    sorted_grades = sorted(unique_grade, 
                            key=lambda x: grade_order.index(x) if x in grade_order else 999)

    Gradefilter = st.multiselect("Grade", 
                                  options=sorted_grades,
                                  default=sorted_grades)

    df_GF = df_AF[df_AF['Grade'].isin(Gradefilter)]
  
    df_GF['Grade'] = pd.Categorical(df_GF['Grade'], categories=grade_order, ordered=True)
    filtered_df = df_GF.sort_values(by=['Grade','PosRank'],ascending=True).reset_index(drop=True)

    styled_df = filtered_df.style.map(style_grade_column, subset=['Grade'])\
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

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)

    df_TF = df_LF[df_LF['Team']== Team_filter]

    Position_Filter = st.multiselect("Position Filter:",
                                     options=df_TF["Position"].unique(),
                                     default=df_TF["Position"].unique())
    
    df_PF = df_TF[df_TF['Position'].isin(Position_Filter)]

    min_age = int(df_PF['Age'].min())
    max_age = int(df_PF['Age'].max())
    
    age_range = st.slider("Age Range:",
                        min_value=min_age,
                        max_value=max_age,
                        value=(min_age, max_age))

    df_AF = df_PF[(df_PF['Age'] >= age_range[0]) & (df_PF['Age'] <= age_range[1])]

    df_AF['Grade'] = pd.Categorical(df_AF['Grade'], categories=grade_order, ordered=True)
    filtered_df = df_AF.sort_values(by=['Grade','PosRank'],ascending=True).reset_index(drop=True)

    styled_df = filtered_df.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical','Goalkeeping'])
    
    st.dataframe(styled_df, 
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
    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df3_LF = df_SF[df_SF['League']== League_filter]
    df4_LF = df_SF[df_SF['League']== League_filter]

    Position_filter3 = st.selectbox("Position:", 
                                df['Position'].unique())

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

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)
    
    df_TF = df_LF[df_LF['Team']== Team_filter]

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
    
        filtered_players = df_TF[df_TF['Position'] == broad_category]['Player'].tolist()

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
            grade = df_TF[df_TF['Player'] == choice]['Grade'].iloc[0]
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
        ax.set_title(f"{Season_filter} - {Team_filter} - {selected_formation}", color='Black', fontsize=14, fontweight='bold', pad=20)
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
            file_name=f"{Team_filter}_lineup.png",
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
    
    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    Position_filter = st.selectbox("Position:", 
                                df_LF['Position'].unique())
    
    df_PF = df_LF[df_LF['Position']== Position_filter]

    min_age = int(df_PF['Age'].min())
    max_age = int(df_PF['Age'].max())
    
    age_range = st.slider("Age Range:",
                        min_value=min_age,
                        max_value=max_age,
                        value=(min_age, max_age))

    df_AF = df_PF[(df_PF['Age'] >= age_range[0]) & (df_PF['Age'] <= age_range[1])]

    teams = df_AF['Team'].unique().tolist()
    sorted_teams = sorted(teams)
    TeamFilter = st.multiselect("Team Filter:",
                                options=sorted_teams,
                                default=sorted_teams)

    if TeamFilter:
        df5_TF = df_AF[df_AF["Team"].isin(TeamFilter)]

    st.subheader("📊 Plot Settings")
    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")
    allowed_metrics = ["Goal-Scoring","Attack", "Possession", "Defense","Physical","Age"]
    variables = [m for m in allowed_metrics if m in df5_TF.columns]
    
    x_axis = st.selectbox("X-Axis (Horizontal)", 
                        variables, 
                        index=0)

    y_axis = st.selectbox("Y-Axis (Vertical)", 
                                  variables, 
                                  index=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#333333")
    ax.set_facecolor("#f7f7f7")

    for i, row in df5_TF.iterrows():
        ax.scatter(row[x_axis], row[y_axis], 
                color= get_grade_color(row['Grade']), 
                s=200, 
                edgecolors='black', 
                alpha=0.8)
        
        ax.text(row[x_axis], row[y_axis]-2.5, 
                row['Player'], 
                color='black', 
                ha='center', fontsize=7)

    ax.set_title(f"{Position_filter}s in {League_filter}: {x_axis} & {y_axis} Analysis", color='white', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel(x_axis, color='white', fontsize=12,fontweight='bold')
    ax.set_ylabel(y_axis, color='white', fontsize=12,fontweight='bold')
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
            file_name=f"{Season_filter}_{League_filter}_{Position_filter}_{x_axis}_{y_axis}_Analysis.png",
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

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    Position_filter = st.selectbox("Position:", 
                                df_LF['Position'].unique())
    
    df_PF = df_LF[df_LF['Position']== Position_filter]

    variables = df_PF.select_dtypes(include=['float64', 'int64']).columns.tolist()

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
        df_PF,
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
        st.dataframe(df_PF)

elif page == "Player Report Card":
    st.write("""---""")
    st.title("7 - Player Report Card")
    st.write("Create a player report card for the player you want.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    variables = ['Goal-Scoring', 'Attack','Possession', 'Defense','Physical']

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)
    
    df_TF = df_LF[df_LF['Team']== Team_filter]

    Position_filter = st.selectbox("Position", 
                                df_TF['Position'].unique())
    
    df_PF = df_TF[df_TF['Position']== Position_filter]

    selected_player = st.selectbox("Select Player to Generate Report", 
                                    df_PF['Player'])
    
    player_data = df_PF[df_PF['Player'] == selected_player].iloc[0]
    pos = player_data['Position']
    pos_mean = df_LF[df_LF['Position'] == pos][variables].mean() #Season League filter only

    st.write("""---""")
    fig = plt.figure(figsize=(16, 9), facecolor='#0e1117')
    gs = gridspec.GridSpec(1, 3, width_ratios=[2, 1.5, 2])

    ax_text = fig.add_subplot(gs[1])          
    ax_bar = fig.add_subplot(gs[0])           
    ax_radar = fig.add_subplot(gs[2], polar=True) 

    ax_bar.set_facecolor('#0e1117')
    ax_text.axis('off')
    ax_text.set_title("Player Information", color='white', pad=15, fontsize=14,fontweight='bold')

    profile_lines = [
        f"Name: {player_data['Player']}",
        f"Team: {player_data.get('Team', 'N/A')}",
        f"Age: {player_data.get('Age', 'N/A')}",
        f"League: {player_data.get('League', 'N/A')}",
        f"Season: {player_data.get('Season', 'N/A')}",
        f"Position: {pos}"
    ]

    for i, line in enumerate(profile_lines):
        ax_text.text(0.1, 0.90 - (i * 0.1), line, color='white', 
                    fontsize=16, fontweight='bold', transform=ax_text.transAxes)

    grade_text = f"Grade: {player_data['Grade']}"

    ax_text.text(0.85, 0.15, 
            grade_text, 
            fontsize=35, 
            fontweight='bold',
            color='white', 
            ha='right', 
            va='bottom',
            bbox=dict(
                facecolor='#161a24',   
                edgecolor='white',     
                boxstyle='round,pad=0.5', 
                alpha=0.8              
            ))

    colors = ["#E40000FF", "#0400F5", "#edf100", "#1eff00", "#f88800"]

    ax_bar.set_xlim(0, 100)
    ax_bar.set_xticks([0, 25, 50, 75, 100])
    ax_bar.set_facecolor('#0e1117')

    bars = ax_bar.barh(variables, [player_data[v] for v in variables], color=colors, alpha=0.8)
    ax_bar.bar_label(bars, 
                 padding=8,       
                 color='white',      
                 fontsize=10, 
                 fontweight='bold',
                 fmt='%.1f')
    ax_bar.barh(variables, [player_data[v] for v in variables], color=colors, alpha=0.8)
    ax_bar.axvline(x=0, color='white', linewidth=4, clip_on=False)  
    ax_bar.set_title("Performance Output", color='white', pad=15, fontsize=14,fontweight='bold')
    ax_bar.tick_params(colors='white', labelsize=10)
    ax_bar.invert_yaxis() 
    ax_bar.spines['top'].set_visible(True)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.grid(axis='x', linestyle='--', alpha=0.2)

    angles = np.linspace(0, 2 * np.pi, len(variables), endpoint=False).tolist()
    angles += angles[:1]
    p_values = [player_data[v] for v in variables] + [player_data[variables[0]]]
    m_values = [pos_mean[v] for v in variables] + [pos_mean[variables[0]]]

    ax_radar.set_facecolor('#161a24')
    ax_radar.plot(angles, p_values, color='#89ff3b', linewidth=2, label=selected_player)
    ax_radar.fill(angles, p_values, color='#89ff3b', alpha=0.25)
    ax_radar.plot(angles, m_values, color='#ff3636', linestyle='--', linewidth=2, label='Avg')
    ax_radar.set_ylim(0, 100)
    ax_radar.set_yticks([25, 50, 75, 100]) 
    ax_radar.set_yticklabels(["25", "50", "75", "100"], color="white", size=10,fontweight='bold')
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(variables, color='white', size=11,fontweight='bold')
    ax_radar.set_title("Player vs League Position Mean", color='white', pad=15, fontsize=14, y=1.165,fontweight='bold')

    radar_pos = ax_radar.get_position()
    ax_radar.set_position([radar_pos.x0, radar_pos.y0-0.25, radar_pos.width, radar_pos.height])

    plt.suptitle(f"SCOUTING REPORT: {selected_player.upper()}", 
                color='white', fontsize=28, fontweight='bold', y=1.10)

    legend = ax_radar.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), 
                            ncol=2, facecolor='#0e1117', edgecolor='white')
    plt.setp(legend.get_texts(), color='white')
    plt.figtext(0.97, 0.05, "@TheStatsWay", ha="right", fontsize=12, color='white', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Player Report",
            data=buf.getvalue(),
            file_name=f"{Season_filter}_{League_filter}_{Position_filter}_{selected_player}_Analysis.png",
            mime="image/png")

elif page == "Player Similarity Tool":
    st.write("""---""")
    st.title("8 - Player Similarity Tool")
    st.write("Find the 10 players with the most similar profile based on the 5 performance pillars.")
    st.info(
    """
    Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
    
    df_LF = df_SF[df_SF['League']== League_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)
    
    df_TF = df_LF[df_LF['Team']== Team_filter]

    Position_filter = st.selectbox("Position", 
                                df_TF['Position'].unique())
    
    df_PF = df_TF[df_TF['Position']== Position_filter]

    selected_player = st.selectbox("Select Player to Generate Report", 
                                    df_PF['Player'])
    
    player_data = df_PF[df_PF['Player'] == selected_player].iloc[0] 

    df_supp = df
    df_supp_pos = df_supp[df_supp['Position']== Position_filter]

    sim_features = ['Attack', 'Goal-Scoring', 'Defense', 'Possession', 'Physical']

    def find_similar_players(df_supp_pos, target_player, top_n=10):
        
        df_sim = df_supp_pos.dropna(subset=sim_features).copy()
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_sim[sim_features])
        
        try:
            player_idx = df_sim[df_sim['Player'] == target_player].index[0]
            pos_idx = df_sim.index.get_loc(player_idx)
            target_vector = scaled_data[pos_idx].reshape(1, -1)
        except IndexError:
            return None
        
        similarity_matrix = cosine_similarity(target_vector, scaled_data)
        df_sim['Similarity_Score'] = similarity_matrix.flatten()
        results = df_sim[df_sim['Player'] != target_player]
        results = results.sort_values(by='Similarity_Score', ascending=False)
        
        return results.head(top_n)

    st.write("""---""")
    st.subheader("⤵️ Search Button")

    if st.button("Find Similar Profiles"):
        with st.spinner('Analyzing player vectors...'):
            similar_df = find_similar_players(df_supp_pos, selected_player)
            
            if similar_df is not None:
                st.write(f"### Top 10 Players with the Most Similar Profile to {selected_player}:")
                display_df = similar_df[['Season','League','Team','Player','Age', 'Position', 'Similarity_Score']].copy()
                display_df['Similarity Accuracy'] = (display_df['Similarity_Score'] * 100).map('{:,.1f}%'.format)
                st.dataframe(display_df[['Season','League','Team','Player', 'Age', 'Position', 'Similarity Accuracy']], 
                             hide_index=True,
                             width='stretch')
                best_match = display_df.iloc[0]['Player']
                st.success(f"**Scout's Note:** {best_match} is the best stylistic match in our dataset at {display_df.iloc[0]['Similarity Accuracy']} similarity.")
                
            else:
                st.error("Error: Player data incomplete for the 5 required variables.")