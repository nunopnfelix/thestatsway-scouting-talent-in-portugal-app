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

with st.sidebar:

    st.markdown("""
        <div class='scout-profile'>
            <h4 style='margin-top: 12px; color: #343A40;'>@TheStatsWay</h4>
            <p style='color: #6C757D; font-size: 0.8rem;'>Football Data Analysis</p>
            <div style='font-size: 0.8rem; color: #28a745;'>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'> </div>", unsafe_allow_html=True)
    st.info("💡 **Page Selection:**")

    page = st.sidebar.radio("Pages:", ["Instructions & Abbreviations","Player Stats - Player Overview","Player Stats - Team Overview","Player Comparison Tool",
                                       "Lineup Builder","Scatter Plot","Interactive Plot","Player Report Card","Player Similarity Tool","Team Comparison Tool","Player Progression in a Team",
                                       "Player Search Hub","Team Recruitment Identifier"],
                                    label_visibility="collapsed")


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
st.sidebar.write("𝐯𝟏.𝟎.𝟎𝟗")
st.sidebar.write("Data Last Updated: Mar 12, 2026")

if page == "Instructions & Abbreviations":
    st.write("""---""")
    st.title("0 - Instructions & Abbreviations")
    st.write("")
    st.info("Features Available:", icon="✅")
    st.write("""      
    - **Player Stats - Player Overview:** Browse through the players performance metrics.
    - **Player Stats - Team Overview:** Browse through the players performance metrics for a specific team.
    - **Player Comparison Tool:** Create a performance radar comparison on the outfield players based on our metrics.
    - **Lineup Builder:** Create a teams lineup with the grades for the selected players.
    - **Scatter Plot:** Create a plot with the desired combination of the variables.
    - **Interactive Plot:** Create an interactive plot with the desired combination of the variables.
    - **Player Report Card:** Create a player report card for the player you want.
    - **Player Similarity Tool:** Find the players with the most similar data profile based on our metrics.
    - **Team Comparison Tool:** Create a teams profile per position based on the mean values of the players.
    - **Player Progression in a Team:** Review and analyze a player’s trajectory in the same team.
    - **Player Search Hub:** Find players that match your performance requirements.""")
    st.write("""---""")
    st.info("Position Abreviations:", icon="ℹ️")
    st.write("""            
    - **GK:** Goalkeepers
    - **CB:** Centre-Backs
    - **FB & WB:** Full-Backs & Wing-Backs
    - **MF:** Midfielders
    - **AM & W:** Attacking-Mids & Wingers
    - **CF:** Centre-Fowards""")
    st.write("""---""")
    st.info("Player Output Metrics:", icon="ℹ️")
    st.write("""
    The Player Output Metrics are calculation values adjusted for their position group.
    To calculate our outputs, we have done calculations based on the variables & weights that fall within each area that we considered relevant to that analysis.
             
    **Example:**
        Player (Centre-Back) with a High Goal-Scoring Output is one of the best players in his position group (CB) for that metric.""")
    st.write("""---""")
    st.info("Grading Values:", icon="ℹ️")
    st.write("""
    Our Grade value is based on a formula that evaluates player data (our Player Metrics) adjusted for their position group.
    We normalize the data so that we scale the values to a standardized range.
    Therefore, we opted for the following intervals to this Grading System and respective colors:
             
    - **S -** Elite Output in the Competition (Dark Green)
    - **A -** Good Output in the Competition (Green)
    - **B -** Above Average Output in the Competition (Light Green)
    - **C -** Average Output in the Competition (Yellow)
    - **D -** Below Average Output in the Competition (Orange)
    - **E -** Poor Output in the Competition (Dark Orange)
    - **F -** Very Poor Output in the Competition (Red)""")
    st.write("""---""")

elif page == "Player Stats - Player Overview":
    st.write("""---""")
    st.title("1 - Player Stats - Player Overview")
    st.write("Browse through the players performance metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    
    if min_age < max_age:
        age_range = st.slider(
            "Age Range:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
    )
    else:
        age_range = (min_age, min_age)
        
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

    filtered_df['Player Info'] = filtered_df['Player'] + " (" + filtered_df['Age'].astype(str) + ")"

    if Position_filter == "GK":
        report_cols = ['Team','Player Info', 'Goalkeeping','PosRank', 'Grade']
        report_title = "Goalkeeper Scouting Report"
    else:
        report_cols = ['Team','Player Info', 'Goal-Scoring','Attack','Possession', 'Defense', 'Physical','PosRank', 'Grade']
        report_title = f"{Position_filter.upper()} Scouting Report"

    top_10_report = filtered_df.head(10)[report_cols]

    st.write("---")

    if st.button(f"🖼️ Generate {Position_filter} Table Image", icon=":material/image:"):
    
        if not top_10_report.empty:
            
            fig, ax = plt.subplots(figsize=(11, 7), facecolor='#F8F9FA')
            ax.axis('off')

            table = ax.table(
                cellText=top_10_report.values, 
                colLabels=top_10_report.columns, 
                cellLoc='center', 
                loc='center'
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width(col=list(range(len(top_10_report.columns))))
            table.scale(1, 2.8)

            for (row, col), cell in table.get_celld().items():
                cell.set_edgecolor('#DEE2E6')
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor("#000000")
                else:
                    if row % 2 == 0:
                        cell.set_facecolor('#FFFFFF')
                    else:
                        cell.set_facecolor("#F1F5F2")
                    
                    if top_10_report.columns[col] == 'Grade':
                       grade_val = cell.get_text().get_text()
                       bg_color = get_grade_color(grade_val)
                       cell.set_facecolor(bg_color)
                       cell.set_text_props(weight='bold', color='black')

            plt.title(f"{League_filter} : {report_title}", 
                    color="#000000", fontsize=18, fontweight='bold', pad=30)
            
            plt.figtext(0.5, 0.90, f"Season: {Season_filter} + Age > {age_range[0]} + Age < {age_range[1]}", 
                        fontsize=12, color="#000000", ha='center', style='italic')

            plt.figtext(0.9, 0.05, "@TheStatsWay", 
                        horizontalalignment='right', size=12, color="#000000", style='italic', fontweight='bold')

            st.pyplot(fig)
            st.success("Table generated successfully.")
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

            st.download_button(
                    label="📥 Download Image",
                    data=buf.getvalue(),
                    file_name=f"{Season_filter} - {League_filter} : {report_title}.png",
                    mime="image/png")
        else:
            st.warning("No players found in the current filter to generate a report.")
  
elif page == "Player Stats - Team Overview":
    st.write("""---""")
    st.title("2 - Player Stats - Team Overview")
    st.write("Browse through the players performance metrics for a specific team.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    
    if min_age < max_age:
        age_range = st.slider(
            "Age Range:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
        )
    else:
        age_range = (min_age, min_age)

    df_AF = df_PF[(df_PF['Age'] >= age_range[0]) & (df_PF['Age'] <= age_range[1])]

    df_AF['Grade'] = pd.Categorical(df_AF['Grade'], categories=grade_order, ordered=True)
    filtered_df = df_AF.sort_values(by=['Grade','PosRank'],ascending=True).reset_index(drop=True)

    styled_df = filtered_df.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical','Goalkeeping'])
    
    st.dataframe(styled_df, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)
    
    filtered_df['Player Info'] = filtered_df['Player'] + " (" + filtered_df['Age'].astype(str) + ")"
    report_cols = ['Player Info','Position', 'Goal-Scoring','Attack','Possession', 'Defense', 'Physical','Goalkeeping','PosRank', 'Grade']

    top_23_report = filtered_df.head(23)[report_cols]
    st.write("---")

    if st.button(f"🖼️ Generate {Season_filter} - {League_filter} - {Team_filter} Report", icon=":material/image:"):
        
        if not top_23_report.empty:

            num_rows = len(top_23_report)
            dynamic_height = max((num_rows * 0.6) + 2, 4) 
            
            fig, ax = plt.subplots(figsize=(11, dynamic_height), facecolor='#F8F9FA')
            ax.axis('off')

            table = ax.table(
                cellText=top_23_report.values, 
                colLabels=top_23_report.columns, 
                cellLoc='center', 
                loc='center'
            )

            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width(col=list(range(len(top_23_report.columns))))
            
            for col_index in range(len(top_23_report.columns)):
                current_w = table.get_celld()[(0, col_index)].get_width()
                if current_w < 0.09:
                    for row_index in range(num_rows + 1):
                        table.get_celld()[(row_index, col_index)].set_width(0.09)

            table.scale(1, 2.8)

            for (row, col), cell in table.get_celld().items():
                cell.set_edgecolor('#DEE2E6')
                
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor("#000000")
                else:
                    cell.set_facecolor('#FFFFFF' if row % 2 == 0 else "#F1F5F2")
                    
                    if top_23_report.columns[col] == 'Grade':
                        grade_val = cell.get_text().get_text()
                        bg_color = get_grade_color(grade_val)
                        cell.set_facecolor(bg_color)
                        cell.set_text_props(weight='bold', color='black')

            plt.title(f"{League_filter}: {Team_filter}", 
                    color="#000000", fontsize=22, fontweight='bold', pad=20)

            plt.figtext(0.5, 0.94, f"Season: {Season_filter} + Age > {age_range[0]} + Age < {age_range[1]}", 
                        fontsize=12, color="#000000", ha='center', style='italic')
            
            plt.figtext(0.9, 0.02, "@TheStatsWay", 
                        horizontalalignment='right', size=12, color="#000000", style='italic', fontweight='bold')

            plt.tight_layout()
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            
            st.download_button(
                label="📥 Download Scouting Image",
                data=buf.getvalue(),
                file_name=f"Report_{Season_filter}_{Team_filter}.png",
                mime="image/png"
            )
        else:
            st.warning("No players found in the current filter.")


elif page == "Player Comparison Tool":
    st.write("""---""")
    st.title("3 - Player Comparison Tool")
    st.write("Create a performance radar comparison on the outfield players based on our metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
                          sorted_players3)

    with col4:
        p2 = st.selectbox("Select Player 2", 
                          sorted_players4)

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

    comparison_df['Player Info'] = comparison_df.index + " (" + comparison_df['Age'].astype(str) + ")"
    comparison_cols = ['Player Info', 'Team', 'Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical', 'Grade']
    report_data = comparison_df[comparison_cols]

    st.write("---")

    if st.button(f"🖼️ Generate H2H Report ({p1} vs {p2})", icon=":material/compare_arrows:"):
        
        if not report_data.empty:

            num_vars = len(categories)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

            angles += angles[:1]
            stats1 += stats1[:1]
            stats2 += stats2[:1]

            fig_width = 10
            fig_height = 10

            fig = plt.figure(figsize=(fig_width, fig_height), facecolor='#F8F9FA')
            
            ax_radar = fig.add_subplot(2, 1, 1, polar=True)
            ax_radar.set_theta_offset(np.pi / 2) 
            ax_radar.set_theta_direction(-1) 

            ax_radar.plot(angles, stats1, color='blue', linewidth=2, label=p1)
            ax_radar.fill(angles, stats1, color='blue', alpha=0.25)

            ax_radar.plot(angles, stats2, color='red', linewidth=2, label=p2)
            ax_radar.fill(angles, stats2, color='red', alpha=0.25)

            ax_radar.set_thetagrids(np.degrees(angles[:-1]), categories)
            ax_radar.tick_params(axis='x', pad=15)
            ax_radar.set_rlabel_position(0)
            ax_radar.set_yticks([20, 40, 60, 80, 100])
            ax_radar.set_yticklabels(["20", "40", "60", "80", "100"], color="grey", size=10)
            ax_radar.set_ylim(0, 100)
            ax_radar.grid(True, linestyle='--', color='lightgrey')
            ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
 
            ax_table = fig.add_subplot(2, 1, 2)
            ax_table.axis('off') 

            table = ax_table.table(
                cellText=report_data.values, 
                colLabels=report_data.columns, 
                cellLoc='center', 
                loc='center'
            )

            table.auto_set_font_size(False)
            table.set_fontsize(11)
            table.auto_set_column_width(col=list(range(len(report_data.columns))))
            
            table.scale(1, 3.5)

            for (row, col) in table.get_celld():
                cell = table.get_celld()[(row, col)]
                cell.set_edgecolor('#DEE2E6')
                
                if row == 0:
                    cell.set_text_props(weight='bold', color='white')
                    cell.set_facecolor("#000000")
                else:
                    if row == 1:
                        cell.set_facecolor('#F0F7FF') 
                    else:
                        cell.set_facecolor('#FFF0F0') 

                    if report_data.columns[col] == 'Grade':
                        grade_val = cell.get_text().get_text()
                        bg_color = get_grade_color(grade_val)
                        cell.set_facecolor(bg_color)
                        cell.set_text_props(weight='bold', color='black')

            fig.suptitle(f"Player Comparison Report", 
                    color="#000000", fontsize=22, fontweight='bold', y=0.98)
            
            plt.figtext(0.5, 0.93, f"{p1} & {p2} (Season: {Season_filter} + League: {League_filter})", 
                        fontsize=12, color="#000000", ha='center', style='italic')
            
            plt.figtext(0.9, 0.05, "@TheStatsWay", 
                        horizontalalignment='right', size=12, color="#000000", style='italic', fontweight='bold')

            plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
            st.pyplot(fig)

            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            st.download_button(
                label="📥 Download Comparison Image",
                data=buf.getvalue(),
                file_name=f"H2H_Comparison_{p1}_vs_{p2}.png",
                mime="image/png"
            )

elif page == "Lineup Builder":
    st.write("""---""")
    st.title("4 - Lineup Builder")
    st.write("Create a teams lineup with the grades for the selected players.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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


        
elif page == "Scatter Plot":
    st.write("""---""")
    st.title("5 - Simple Scatter Plot")
    st.write("Create a plot with the desired combination of the variables.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    
    if min_age < max_age:
        age_range = st.slider(
            "Age Range:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
        )
    else:
        age_range = (min_age, min_age)

    df_AF = df_PF[(df_PF['Age'] >= age_range[0]) & (df_PF['Age'] <= age_range[1])]

    teams = df_AF['Team'].unique().tolist()
    sorted_teams = sorted(teams)
    TeamFilter = st.multiselect("Team Filter:",
                                options=sorted_teams,
                                default=sorted_teams)

    if TeamFilter:
        df_TF = df_AF[df_AF["Team"].isin(TeamFilter)]

    st.subheader("📊 Plot Settings")
    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")
    allowed_metrics = ["Goal-Scoring","Attack", "Possession", "Defense","Physical","Age"]
    variables = [m for m in allowed_metrics if m in df_TF.columns]
    
    x_axis = st.selectbox("X-Axis (Horizontal)", 
                        variables, 
                        index=0)

    y_axis = st.selectbox("Y-Axis (Vertical)", 
                                  variables, 
                                  index=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#333333")
    ax.set_facecolor("#f7f7f7")

    for i, row in df_TF.iterrows():
        ax.scatter(row[x_axis], row[y_axis], 
                color= get_grade_color(row['Grade']), 
                s=200, 
                edgecolors='black', 
                alpha=0.8)
        
        ax.text(row[x_axis], row[y_axis]-2.5, 
                row['Player'], 
                color='black', 
                ha='center', fontsize=7)

    ax.set_title(f"{Position_filter}s Report: {x_axis} & {y_axis}", color='white', fontsize=18, fontweight='bold', pad=30)
    ax.set_xlabel(x_axis, color='white', fontsize=12,fontweight='bold')
    ax.set_ylabel(y_axis, color='white', fontsize=12,fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)

    plt.figtext(0.5, 0.915, f"Season: {Season_filter} + League: {League_filter} + Age > {age_range[0]} + Age < {age_range[1]}", 
                fontsize=11, color="#FFFFFF", ha='center', style='italic')
    plt.figtext(0.9, 0.02, "@TheStatsWay", ha="right", 
                fontsize=10, color='White', fontweight='bold')
    plt.figtext(0.35, 0.01, "https://thestatsway-scouting-talent-in-portugal-app.streamlit.app/",ha="right", fontsize=6, color='White', fontweight='bold')
    
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Lineup Image",
            data=buf.getvalue(),
            file_name=f"{Season_filter}_{League_filter}_{Position_filter}_{x_axis}_{y_axis}_Analysis.png",
            mime="image/png")
    
elif page == "Interactive Plot":
    st.write("""---""")
    st.title("6 - Interactive Plot")
    st.write("Create an interactive plot with the desired combination of the variables.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    pos_mean = df_LF[df_LF['Position'] == pos][variables].mean()

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

    plt.suptitle(f"Scouting Report: {selected_player.upper()}", 
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
    st.write("Find the players with the most similar data profile based on our metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
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
    df_supp_pos = df_supp_pos.dropna(subset=['Age'])

    sim_features = ['Attack', 'Goal-Scoring', 'Defense', 'Possession', 'Physical']

    st.write("""---""")
    st.subheader("🛠️ Similar Profiles - Age Filter")

    min_age = int(df_supp_pos['Age'].min())
    max_age = int(df_supp_pos['Age'].max())

    age_range = st.slider("Age Range for the Similar Profiles to display:",
                        min_value=min_age,
                        max_value=max_age,
                        value=(min_age, max_age))

    st.subheader("⤵️ Search Button")

    def find_similar_players(df_supp_pos, target_player, target_season, top_n=10):
        df_sim = df_supp_pos.dropna(subset=sim_features).copy()
        
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df_sim[sim_features])
        
        try:
            target_row = df_sim[(df_sim['Player'] == target_player) & 
                                (df_sim['Season'] == target_season)]
            
            if target_row.empty:
                return None
                
            player_idx = target_row.index[0]
            pos_idx = df_sim.index.get_loc(player_idx)
            target_vector = scaled_data[pos_idx].reshape(1, -1)
            
        except (IndexError, KeyError):
            return None
        
        similarity_matrix = cosine_similarity(target_vector, scaled_data)
        df_sim['Similarity_Score'] = similarity_matrix.flatten()
        results = df_sim.drop(index=player_idx)
        
        results = results[(results['Age'] >= age_range[0]) & (results['Age'] <= age_range[1])]
        results = results[(results['Similarity_Score'] > 0)]
        results = results.sort_values(by='Similarity_Score', ascending=False)
        
        return results.head(top_n)

    if st.button("🔍 Find Similar Profiles"):
        with st.spinner(f'Analyzing {selected_player}\'s DNA in the {Season_filter} season...'):
            
            similar_df = find_similar_players(df_supp_pos, selected_player, Season_filter)
            
            if similar_df is not None:
                st.write(f"### Top 10 Similar Profiles to {selected_player} ({Season_filter}):")
                
                display_cols = ['Season', 'League', 'Team', 'Player', 'Age', 'Position', 'Similarity_Score']
                display_df = similar_df[display_cols].copy()
                display_df['Similarity Accuracy'] = (display_df['Similarity_Score'] * 100).map('{:,.1f}%'.format)
                
                st.dataframe(
                    display_df[['Season', 'League', 'Team', 'Player', 'Age', 'Position', 'Similarity Accuracy']], 
                    hide_index=True,
                    width='stretch'
                )
                
                top_row = display_df.iloc[0]
                best_match_name = top_row['Player']
                best_match_season = top_row['Season']
                accuracy = top_row['Similarity Accuracy']
                
                note_text = f" **{best_match_name} ({best_match_season})** is the best stylistic match in this condition at **{accuracy}** similarity."
                
                st.success(note_text)
                
                num_rows = len(display_df)
                dynamic_height = max((num_rows * 0.6) + 2.5, 4)
                
                fig, ax = plt.subplots(figsize=(10, dynamic_height), facecolor='#F8F9FA')
                ax.axis('off')

                display_df['Player Info'] = display_df['Player'] + " (" + display_df['Age'].astype(str) + ")"
                plot_df = display_df[['Season', 'League', 'Team', 'Player Info', 'Position', 'Similarity Accuracy']]

                table = ax.table(
                    cellText=plot_df.values, 
                    colLabels=plot_df.columns, 
                    cellLoc='center', 
                    loc='center'
                )

                table.auto_set_font_size(False)
                table.set_fontsize(10)
                table.auto_set_column_width(col=list(range(len(plot_df.columns))))
                table.scale(1.4, 2.8) 
                
                for (row, col), cell in table.get_celld().items():
                    cell.set_edgecolor('#DEE2E6')

                    if row == 0:
                        cell.set_text_props(weight='bold', color='white')
                        cell.set_facecolor("#000000")
                    else:
                        cell.set_facecolor('#FFFFFF' if row % 2 == 0 else "#F1F5F2")
                        
                        if plot_df.columns[col] == 'Similarity Accuracy':
                            cell.set_text_props(weight='bold', color='#1A73E8') 

                plt.title(f"Most Similar Data Profile to {selected_player} ({Season_filter})", 
                      color="#000000", fontsize=16, fontweight='bold', pad=30, y=0.92)
            
                plt.figtext(0.5, 0.915, f"Age > {age_range[0]} + Age < {age_range[1]}", 
                            fontsize=11, color="#000000", ha='center', style='italic')

                plt.figtext(0.9, 0.05, "@TheStatsWay", 
                            horizontalalignment='right', size=12, color="#000000", style='italic', fontweight='bold')

                plt.tight_layout()
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                st.download_button(
                    label="📥 Download Similarity Report",
                    data=buf.getvalue(),
                    file_name=f"Similarity_{selected_player}_{Season_filter}.png",
                    mime="image/png"
            )
                
            else:
                st.error(f"**Data Gap:** We don't have enough performance data for {selected_player} in the {Season_filter} season to generate a vector.")


elif page == "Team Comparison Tool":
    st.write("""---""")
    st.title("9 - Team Comparison Tool")
    st.write("Create a teams profile per position based on the mean values of the players.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    st.subheader("🛠️ Team Settings")

    sim_features = ['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical']

    s_filt = st.selectbox("Select Season:", df['Season'].unique(), key='heatmap_s')
    l_filt = st.selectbox("Select League:", df[df['Season']==s_filt]['League'].unique(), key='heatmap_l')

    df_filtered = df[(df['Season'] == s_filt) & (df['League'] == l_filt)]

    team_pos_mean = df_filtered.groupby(['Team', 'Position'])[sim_features].mean().reset_index()
    pos_to_view = st.selectbox("Compare Teams by Position Group:", team_pos_mean['Position'].unique())

    heatmap_data = team_pos_mean[team_pos_mean['Position'] == pos_to_view].set_index('Team')[sim_features]

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        show_median = st.toggle("📊 Show League Median", value=False)
    with t_col2:
        show_mean = st.toggle("📈 Show League Mean", value=False)

    if show_mean and not heatmap_data.empty:
        mean_val = heatmap_data.mean()
        mean_df = pd.DataFrame([mean_val], columns=sim_features, index=['League Mean'])
        heatmap_data = pd.concat([heatmap_data, mean_df])

    if show_median and not heatmap_data.empty:
        median_val = heatmap_data.median()
        median_df = pd.DataFrame([median_val], columns=sim_features, index=['League Median'])
        heatmap_data = pd.concat([heatmap_data, median_df])

    if not heatmap_data.empty:
        st.write("""---""")
        fig, ax = plt.subplots(figsize=(12, len(heatmap_data) * 0.5 + 2), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')

        sns.heatmap(heatmap_data, 
                    annot=True, 
                    fmt=".1f", 
                    cmap="RdYlGn", 
                    ax=ax, 
                    cbar=False,
                    annot_kws={"weight": "bold", "size": 11})

        plt.title(f"{l_filt} - {pos_to_view} Profile ({s_filt})", 
                color='white', fontsize=18, pad=60, fontweight='bold')
        
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        ax.tick_params(axis='x', colors='white', labelsize=12, pad=15)
        ax.tick_params(axis='y', colors='white', labelsize=12)
        
        ax.set_xlabel("") 
        ax.set_ylabel("")

        for i, name in enumerate(heatmap_data.index):
            if name in ['League Mean', '📊 Show League Median']:
                ax.add_patch(plt.Rectangle((0, i), len(sim_features), 1, 
                                        fill=False, edgecolor='white', lw=3, ls='--'))

        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.figtext(0.97, -0.01, "@TheStatsWay", ha="right", fontsize=12, color='white', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        st.download_button(
                label="📥 Download Team Comparison Report",
                data=buf.getvalue(),
                file_name=f"Team_Comparison_{s_filt}_{l_filt}_{pos_to_view}.png",
                mime="image/png")

elif page == "Player Progression in a Team":
    st.write("""---""")
    st.title("10 - Player Progression in a Team")
    st.write("Review and analyze a player’s trajectory in the same team.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Player Settings")

    df1 = df.sort_values(['Player','Team','Season'])
    
    df1['age_jump_backw'] = (df1.groupby('Player')['Age'].shift(1))-(df1['Age'])
    df1['age_jump_foward'] = (df1.groupby('Player')['Age'].shift(-1))-(df1['Age'])
    df1['age_jump_backw_good'] = (df1['age_jump_backw'].isin([1,0,-1]))
    df1['age_jump_foward_good'] = (df1['age_jump_foward'].isin([-1,0, 1]))
    df1['filter'] = (df1['age_jump_backw_good'] == True) | (df1['age_jump_foward_good'] == True)

    df_clean = df1[df1['filter'] != False].copy()
    df_clean = df_clean.drop(columns=['age_jump_backw','age_jump_foward','age_jump_backw_good','age_jump_foward_good','filter']) 
    df_clean = df_clean.reset_index(drop=True)
    
    league_order = ['Liga Portugal', 'Liga 2', 'Liga 3', 'Campeonato de Portugal', 'Liga Revelação U23']

    df_clean['League'] = pd.Categorical(df_clean['League'], categories=league_order, ordered=True)

    league_filter = st.selectbox("Filter by a League that the Team played in:",
                                df_clean['League'].unique().sort_values())

    df_LF = df_clean[df_clean['League'] == league_filter]

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)

    df_TF = df_clean[df_clean['Team']== Team_filter]
    
    df_TF = df_TF.groupby(['Player', 'Team']).filter(lambda x: len(x) > 1) #filter to have only player names with 2 rows for a Team
    players = df_TF['Player'].unique().tolist()
    sorted_players = sorted(players)
    
    Player_filter = st.selectbox("Player:", 
                                options=sorted_players)
    
    df_PF = df_TF[df_TF['Player']== Player_filter]

    filtered_df = df_PF.sort_values(by='Season', ascending=True)

    styled_df = df_PF.style.map(style_grade_column, subset=['Grade'])\
                   .format(precision=2, subset=['Goal-Scoring', 'Attack','Possession', 'Defense','Physical','Goalkeeping'])

    st.dataframe(styled_df,
                 column_order=("Season","League","Player","Team","Age","Position","Goal-Scoring","Attack","Possession","Defense","Physical","Goalkeeping","PosRank","Grade"),
                 width="stretch",
                 hide_index=True,
                 height = 143)
    
    st.write("""---""")

    plot_df = df_PF[df_PF['Player'] == Player_filter].sort_values('Season')
    target_seasons = ['2023/24', '2024/25', '2025/26']
    plot_df = plot_df[plot_df['Season'].isin(target_seasons)]
    plot_df = plot_df.drop_duplicates(subset=['Season'], keep='last').sort_values('Season')

    if len(plot_df) < 2:
        st.warning(f"⚠️ Comparison impossible. Missing data for it.")
        st.stop()

    season_labels = plot_df['Season'].tolist()
    num_seasons = len(plot_df)
    current_position = plot_df.iloc[-1]['Position'].lower()

    if 'GK' in current_position or 'gk' in current_position:
        metrics = ['Goalkeeping']
        colors = ['#1A73E8'] 
    else:
        metrics = ['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical']
        colors = ['#E63946', '#1A73E8', '#2A9D8F', '#F4A261', '#8D99AE']

    season_colors = ["#5da5da", "#faa43a", "#60bd68"]

    fig = plt.figure(figsize=(20, 14), facecolor='#F8F9FA')
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.2, 2.8], height_ratios=[1, 1], hspace=0.3, wspace=0.2)

    ax_info = fig.add_subplot(gs[:, 0])
    ax_info.axis('off')
    ax_info.text(0.05, 1.05, Player_filter.upper(), fontsize=28, fontweight='bold')
    ax_info.text(0.05, 1.025, f"{plot_df.iloc[-1]['Team']} | {plot_df.iloc[-1]['Age']}y", fontsize=14, color='#6C757D', fontweight='bold')
    y_offset = 0.95

    for _, row in plot_df.iloc[::-1].iterrows():
        ax_info.text(0.05, y_offset, f"▼ Season {row['Season']} ▼", fontsize=13, color='#6C757D', fontweight='bold')
        ax_info.text(0.05, y_offset-0.03, f"League: {row['League']}", fontsize=12)
        ax_info.text(0.05, y_offset-0.0525, f"Position: {row['Position']}", fontsize=12)
        ax_info.text(0.05, y_offset-0.075, f"Grade: {row['Grade']}", fontsize=12, fontweight='bold')
        y_offset -= 0.13

    ax_info.text(0.05, 0.455, "DEVELOPMENT SUMMARY", fontsize=14, fontweight='bold')

    for i, m in enumerate(metrics):
        diff = plot_df.iloc[-1][m] - plot_df.iloc[0][m]
        color = '#2A9D8F' if diff >= 0 else '#E63946'
        symbol = "▲" if diff >= 0 else "▼"
        y_pos = (0.35) - (i * 0.07)
        ax_info.text(0.05, y_pos, m, fontsize=13, color='#6C757D', fontweight='bold')
        ax_info.text(0.55, y_pos, f"{symbol} {abs(diff):.1f}", fontsize=12, fontweight='bold', color=color)

    ax_bar = fig.add_subplot(gs[0, 1])
    y = np.arange(len(metrics))
    width = 0.25 

    for i in range(num_seasons):
        offset = (width * (num_seasons - 1) / 2) - (i * width)
        ax_bar.barh(y + offset, plot_df.iloc[i][metrics], width, 
                    label=season_labels[i], color=season_colors[i], alpha=0.8 if i < num_seasons-1 else 1.0)

    ax_bar.set_yticks(y)
    ax_bar.invert_yaxis()
    ax_bar.set_yticklabels(metrics, fontweight='bold')
    ax_bar.set_xlim(0, 115)
    ax_bar.set_title("STATISTICAL COMPARISON", loc='left', fontsize=14, fontweight='bold', pad=15)
    ax_bar.legend(loc='lower right', frameon=False)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    handles, labels = ax_bar.get_legend_handles_labels()
    ax_bar.legend(handles[::-1], labels[::-1], loc='lower right', frameon=False, fontsize=10)

    ax_line = fig.add_subplot(gs[1, 1])
    x_indices = np.arange(num_seasons)

    for i, metric in enumerate(metrics):
        y_vals = plot_df[metric].tolist()
        
        ax_line.plot(x_indices, y_vals, color=colors[i], linewidth=4, alpha=0.8, zorder=1)
        ax_line.scatter(x_indices, y_vals, s=120, color=colors[i], edgecolors='white', linewidth=2, zorder=2)
        ax_line.text(x_indices[-1] + 0.05, y_vals[-1], metric, color=colors[i], 
                    fontweight='bold', va='center', fontsize=10)

    ax_line.set_xticks(x_indices)
    ax_line.set_xticklabels(season_labels, fontweight='bold', fontsize=12)
    ax_line.set_xlim(-0.3, num_seasons - 0.5)
    ax_line.set_ylim(0, 105)
    ax_line.set_title("PERFORMANCE TRENDLINE", loc='left', fontsize=14, fontweight='bold', pad=15)
    ax_line.spines['top'].set_visible(False)
    ax_line.spines['right'].set_visible(False)
    ax_line.grid(True, axis='y', linestyle=':', alpha=0.3)
    plt.figtext(0.9, 0.02, "@TheStatsWay", ha="right", fontsize=12, color='black', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Player Report",
            data=buf.getvalue(),
            file_name=f"Player_Progression_{Player_filter}_Analysis.png",
            mime="image/png")
    
elif page == "Player Search Hub":
    st.write("""---""")
    st.title("11 - Player Search Hub ")
    st.write("Find players that match your performance requirements.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    
    df = df[df.Position != "GK"]

    st.subheader("🛠️ Search Settings")

    selected_season = st.multiselect("Targeted Season(s):",
                                options=sorted(df['Season'].unique()),
                                default='2025/26')

    selected_leagues = st.multiselect("Targeted Leagues:",
                                options=sorted(df['League'].unique()),
                                default="Liga 3")

    selected_position = st.selectbox("Targeted Position:", 
                                  df['Position'].unique())
    
    col1, col2 = st.columns(2)
    min_age = int(df['Age'].min())
    max_age = int(df['Age'].max())

    with col1:       
        age_min = st.number_input("Minimum Player Age:", 
                                min_value=min_age,
                                max_value=max_age,
                                value=19)
        age_min = int(age_min)
                      
    with col2:
        age_max = st.number_input("Maximum Player Age:", 
                                min_value=min_age,
                                max_value=max_age,
                                value=37)
        age_max = int(age_max)
           
    st.divider()
    st.subheader("Required Thresholds")

    goal_min = st.slider("Minimum Goal-Scoring", 0, 100, 0)
    attack_min = st.slider("Minimum Attack", 0, 100, 0)
    poss_min = st.slider("Minimum Possession", 0, 100, 0)
    def_min = st.slider("Minimum Defense", 0, 100, 0)
    phys_min = st.slider("Minimum Physical", 0, 100, 0)

    filtered_df = df[
        (df['Season'].isin(selected_season)) &
        (df['League'].isin(selected_leagues)) &
        (df['Position'] == selected_position) &
        (df['Age'] >= age_min) &
        (df['Age'] <= age_max) &
        (df['Goal-Scoring'] >= goal_min) &
        (df['Attack'] >= attack_min) &
        (df['Possession'] >= poss_min) &
        (df['Defense'] >= def_min) &
        (df['Physical'] >= phys_min)
    ]
  
    st.divider()
    st.title("🔍 Player Search Hub")
    st.markdown(f"Finding players that match your requirements.")

    col1, col2, col3, col4, col5, col6, col7, col8  = st.columns(8)
    col1.metric("Results Found", len(filtered_df))
    col2.metric("Avg. Age", f"{round(filtered_df['Age'].mean(), 1) if not filtered_df.empty else '0'}")
    col3.metric("Most Common Grade", f"{filtered_df['Grade'].mode()[0] if not filtered_df.empty else 'N/A'}")
    col4.metric("Avg. Goal-Scoring", f"{round(filtered_df['Goal-Scoring'].mean(), 1) if not filtered_df.empty else '0'}")
    col5.metric("Avg. Attack", f"{round(filtered_df['Attack'].mean(), 1) if not filtered_df.empty else '0'}")
    col6.metric("Avg. Possession", f"{round(filtered_df['Possession'].mean(), 1) if not filtered_df.empty else '0'}")
    col7.metric("Avg. Defense", f"{round(filtered_df['Defense'].mean(), 1) if not filtered_df.empty else '0'}")
    col8.metric("Avg. Physical", f"{round(filtered_df['Physical'].mean(), 1) if not filtered_df.empty else '0'}")

    filtered_df['Skill Score'] = filtered_df[['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical']].mean(axis=1)

    if not filtered_df.empty:
        display_cols = ['Season','League','Player', 'Team', 'Age', 'Position', 'Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical','Grade', 'Skill Score']
        
        st.dataframe(
            filtered_df[display_cols].sort_values('Skill Score', ascending=False),
            width='stretch',
            height = 770,
            hide_index=True,
            column_config={
                "Skill Score": st.column_config.ProgressColumn(
                    "Metric Average",
                    help="Average of the 5 core scouting metrics",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
    else:
        st.info("No players found matching these exact criteria. Try lowering the thresholds!")

elif page == "Team Recruitment Identifier":
    st.write("""---""")
    st.title("12 - Team Recruitment Identifier Hub ")
    st.write("Find players that fit the teams needs.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Team Search Settings")

    season_filter = st.selectbox("Filter by the Season that the Team played in:",
                                df['Season'].unique())

    df = df[df['Season'] == season_filter]
    df_clean = df[df['Season'] == season_filter] 

    league_filter = st.selectbox("Filter by a League that the Team played in:",
                                df['League'].unique())

    df_LF = df[df['League'] == league_filter]

    metrics = ['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical','Goalkeeping']

    teams = df_LF['Team'].unique().tolist()
    sorted_teams = sorted(teams)

    Team_filter = st.selectbox("Team:", 
                                options=sorted_teams)

    team_data = df_LF[df_LF['Team'] == Team_filter]

    team_avg = team_data.groupby('Position')[metrics].mean().round(1)

    position_context = team_data.groupby('Position').agg(AvgAge=('Age', 'mean'),
                                                         NumberPlayers=('Player', 'count'))
    
    position_context['AvgAge'] = position_context['AvgAge'].round(1)
    position_context['NumberPlayers'] = position_context['NumberPlayers'].astype(int)
    team_avg = pd.concat([position_context, team_avg], axis=1)

    pos_order = ['GK', 'CB', 'FB & WB', 'MF', 'AM & W', 'CF']
    existing_order = [p for p in pos_order if p in team_avg.index]

    team_avg = team_avg.reindex(existing_order)
    st.subheader(f"📊 {Team_filter} - Positional DNA")
    
    def highlight_low_scores(val):
        if val == 0:
            return 'background-color: grey; color: white; font-weight: bold;'
        if val < 50:
            return 'background-color: #ff4b4b; color: white; font-weight: bold;'
        return ''
    
    styled_team_avg = (
            team_avg.style
            .map(highlight_low_scores, subset=metrics)
            .format(lambda x: "NA" if x == 0 else f"{x:.2f}")
        )
    
    st.dataframe(styled_team_avg, 
                 width='stretch')

    threshold = 50.0
    weaknesses = []

    for pos in team_avg.index:
        for metric in metrics:
            score = team_avg.loc[pos, metric]
            if score < threshold:
                weaknesses.append({'Position': pos, 'Metric': metric, 'Score': score})

    weak_df = pd.DataFrame(weaknesses)

    if not weak_df.empty:
        weak_df = weak_df[weak_df['Score'] > 0]

    if not weak_df.empty:
       
        st.warning(f"⚠️ Found {len(weak_df)} actionable areas performing below the {threshold} threshold.")
        position_needs = weak_df.groupby('Position')['Metric'].apply(list).to_dict()
        
    else:
        st.success("✅ No actionable weaknesses found (all missing data marked as NA).")

    st.divider()
    st.header("🎯 Required Positional Profiles")
    st.info("The following players are ranked by their ability to solve all identified weaknesses for each position simultaneously.")

    Leagues = df_clean['League'].unique().tolist()
    LeaguesReplacementFilter = st.multiselect("League Filter:",
                                options=Leagues,
                                default=league_filter)

    if LeaguesReplacementFilter:
        df_clean = df_clean[df_clean["League"].isin(LeaguesReplacementFilter)]

    min_age = int(df_clean['Age'].min())
    max_age = int(df_clean['Age'].max())
    
    if min_age < max_age:
        age_range = st.slider(
            "Age Range:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
    )
    else:
        age_range = (min_age, min_age)

    df_clean = df_clean[(df_clean['Age'] >= age_range[0]) & (df_clean['Age'] <= age_range[1])]

    st.divider()
    st.header("💎 Analysing: Player Needs")
    st.info("These potential targets are aimed to solve the identified weaknesses for each position.")

    if not weak_df.empty:

        real_weaknesses = weak_df[weak_df['Score'] > 0]

        if not real_weaknesses.empty:

            position_needs = real_weaknesses.groupby('Position')['Metric'].apply(list).to_dict()
            pos_order = ['GK', 'CB', 'FB & WB', 'MF', 'AM & W', 'CF']
            
            for pos in pos_order:
                if pos in position_needs:
                    needs = position_needs[pos]
                    
                    with st.expander(f"**PLAYER NEEDS - SIGNINGS PROFILE: {pos}** (Needs: {', '.join(needs)})"):

                        query_condition = (df_clean['Position'] == pos) & (df_clean['Team'] != Team_filter)
                        
                        for m in needs:
                            
                            team_score = real_weaknesses[(real_weaknesses['Position'] == pos) & 
                                                         (real_weaknesses['Metric'] == m)]['Score'].values[0]
                            
                            query_condition &= (df_clean[m] > 49.999) #higher than teams value and 50 threshold

                        potential_signings = df_clean[query_condition].copy()

                        if not potential_signings.empty:
                            potential_signings['Solution Score'] = potential_signings[needs].mean(axis=1)

                            recommendations = potential_signings.sort_values(by='Solution Score', ascending=False).head(10)

                            st.write(f"Showing the best players to improve **{', '.join(needs)}** for the {pos} position:")
                            
                            display_cols = ['Player', 'Team', 'Age'] + needs + ['Grade', 'Solution Score']
                            
                            styled_recommendations = (recommendations[display_cols].style
                                .format(lambda x: "NA" if x == 0 else (f"{x:.2f}" if isinstance(x, (int, float)) else x)))

                            st.dataframe(
                                styled_recommendations,
                                hide_index=True,
                                width='stretch',
                                column_config={
                                    "Solution Score": st.column_config.ProgressColumn(
                                        "Fit Score", 
                                        min_value=0, max_value=100, format="%.2f"),
                                }
                            )
                        else:
                            st.info(f"No players found in the database who perform better than the current {pos} average in {', '.join(needs)}.")
        else:
            st.success("✅ No actionable weaknesses found (all missing data marked as NA).")
    else:
        st.success("✅ Your squad is balanced! No positions are currently below the threshold.")


    st.divider()
    st.header("💎 Analysing: Star Upgrades")
    st.info("These potential targets outperform the current squad average in every single performance category for their position.")

    outfield_metrics = ['Goal-Scoring', 'Attack', 'Possession', 'Defense', 'Physical']
    gk_metrics = ['Goalkeeping']

    for pos in pos_order:

        if pos in team_avg.index:
            
            compare_metrics = gk_metrics if pos == 'GK' else outfield_metrics
            team_baseline = team_avg.loc[pos, compare_metrics]

            potential_upgrades = df_clean[
                (df_clean['Position'] == pos) & 
                (df_clean['Team'] != Team_filter)
            ].copy()

            if not potential_upgrades.empty:

                upgrade_mask = (potential_upgrades[compare_metrics] > team_baseline).all(axis=1)
                elite_targets = potential_upgrades[upgrade_mask].copy()

                if not elite_targets.empty:
                    with st.expander(f"**STAR UPGRADES: {pos}** ({len(elite_targets)} targets found)"):
                        
                        elite_targets['Value Added'] = (elite_targets[compare_metrics].mean(axis=1) - team_baseline.mean())
                        elite_targets = elite_targets.sort_values(by='Value Added', ascending=False).head(10)

                        st.write(f"These players are statistically superior to your **{pos}** baseline in all {len(compare_metrics)} categories:")

                        display_cols = ['Player', 'Team', 'Age'] + compare_metrics + ['Value Added']
                        
                        st.dataframe(
                            elite_targets[display_cols].style.format(precision=2),
                            hide_index=True,
                            width='stretch',
                            column_config={
                                "Value Added": st.column_config.NumberColumn(
                                    "Avg. Lift",
                                    help="Average performance increase across all metrics compared to your squad",
                                    format="+%.2f"
                                ),
                                **{m: st.column_config.NumberColumn(m, format="%.1f") for m in (outfield_metrics + gk_metrics)}
                            }
                        )

    st.divider()
    st.header("💎 Analysing: Positional Upgrades")
    st.info("These potential targets have a higher average performance than the current squads baseline for their position.")
   
    team_mean_benchmarks = team_data.groupby('Position')[outfield_metrics + gk_metrics].mean()

    for pos in pos_order:
        if pos in team_mean_benchmarks.index:
            
            compare_metrics = gk_metrics if pos == 'GK' else outfield_metrics

            team_baseline_avg = team_mean_benchmarks.loc[pos, compare_metrics].mean()

            potential_upgrades = df_clean[
                (df_clean['Position'] == pos) & 
                (df_clean['Team'] != Team_filter)
            ].copy()

            if not potential_upgrades.empty:

                potential_upgrades['Avg Value Added'] = (potential_upgrades[compare_metrics].mean(axis=1) - team_baseline_avg)
                
                upgrade_targets = potential_upgrades[potential_upgrades['Avg Value Added'] > 0].copy()
                
                if not upgrade_targets.empty:

                    upgrade_targets = upgrade_targets.sort_values(by='Avg Value Added', ascending=False).head(10)

                    with st.expander(f"**POSITIONAL UPGRADES: {pos}** ({len(potential_upgrades)} targets found)"):
                        
                        st.write(f"Showing players who are, on average, better than your current {pos} group:")
                        
                        display_cols = ['Player', 'Team', 'Age'] + compare_metrics + ['Avg Value Added']
                        
                        st.dataframe(
                            upgrade_targets[display_cols].style.format(precision=2),
                            hide_index=True,
                            width='stretch',
                            column_config={
                                "Avg Value Added": st.column_config.NumberColumn(
                                    "Avg. Lift",
                                    help="The average points this player adds per metric compared to the team average.",
                                    format="+%.2f" 
                                ),
                                **{m: st.column_config.NumberColumn(m, format="%.1f") for m in (outfield_metrics + gk_metrics)}
                            }
                        )
                else:
                    st.info(f"No targets found who are, on average, better than the current {pos} squad.")