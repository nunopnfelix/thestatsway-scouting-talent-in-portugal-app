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
import matplotlib.patheffects as path_effects
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from lightgbm import LGBMRegressor

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

    page = st.sidebar.radio("Pages:", ["Instructions & Abbreviations","Player Stats - Player Overview","Player Stats - Team Overview","Two Player Comparison Tool","Three Player Comparison Tool",
                                       "Lineup Builder","Scatter Plot","Team Scatter Plot","Interactive Plot","Player Report Card","Player Similarity Tool","Team Comparison Tool",
                                       "Player Progression in a Team","Player Search Hub","Team Recruitment Identifier","Squad Builder Report","Profile Clusters","Re-Sale Value Calculator",
                                       "Ternary Graph","Team Global Analysis"],
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
st.sidebar.write("𝐯𝟏.𝟎.𝟏𝟓")
st.sidebar.write("Data Last Updated: Jun 10, 2026")

if page == "Instructions & Abbreviations":
    st.write("""---""")
    st.title("0 - Instructions & Abbreviations")
    st.write("")
    st.info("Features Available:", icon="✅")
    st.write("""      
    - **Player Stats - Player Overview:** Browse through the players performance metrics.
    - **Player Stats - Team Overview:** Browse through the players performance metrics for a specific team.
    - **Two Player Comparison Tool:** Create a performance radar comparison on the outfield players based on our metrics.
    - **Three Player Comparison Tool:** Create a performance radar comparison on the outfield players based on our metrics.
    - **Lineup Builder:** Create a teams lineup with the grades for the selected players.
    - **Scatter Plot:** Create a plot with the desired combination of the variables.
    - **Interactive Plot:** Create an interactive plot with the desired combination of the variables.
    - **Player Report Card:** Create a player report card for the player you want.
    - **Player Similarity Tool:** Find the players with the most similar data profile based on our metrics.
    - **Team Comparison Tool:** Create a teams profile per position based on the mean values of the players.
    - **Player Progression in a Team:** Review and analyze a player’s trajectory in the same team.
    - **Player Search Hub:** Find players that match your performance requirements.
    - **Team Recruitment Identifier:** Find players that fit the teams needs.
    - **Squad Builder Report:** Build your Team's squad for next season.
    - **Profile Clusters:** Group the players into clusters to help for profile analysis.
    - **Re-Sale Value Calculator:** Calculate the player re-sale value based on our available metrics.
    - **Ternary Graph:** Analyze compositional data in the three-dimensional tool.
    - **Team Global Analysis:** This section aggregates individual player metrics to map out team-wide tactical identities and styles.""")
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

    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","Goalkeeping","PosRank","Grade"]]
    
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
                   .format(precision=2, subset=['Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession','Defense','Physical','Goalkeeping'])

    st.dataframe(styled_df, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)

    filtered_df['Player Info'] = filtered_df['Player'] + " (" + filtered_df['Age'].astype(str) + ")"

    if Position_filter == "GK":
        report_cols = ['Team','Player Info', 'Goalkeeping','PosRank', 'Grade']
        report_title = "Goalkeeper Scouting Report"
    else:
        report_cols = ['Team','Player Info', 'Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession', 'Defense', 'Physical', 'Grade']
        report_title = f"{Position_filter.upper()} Scouting Report"

    top_10_report = filtered_df.head(10)[report_cols]

    st.write("---")

    if st.button(f"🖼️ Generate {Position_filter} Table Image", icon=":material/image:"):
    
        if not top_10_report.empty:
            
            fig, ax = plt.subplots(figsize=(11.5, 7), facecolor='#F8F9FA')
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

    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","Goalkeeping","PosRank","Grade"]]

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
                   .format(precision=2, subset=['Goal-Scoring','Assist-Creation', 'Attack','Dribbling','Possession', 'Defense','Physical','Goalkeeping'])
    
    st.dataframe(styled_df, 
                 width="stretch", 
                 hide_index=True,
                 height = 500)
    
    filtered_df['Player Info'] = filtered_df['Player'] + " (" + filtered_df['Age'].astype(str) + ")"
    report_cols = ['Player Info','Position', 'Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession', 'Defense', 'Physical','Goalkeeping', 'Grade']

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

            plt.figtext(0.5, 0.9325, f"Season: {Season_filter} + Age > {age_range[0]} + Age < {age_range[1]}", 
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


elif page == "Two Player Comparison Tool":
    st.write("""---""")
    st.title("3 - Two Player Comparison Tool")
    st.write("Create a performance radar comparison on the outfield players based on our metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Player Settings")
    df = df[df.Position != "GK"]
    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]

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

    categories = ['Goal-Scoring','Assist-Creation', 'Attack','Dribbling', 'Possession', 'Defense', 'Physical']

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
                   .format(precision=2, subset=['Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession', 'Defense','Physical'])
    
    st.dataframe(styled_df3, 
                 width="stretch", 
                 hide_index=True,
                 height = 107)

    comparison_df['Player Info'] = comparison_df.index + " (" + comparison_df['Age'].astype(str) + ")"
    comparison_cols = ['Player Info', 'Team', 'Goal-Scoring','Assist-Creation', 'Attack','Dribbling','Possession', 'Defense', 'Physical', 'Grade']
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

elif page == "Three Player Comparison Tool":
    st.write("""---""")
    st.title("4 - Three Player Comparison Tool")
    st.write("Create a performance radar comparison on the outfield players based on our metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Player Settings")
    df = df[df.Position != "GK"]
    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]

    Season_filter = st.selectbox("Season:", 
                                df['Season'].unique())
    
    df_SF = df[df['Season']== Season_filter]

    League_filter = st.selectbox("League:", 
                                df_SF['League'].unique())
       
    df_LF = df_SF[df_SF['League'] == League_filter]

    Position_filter3 = st.selectbox("Position:", df['Position'].unique())
    df_PF = df_LF[df_LF['Position'] == Position_filter3]

    sorted_teams = sorted(df_PF['Team'].unique().tolist())

    col1, col2, col3 = st.columns(3)

    with col1:
        t1 = st.selectbox("Select Team 1:", sorted_teams, key="team1")
        df3_TF = df_PF[df_PF['Team'] == t1]

    with col2:
        idx2 = 1 if len(sorted_teams) > 1 else 0
        t2 = st.selectbox("Select Team 2:", sorted_teams, index=idx2, key="team2")
        df4_TF = df_PF[df_PF['Team'] == t2]

    with col3:
        idx3 = 2 if len(sorted_teams) > 2 else 0
        t3 = st.selectbox("Select Team 3:", sorted_teams, index=idx3, key="team3")
        df5_TF = df_PF[df_PF['Team'] == t3]

    col4, col5, col6 = st.columns(3)

    with col4:
        list1 = sorted(df3_TF['Player'].unique())
        p1 = st.selectbox("Select Player 1", sorted(df3_TF['Player'].unique()), key="p1")
    with col5:
        list2 = [p for p in sorted(df4_TF['Player'].unique()) if p != p1]
        p2 = st.selectbox("Select Player 2", sorted(df4_TF['Player'].unique()), key="p2")
    with col6:
        list3 = [p for p in sorted(df5_TF['Player'].unique()) if p not in [p1, p2]]
        p3 = st.selectbox("Select Player 3", sorted(df5_TF['Player'].unique()), key="p3")

    categories = ['Goal-Scoring','Assist-Creation','Attack', 'Dribbling', 'Possession', 'Defense', 'Physical']

    def get_stats(df_source, player_name):
        return df_source[df_source['Player'] == player_name][categories].values.flatten().tolist()

    stats1 = get_stats(df3_TF, p1)
    stats2 = get_stats(df4_TF, p2)
    stats3 = get_stats(df5_TF, p3)

    fig = go.Figure()

    radar_data = [(stats1, p1, 'blue'), (stats2, p2, 'red'), (stats3, p3, 'green')]

    for stats, name, color in radar_data:
        fig.add_trace(go.Scatterpolar(
            r=stats,
            theta=categories,
            fill='toself',
            name=name,
            line_color=color
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=650,
        margin=dict(l=80, r=80, t=100, b=80),
        legend=dict(title=dict(
                    text="<span style='color:black'><b>Selected Players:</b></span><br> ",                    
                    font=dict(size=16)),
                    orientation="v",    
                    yanchor="top",
                    y=1,               
                    xanchor="left",
                    x=0.8,
                    font=dict(size=14)))

    st.plotly_chart(fig, width='stretch')

    st.subheader("Direct Comparison Table")

    comparison_df = pd.concat([
        df3_TF[df3_TF['Player'] == p1],
        df4_TF[df4_TF['Player'] == p2],
        df5_TF[df5_TF['Player'] == p3]
    ]).set_index('Player')

    styled_df = comparison_df.style.map(style_grade_column, subset=['Grade'])\
        .format(precision=3, subset=categories)

    st.dataframe(styled_df, width='stretch', hide_index=False, height=142)

    comparison_df['Player Info'] = comparison_df.index + " (" + comparison_df['Age'].astype(str) + ")"
    comparison_cols = ['Player Info', 'Team'] + categories + ['Grade']
    report_data = comparison_df[comparison_cols]

    st.write("---")

    if st.button(f"🖼️ Generate H2H Report ({p1} vs {p2} vs {p3})", icon=":material/compare_arrows:"):
        
        if not report_data.empty:

            num_vars = len(categories)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

            angles += angles[:1]
            stats1 += stats1[:1]
            stats2 += stats2[:1]
            stats3 += stats3[:1]

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

            ax_radar.plot(angles, stats3, color='green', linewidth=2, label=p3)
            ax_radar.fill(angles, stats3, color='green', alpha=0.25)

            ax_radar.set_thetagrids(np.degrees(angles[:-1]), categories)
            ax_radar.tick_params(axis='x', pad=15)
            ax_radar.set_rlabel_position(25)
            ax_radar.set_yticks([25, 50, 75, 100])
            ax_radar.set_yticklabels(["25", "50", "75", "100"], color="black", size=8)
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
            table.set_fontsize(10)
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
                    elif row == 2:
                        cell.set_facecolor('#FFF0F0')
                    elif row == 3:
                        cell.set_facecolor('#F0FFF0')

                    if report_data.columns[col] == 'Grade':
                        grade_val = cell.get_text().get_text()
                        bg_color = get_grade_color(grade_val)
                        cell.set_facecolor(bg_color)
                        cell.set_text_props(weight='bold', color='black')

            fig.suptitle(f"Player Comparison Report", 
                    color="#000000", fontsize=22, fontweight='bold', y=0.98)
            
            plt.figtext(0.5, 0.93, f"{p1} & {p2} & {p3} (Season: {Season_filter} + League: {League_filter})", 
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
                file_name=f"H2H_Comparison_{p1}_{p2}_{p3}.png",
                mime="image/png"
            )

elif page == "Lineup Builder":
    st.write("""---""")
    st.title("5 - Lineup Builder")
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
            "RW": (85, 67),"CF": (110, 40),"LW": (85, 13),
        },
        "4-4-2": {
            "GK": (11, 40),
            "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
            "RCM": (60, 55),"LCM": (60, 25), "RM": (74, 67),"LM": (74, 13),
            "RF": (110, 55), "LF": (110, 25)
        },
         "4-2-3-1": {
            "GK": (11, 40),
            "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
            "RCM": (60, 55),"LCM": (60, 25),
            "RW": (85, 67), "AM": (85, 40), "LW": (85, 13),
            "CF": (110, 40)
        },
        "5-2-2-1": {
            "GK": (11, 40),
            "RCB": (33, 60), "CCB": (25,40), "LCB": (33, 20), "RWB": (48, 70), "LWB": (48, 10),
            "RCM": (60, 55), "LCM": (60, 25),
            "RW": (85, 67), "LW": (85, 13),
            "CF": (110, 40)
        },
        "5-3-2": {
            "GK": (11, 40),
            "RCB": (33, 60), "CCB": (25,40), "LCB": (33, 20), "RWB": (48, 70), "LWB": (48, 10),
            "RCM": (74, 60),"CM": (62, 40),"LCM": (74, 20),
            "RF": (110, 55), "LF": (110, 25)
        },
         "4-3-3 (3 CF's)": {
            "GK": (11, 40),
            "RCB": (30, 53),"LCB": (30, 27),"RB": (39, 70),"LB": (39, 10),
            "RCM": (64, 60),"CM": (52, 40),"LCM": (64, 20),
            "RF": (95, 60),"CF": (110, 40),"LF": (95, 20)
        },
        "5-3-2 (1 AM + 2 MF)": {
            "GK": (11, 40),
            "RCB": (33, 60), "CCB": (25,40), "LCB": (33, 20), "RWB": (48, 70), "LWB": (48, 10),
            "RAM": (74, 60),"CM": (62, 40),"LCM": (74, 20),
            "RF": (110, 55), "LF": (110, 25)
        },
        "5-2-3 (3 CF's)": {
            "GK": (11, 40),
            "RCB": (33, 60), "CCB": (25,40), "LCB": (33, 20), "RWB": (48, 70), "LWB": (48, 10),
            "RCM": (60, 55), "LCM": (60, 25),
            "RF": (95, 60),"CF": (110, 40),"LF": (95, 20)
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
         "RAM": "AM & W",
         "LAM": "AM & W",
         "AM": "AM & W",
         "LW": "AM & W",
         "RW": "AM & W",
         "LF": "CF",
         "RF": "CF",
         "CF": "CF"
    }

    if 'current_formation' not in st.session_state:
        st.session_state.current_formation = "4-3-3"
    if 'lineup' not in st.session_state:
        st.session_state.lineup = {}

    def reset_lineup():
        st.session_state.lineup = {}
        
    st.subheader("🛠️ Lineup Settings")

    selected_formation = st.selectbox("Choose Formation", 
                                        options=list(formations.keys()), 
                                        on_change=reset_lineup)

    st.subheader("📋 Select Your Eleven")

    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")

    footer_tag = "@TheStatsWay"

    outfield_categories =  ['Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession', 'Defense', 'Physical']
    metric_colors = ['#FFD700',"#FF00F2", '#FF4B4B', '#A020F0', '#1E90FF', '#32CD32', '#8B4513']
         
    plot_data = {}

    for pos, coords in formations[selected_formation].items():
        broad_category = PositionIndex.get(pos)
        
        pos_data = df[df['Position'] == broad_category]
        
        col_season, col_league, col_team, col_player = st.columns(4)

        with col_season:
            available_seasons = sorted(pos_data['Season'].unique().tolist(), reverse=True)
            season_choice = st.selectbox(f"Season ({pos})", 
                                         ["Select Season"] + available_seasons, 
                                         key=f"s_{pos}")

        with col_league:
            if season_choice != "Select Season":
                season_filtered_data = pos_data[pos_data['Season'] == season_choice]
                available_leagues = sorted(season_filtered_data['League'].unique().tolist())
            else:
                season_filtered_data = pd.DataFrame()
                available_leagues = []
                
            league_choice = st.selectbox(f"League ({pos})", 
                                         ["Select League"] + available_leagues, 
                                         key=f"l_{pos}")
        
        with col_team:
            if league_choice != "Select League" and not season_filtered_data.empty:
                team_filtered_data = season_filtered_data[season_filtered_data['League'] == league_choice]
                available_teams = sorted(team_filtered_data['Team'].unique().tolist())
            else:
                team_filtered_data = pd.DataFrame()
                available_teams = []

            team_choice = st.selectbox(f"Team ({pos})", 
                                       ["Select Team"] + available_teams, 
                                       key=f"t_{pos}")

        with col_player:
            available_players = []
            if team_choice != "Select Team" and not team_filtered_data.empty:
                team_pos_players = team_filtered_data[team_filtered_data['Team'] == team_choice]['Player'].tolist()
                taken = [name for p, name in st.session_state.lineup.items() if p != pos]
                available_players = [p for p in team_pos_players if p not in taken]

            current = st.session_state.lineup.get(pos, "Select Player")
            choice_index = 0
            if current in available_players:
                choice_index = available_players.index(current) + 1
                
            choice = st.selectbox(f"Player ({pos})", 
                                  ["Select Player"] + available_players, 
                                  index=choice_index,
                                  key=f"p_{pos}")

        if choice != "Select Player":
            st.session_state.lineup[pos] = choice
            
            p_row_filter = (df['Player'] == choice) & (df['Team'] == team_choice) & (df['League'] == league_choice) & (df['Season'] == season_choice)
            p_row = df[p_row_filter].iloc[0]
            
            if pos == "GK":
                stats = {"Goalkeeping": p_row.get('Goalkeeping', 0)}
            else:
                stats = p_row[outfield_categories].to_dict()

            plot_data[pos] = {
                "name": choice, 
                "grade": p_row['Grade'],
                "x": coords[0], 
                "y": coords[1], 
                "metrics": stats, 
                "team": f"{team_choice} ({season_choice})" 
            }

    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color="#1a7953", line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(7, 9))

    for pos, info in plot_data.items():
        grade_color = get_grade_color(info['grade'])
        px, py = info['x'], info['y']
        
        pitch.scatter(px, py, c=grade_color, s=1200, edgecolors='white', linewidth=2, ax=ax, zorder=3)
        pitch.annotate(str(info['grade']), xy=(px, py), va='center', ha='center', 
                    color='black', fontsize=12, fontweight='bold', ax=ax, zorder=4)
        
        playername = f"{info['name']} ({pos})"

        pitch.annotate(playername, xy=(px - 3, py), va='center', ha='center', 
                    color='white', fontsize=9, fontweight='bold', 
                    bbox=dict(facecolor='black', alpha=0.7, boxstyle='round,pad=0.2'), ax=ax, zorder=4)

        if pos == "GK":
            gk_val = info['metrics']['Goalkeeping']
            pitch.annotate(f"Goalkeeping: {gk_val:.0f}", xy=(px - 8, py), 
                            va='center', ha='center', color="red", fontsize=9, fontweight='bold', ax=ax, zorder=4,
                    path_effects=[plt.matplotlib.patheffects.withStroke(linewidth=1.5, foreground='black')],
                    bbox=dict(facecolor='black', alpha=0.8, boxstyle='round',pad=0.2),)
        else:
            for i, (val, color) in enumerate(zip(info['metrics'].values(), metric_colors)):
                horizontal_offset = (i - 3) * 3
                pitch.annotate(f"{val:.0f}", xy=(px - 8, py + horizontal_offset), 
                            va='center', ha='center', color=color, 
                            fontsize=8.5, fontweight='bold', 
                            path_effects=[plt.matplotlib.patheffects.withStroke(linewidth=1.5, foreground='black')],
                            bbox=dict(facecolor='black', alpha=1, boxstyle='round',pad=0.1),
                            ax=ax, zorder=4)

        pitch.annotate(info['team'], xy=(px - 5.5, py), va='center', ha='center', 
                    color="white", fontsize=9, fontweight='bold', ax=ax, zorder=4,
                    path_effects=[plt.matplotlib.patheffects.withStroke(linewidth=1.5, foreground='black')],
                    bbox=dict(facecolor='black', alpha=0.8, boxstyle='round',pad=0.2),)

    for i, (cat, col) in enumerate(zip(outfield_categories, metric_colors)):
        ax.scatter( (i * 12), 122, color=col, s=60, edgecolors='white')
        ax.text(1 + (i * 12.05), 122, cat, color='white', fontsize=5.5, fontweight='bold', va='center')

    ax.text(0.945, 0.04, footer_tag, transform=ax.transAxes, 
            color='Black', fontsize=8, fontweight='bold',
            ha='right', va='bottom', alpha=1)
            
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")

    st.download_button(
            label="📥 Download Lineup Image",
            data=buf.getvalue(),
            file_name=f"{selected_formation}_Lineup_Builder.png",
            mime="image/png")
        
elif page == "Scatter Plot":
    st.write("""---""")
    st.title("6 - Simple Scatter Plot")
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
    allowed_metrics = ["Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession", "Defense","Physical","Age"]
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
        
        ax.text(row[x_axis], row[y_axis]-3, 
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
    
elif page == "Team Scatter Plot":
    st.write("""---""")
    st.title("7 - Team Scatter Plot")
    st.write("Create a plot with the desired combination of the variables for a team.")
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
   
    df_PF = df_LF[df_LF['Team']== Team_filter]

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

    st.subheader("📊 Plot Settings")
    st.info(
    """
    The color of the player plot reflects the color of their grade where :
    Elite - S (Dark Green) to Very Poor - F (Red)
    """, icon="ℹ️")
    allowed_metrics = ["Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession", "Defense","Physical","Age"]
    variables = [m for m in allowed_metrics if m in df_AF.columns]
    
    x_axis = st.selectbox("X-Axis (Horizontal)", 
                        variables, 
                        index=0)

    y_axis = st.selectbox("Y-Axis (Vertical)", 
                                  variables, 
                                  index=1)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#333333")
    ax.set_facecolor("#f7f7f7")

    for i, row in df_AF.iterrows():
        ax.scatter(row[x_axis], row[y_axis], 
                color= get_grade_color(row['Grade']), 
                s=200, 
                edgecolors='black', 
                alpha=0.8)
        
        ax.text(row[x_axis], row[y_axis]-2.5, 
                row['Player'], 
                color='black', 
                ha='center', fontsize=7)

    ax.set_title(f"{Team_filter}s Report: {x_axis} & {y_axis}", color='white', fontsize=18, fontweight='bold', pad=30)
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
            file_name=f"{Season_filter}_{League_filter}_{Team_filter}_{x_axis}_{y_axis}_Analysis.png",
            mime="image/png")
    
elif page == "Interactive Plot":
    st.write("""---""")
    st.title("8 - Interactive Plot")
    st.write("Create an interactive plot with the desired combination of the variables.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]
    df = df[df.Position != "GK"]

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
    st.title("9 - Player Report Card")
    st.write("Create a player report card for the player you want.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    df = df[df.Position != "GK"]
    df = df.drop(columns=['Goalkeeping'])

    variables = ['Attack','Goal-Scoring','Assist-Creation','Dribbling','Possession', 'Defense','Physical']

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
        ax_text.text(0, 
                     0.85 - (i * 0.1), line, color='white', 
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

    colors = ["#E6194B","#3CB44B","#FFE119","#4363D8","#F58231","#911EB4"]

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
    st.title("10 - Player Similarity Tool")
    st.write("Find the players with the most similar data profile based on our metrics.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    st.subheader("🛠️ Player Settings")

    df = df[df.Position != "GK"]
    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]

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

    sim_features = ['Goal-Scoring','Assist-Creation','Attack', 'Dribbling', 'Defense', 'Possession', 'Physical']

    def find_similar_players(df_supp_pos, target_player, target_season):
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
        
        #results = results[(results['Age'] >= age_range[0]) & (results['Age'] <= age_range[1])]
        results = results[(results['Similarity_Score'] > 0)]
        results = results.sort_values(by='Similarity_Score', ascending=False)
        
        return results

    st.write("""---""")
    st.subheader("🛠️ Similar Profiles Settings")

    min_age = int(df_supp_pos['Age'].min())
    max_age = int(df_supp_pos['Age'].max())
    
    if min_age < max_age:
        age_range = st.slider(
            "Age Range:",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
    )
    else:
        age_range = (min_age, min_age)

    col_sim1, col_sim2 = st.columns(2)

    with col_sim1:
        sim_seasons = sorted(df_supp_pos['Season'].unique().tolist())
        sim_season_filter = st.multiselect("Search in Season:", 
                                         options=sim_seasons,
                                         default=sim_seasons)

    with col_sim2:
        sim_leagues = sorted(df['League'].unique().tolist())
        sim_leagues_filter = st.multiselect("League Filter:",
                                options=sim_leagues,
                                default=sim_leagues)

    st.subheader("⤵️ Search Button")

    if st.button("🔍 Find Similar Profiles"):
        with st.spinner(f'Analyzing {selected_player}\'s Profile in the {Season_filter} season...'):
            
            similar_df = find_similar_players(df_supp_pos, selected_player, Season_filter)
            similar_df = similar_df[(similar_df['Age'] >= age_range[0]) & (similar_df['Age'] <= age_range[1])]
            similar_df = similar_df[similar_df["Season"].isin(sim_season_filter)]
            similar_df = similar_df[similar_df["League"].isin(sim_leagues_filter)]

            if similar_df is not None:
                st.write(f"### Top 10 Similar Profiles to {selected_player} ({Season_filter}):")
                
                display_cols = ['Season', 'League', 'Team', 'Player', 'Age', 'Position', 'Similarity_Score']
                display_df = similar_df[display_cols].copy()
                display_df['Similarity Accuracy'] = (display_df['Similarity_Score'] * 100).map('{:,.1f}%'.format)
                display_df = display_df.head(10)

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
    st.title("11 - Team Comparison Tool")
    st.write("Create a teams profile per position based on the mean values of the players.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]
    df = df[df.Position != "GK"]

    st.subheader("🛠️ Team Settings")

    sim_features = ['Goal-Scoring','Assist-Creation','Attack','Dribbling', 'Possession', 'Defense', 'Physical']

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
    st.title("12 - Player Progression in a Team")
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
                   .format(precision=2, subset=['Goal-Scoring','Assist-Creation','Attack','Dribbling','Possession', 'Defense','Physical','Goalkeeping'])

    st.dataframe(styled_df,
                 column_order=("Season","League","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack",'Dribbling',"Possession","Defense","Physical","Goalkeeping","PosRank","Grade"),
                 width="stretch",
                 hide_index=True,
                 height = 210)
    
    st.write("""---""")

    plot_df = df_PF[df_PF['Player'] == Player_filter].sort_values('Season')
    target_seasons = ['2021/22','2022/23','2023/24', '2024/25', '2025/26']
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
        metrics = ['Goal-Scoring','Assist-Creation', 'Attack','Dribbling', 'Possession', 'Defense', 'Physical']
        colors = ['#E63946',"#DAE639", '#1A73E8',"#A723CF", '#2A9D8F', '#F4A261', '#8D99AE']

    season_colors = ["#C2C2C2","#62CBDD","#068AA5","#024468","#000136"]
    
    fig = plt.figure(figsize=(20, 14), facecolor='#F8F9FA')
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.5, 3], height_ratios=[1, 1], hspace=0.3, wspace=0.2)

    ax_info = fig.add_subplot(gs[:, 0])
    ax_info.axis('off')
    ax_info.text(0.05, 1.05, Player_filter.upper(), fontsize=28, fontweight='bold')
    ax_info.text(0.05, 1.025, f"{plot_df.iloc[-1]['Team']} | {plot_df.iloc[-1]['Age']}y", fontsize=14, color='#6C757D', fontweight='bold')
    y_offset = 0.975

    for _, row in plot_df.iloc[::-1].iterrows():
        ax_info.text(0.05, y_offset, f"▼ Season {row['Season']} ▼", fontsize=13, color='#6C757D', fontweight='bold')
        ax_info.text(0.05, y_offset-0.02, f"League: {row['League']}", fontsize=12)
        ax_info.text(0.05, y_offset-0.04, f"Position: {row['Position']}", fontsize=12)
        ax_info.text(0.05, y_offset-0.06, f"Grade: {row['Grade']}", fontsize=12, fontweight='bold')
        y_offset -= 0.1

    ax_info.text(0.05, 0.45, "DEVELOPMENT SUMMARY", fontsize=14, fontweight='bold')

    for i, m in enumerate(metrics):
        diff = plot_df.iloc[-1][m] - plot_df.iloc[0][m]
        color = '#2A9D8F' if diff >= 0 else '#E63946'
        symbol = "▲" if diff >= 0 else "▼"
        y_pos = (0.35) - (i * 0.065)
        ax_info.text(0.05, y_pos, m, fontsize=13, color='#6C757D', fontweight='bold')
        ax_info.text(0.55, y_pos, f"{symbol} {abs(diff):.1f}", fontsize=12, fontweight='bold', color=color)

    ax_bar = fig.add_subplot(gs[0, 1])
    y = np.arange(len(metrics))

    num_seasons = len(season_labels) 
    width = (6 - num_seasons)/11

    for i in range(num_seasons):
        offset = (width * (num_seasons-1) / 2) - (i * width)
        ax_bar.barh(y + offset, plot_df.iloc[i][metrics], width, 
                    label=season_labels[i], color=season_colors[i], alpha=1 if i < num_seasons-1 else 1.0, edgecolor='black')  #The outline color

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
    st.title("13 - Player Search Hub ")
    st.write("Find players that match your performance requirements.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")
    
    df = df[["Season","League","Player","Team","Age","Position","Goal-Scoring","Assist-Creation","Attack","Dribbling","Possession",
            "Defense","Physical","PosRank","Grade"]]
    
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
    assist_min = st.slider("Minimum Assist-Creation", 0, 100, 0)
    attack_min = st.slider("Minimum Attack", 0, 100, 0)
    dribbling_min = st.slider("Minimum Dribbling", 0, 100, 0)
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
        (df['Assist-Creation'] >= assist_min) &
        (df['Attack'] >= attack_min) &
        (df['Dribbling'] >= dribbling_min) &
        (df['Possession'] >= poss_min) &
        (df['Defense'] >= def_min) &
        (df['Physical'] >= phys_min)
    ]
  
    st.divider()
    st.title("🔍 Player Search Hub")
    st.markdown(f"Finding players that match your requirements.")

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10  = st.columns(10)
    col1.metric("Results Found", len(filtered_df))
    col2.metric("Avg. Age", f"{round(filtered_df['Age'].mean(), 1) if not filtered_df.empty else '0'}")
    col3.metric("Most Common Grade", f"{filtered_df['Grade'].mode()[0] if not filtered_df.empty else 'N/A'}")
    col4.metric("Avg. Goal-Scoring", f"{round(filtered_df['Goal-Scoring'].mean(), 1) if not filtered_df.empty else '0'}")
    col5.metric("Avg. Assist-Creation", f"{round(filtered_df['Assist-Creation'].mean(), 1) if not filtered_df.empty else '0'}")
    col6.metric("Avg. Attack", f"{round(filtered_df['Attack'].mean(), 1) if not filtered_df.empty else '0'}")
    col7.metric("Avg. Dribbling", f"{round(filtered_df['Dribbling'].mean(), 1) if not filtered_df.empty else '0'}")
    col8.metric("Avg. Possession", f"{round(filtered_df['Possession'].mean(), 1) if not filtered_df.empty else '0'}")
    col9.metric("Avg. Defense", f"{round(filtered_df['Defense'].mean(), 1) if not filtered_df.empty else '0'}")
    col10.metric("Avg. Physical", f"{round(filtered_df['Physical'].mean(), 1) if not filtered_df.empty else '0'}")

    filtered_df['Skill Score'] = filtered_df[['Goal-Scoring','Assist-Creation', 'Attack', 'Dribbling' , 'Possession', 'Defense', 'Physical']].mean(axis=1)

    if not filtered_df.empty:
        display_cols = ['Season','League','Player', 'Team', 'Age', 'Position', 'Goal-Scoring','Assist-Creation','Attack', 'Dribbling', 'Possession', 'Defense', 'Physical','Grade', 'Skill Score']
        
        st.dataframe(
            filtered_df[display_cols].sort_values('Skill Score', ascending=False),
            width='stretch',
            height = 770,
            hide_index=True,
            column_config={
                "Skill Score": st.column_config.ProgressColumn(
                    "Metric Average",
                    help="Average of the 6 core scouting metrics",
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
    st.title("14 - Team Recruitment Identifier Hub ")
    st.write("Find players that fit the teams needs.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.subheader("🛠️ Team Search Settings")

    season_filter = st.selectbox("Filter by the Season that the Team played in:",
                                df['Season'].unique())

    df_clean = df
    df = df[df['Season'] == season_filter]
    #df_clean = df[df['Season'] == season_filter] 

    league_filter = st.selectbox("Filter by a League that the Team played in:",
                                df['League'].unique())

    df_LF = df[df['League'] == league_filter]

    metrics = ['Goal-Scoring','Assist-Creation', 'Attack', 'Dribbling' , 'Possession', 'Defense', 'Physical','Goalkeeping']

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

    Seasons = df_clean['Season'].unique().tolist()
    SeasonsReplacementFilter = st.multiselect("Season Filter:",
                                options=Seasons,
                                default=season_filter)

    if SeasonsReplacementFilter:
        df_clean = df_clean[df_clean["Season"].isin(SeasonsReplacementFilter)]

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
                            
                            display_cols = ['Season','Player', 'Team', 'Age'] + needs + ['Grade', 'Solution Score']
                            
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

    outfield_metrics = ['Goal-Scoring','Assist-Creation', 'Attack', 'Dribbling', 'Possession', 'Defense', 'Physical']
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

                        display_cols = ['Season','Player', 'Team', 'Age'] + compare_metrics + ['Value Added']
                        
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

                    #upgrade_targets = upgrade_targets.sort_values(by='Avg Value Added', ascending=False).head(10)
                    upgrade_targets = upgrade_targets.sort_values(by='Avg Value Added', ascending=False)

                    with st.expander(f"**POSITIONAL UPGRADES: {pos}** ({len(potential_upgrades)} targets found)"):
                        
                        st.write(f"Showing players who are, on average, better than your current {pos} group:")
                        
                        display_cols = ['Season','Player', 'Team', 'Age'] + compare_metrics + ['Avg Value Added']
                        
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

elif page == "Squad Builder Report":
    st.write("""---""")
    st.title("15 - Squad Builder Report for 2026/27 Season")
    st.write("Build your Team's squad for next season.")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    ordered_positions = ["GK", "CB", "FB & WB", "MF", "AM & W", "CF"]
    positions_map = {
    "GK": "Goalkeepers",
    "CB": "Center-Backs",
    "FB & WB": "Full-Backs & Wing-Backs",
    "MF": "Midfielders",
    "AM & W": "Attacking Mids & Wingers",
    "CF": "Center-Forwards"
    }
    outfield_cats = ['Goal-Scoring','Assist-Creation', 'Attack', 'Dribbling', 'Possession', 'Defense', 'Physical']
    colors = {'Goal-Scoring': 'orange', 'Assist-Creation':'yellow','Attack': 'red', 'Dribbling': 'violet', 
            'Possession': 'blue', 'Defense': 'green', 'Physical': 'gray'}

    st.subheader("🏢 Selected Club to Manage")

    df_26 = df[df['Season'] == '2025/26'].copy()
    df_26['Player'] = df_26.apply(lambda x: f"{x['Player']} ({x['Age']} - {x['Position']})", axis=1)

    col_l, col_r = st.columns(2)

    with col_l:
        league_filter = st.selectbox(
            "Baseline League:",
            options=sorted(df_26['League'].unique()),
            help="Filter the list of teams to set your baseline.")

    available_teams = df_26[df_26['League'] == league_filter]['Team'].unique()

    with col_r:
        base_team = st.selectbox(
            "Select Base Team (Baseline):", 
            options=sorted(available_teams))

    if 'active_squad' not in st.session_state or st.session_state.get('last_team') != base_team:
        initial_data = df_26[df_26['Team'] == base_team].copy()
        st.session_state.active_squad = initial_data.to_dict('records')
        st.session_state.last_team = base_team
        
        baseline_avgs = {}
        for pos in ordered_positions:
            pos_df = initial_data[initial_data['Position'] == pos]
            if not pos_df.empty:
                if pos == "GK":
                    baseline_avgs[pos] = pos_df['Goalkeeping'].mean()
                else:
                    baseline_avgs[pos] = pos_df[outfield_cats].mean()
        st.session_state.baseline = baseline_avgs

    st.header("🔍 Scouting Network")
    current_names = [p['Player'] for p in st.session_state.active_squad]
    all_players_pool = df_26[~df_26['Player'].isin(current_names)]

    target_league = st.selectbox(
        "Search League:", 
        options=[""] + sorted(all_players_pool['League'].unique().tolist()),
        key="sb_league"
    )

    team_options = [""]
    if target_league != "":
        all_players_pool2 = all_players_pool[all_players_pool['League'] == target_league]
        team_options = sorted(all_players_pool2['Team'].unique().tolist())

    target_team = st.selectbox(
        "Search Team:", 
        options=[""] + team_options,
        key="sb_team"
    )

    player_options = [""]
    if target_team != "":
        all_players_pool3 = all_players_pool[all_players_pool['Team'] == target_team]
        player_options = sorted(all_players_pool3['Player'].unique().tolist())

    target_player = st.selectbox(
        "Search Player:", 
        options=[""] + player_options,
        key="sb_player"
    )

    if st.button("➕ Sign Player") and target_player != "":
        new_data = df_26[df_26['Player'] == target_player].to_dict('records')[0]
        st.session_state.active_squad.append(new_data)
        st.rerun()

    st.divider()
    col_roster, col_analysis = st.columns([2, 1])
    squad_df = pd.DataFrame(st.session_state.active_squad)

    with col_roster:
        with st.expander("➕ Add Custom Player (Not in Database)"):
            with st.form("custom_player_form"):
                c1, c2, c3 = st.columns(3)
                new_name = c1.text_input("Player Name")
                new_team = c2.text_input("Team Name")
                new_age = c3.number_input("Player Age", step=1)

                new_pos = st.selectbox("Position", ["GK", "CB", "FB & WB", "MF", "AM & W", "CF"])
                                
                submit_custom = st.form_submit_button("Add to Roster")
                
                final_name = f"{new_name} ({new_age} - {new_pos})"

                if submit_custom:
                    if new_name and new_team:
                        new_player = {
                            'Player': final_name,
                            'Team': new_team,
                            'Position': new_pos,
                            'Age': new_age
                        }
                        
                        for cat in outfield_cats:
                            if cat not in new_player: new_player[cat] = 0
                        if 'Goalkeeping' not in new_player: new_player['Goalkeeping'] = 0

                        st.session_state.active_squad.append(new_player)
                        st.success(f"Added {new_name} to {new_pos} roster!")
                        st.rerun()
                    else:
                        st.error("Please provide both a Name and a Team.")

        base_grey = "#f5f5f5"
        signing_green = "#87ff91"
        card_text_color = "#000000"

        for pos_label in ordered_positions:
            pos_squad = squad_df[squad_df['Position'] == pos_label]
            
            if not pos_squad.empty:
                full_name = positions_map.get(pos_label, pos_label)
                st.markdown(f"### {full_name}")

                with st.container(border=True):
                    for _, player in pos_squad.iterrows():
                        is_original = player['Team'] == base_team
                        current_bg = base_grey if is_original else signing_green
                        border_color = "#cccccc" if is_original else "#2eb840"              
                        
                        st.markdown(f"""
                            <div style="
                                background-color: {current_bg}; 
                                padding: 10px; 
                                border-radius: 8px; 
                                border: 1px solid {border_color};
                                color: {card_text_color};
                                margin-bottom: 10px;
                                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
                            ">
                        """, unsafe_allow_html=True)

                        with st.container(border=True):
                            c1, c_grade, c2 = st.columns([3.5, 1.5, 1])
                            
                            c1.markdown(f"**{player['Player']}** | {player['Team']}")
                            
                            if pos_label == "GK":
                                c1.markdown(f":green[**GK: {player['Goalkeeping']:.0f}**]")
                            else:
                                stat_line = " • ".join([f":{colors[cat]}[{cat[:2].upper()}:{player[cat]:.0f}]" for cat in outfield_cats])
                                c1.markdown(stat_line)

                            c_grade.markdown(f"""
                                <div style="
                                    background-color: white;
                                    border: 2px solid {border_color};
                                    border-radius: 6px;
                                    padding: 5px;
                                    text-align: center;
                                    line-height: 1.2;
                                ">
                                    <small style="color: gray; font-weight: bold; text-transform: uppercase;">Grade</small><br>
                                    <span style="font-size: 20px; font-weight: 800; color: #333;">{player['Grade']}</span>
                                </div>
                            """, unsafe_allow_html=True)

                            idx = next(i for i, p in enumerate(st.session_state.active_squad) if p['Player'] == player['Player'])
                            if c2.button("❌", key=f"rem_{player['Player']}_{pos_label}_{idx}"):
                                st.session_state.active_squad.pop(idx)
                                st.rerun()

                        st.markdown("</div>", unsafe_allow_html=True)

    with col_analysis:
        st.subheader("📈 Comparison vs Baseline")
        st.caption(f"Comparing current squad to original **{base_team}**")

        for pos_label in ordered_positions:
            current_pos_df = squad_df[squad_df['Position'] == pos_label]
            full_pos_name = positions_map.get(pos_label, pos_label)
            
            with st.expander(f"{full_pos_name} Analysis", expanded=True):
                if not current_pos_df.empty:
                    base = st.session_state.baseline.get(pos_label)
                    
                    g1, g2 = st.columns(2)
                    
                    cur_count = len(current_pos_df)
                    base_count = st.session_state.get('baseline_counts', {}).get(pos_label, cur_count) 
                    count_diff = cur_count - base_count
                    g1.metric("Number of Players", f"{cur_count}")

                    cur_age = current_pos_df['Age'].mean()
                    g2.metric("Avg Age", f"{cur_age:.1f}")

                    st.divider()

                    if pos_label == "GK":
                        cur_val = current_pos_df['Goalkeeping'].mean()
                        base_val = base if isinstance(base, float) else (base['Goalkeeping'] if base is not None else cur_val)
                        diff = cur_val - base_val
                        symbol = "▲" if diff > 0 else "▼" if diff < 0 else "—"
                        
                        st.metric("Goalkeeping", f"{cur_val:.1f}", delta=f"{diff:.1f} {symbol}")
                    
                    else:
                        cur_means = current_pos_df[outfield_cats].mean()
                        m_col1, m_col2 = st.columns(2)
                        
                        for i, cat in enumerate(outfield_cats):
                            cur_val = cur_means[cat]
                            base_val = base[cat] if (base is not None and cat in base) else cur_val
                            diff = cur_val - base_val
                            symbol = "▲" if diff > 0 else "▼" if diff < 0 else "—"
                            
                            target_col = m_col1 if i % 2 == 0 else m_col2
                            target_col.metric(
                                label=cat, 
                                value=f"{cur_val:.1f}", 
                                delta=f"{diff:.1f} {symbol}"
                            )
                        
                        if base is None:
                            st.caption("⚠️ No baseline technical data for this position.")
                else:
                    st.caption("Position vacant.")

    st.divider()
    st.subheader("🏁 Finalize Squad Report")

    if st.button("🖼️ Generate Image Report"):
     if not squad_df.empty:
        num_players = len(squad_df)
        num_groups = squad_df['Position'].nunique()
        fig_height = (num_players * 0.4) + (num_groups * 0.8)
        
        fig, ax = plt.subplots(figsize=(12, fig_height), facecolor='white')
        ax.set_facecolor('white')
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.axis('off')

        ax.text(5, 98, f"SQUAD BUILDING REPORT: {base_team}", fontsize=16, fontweight='bold', color='#1a7953')
        ax.text(5, 95.5, "Preparing the 2026/27 Season | Squad Composition", fontsize=9, color='gray')
        ax.axhline(94, color='black', linewidth=1.2, xmin=0.05, xmax=0.95)
        ax.text(95, 95.5, "@TheStatsWay", horizontalalignment='right', size=9, color="#000000", fontweight='bold')

        header_y = 91.5
        ax.text(5, header_y, "AGE - PLAYER", fontsize=9, fontweight='bold', color='#333333')
        ax.text(43.5, header_y, "PREVIOUS CLUB", fontsize=9, fontweight='bold', color='#333333')
        ax.text(60, header_y, "GRADE", fontsize=9, fontweight='bold', color='#333333')
        ax.text(70, header_y, "METRICS", fontsize=9, fontweight='bold', color='#333333')

        y_pos = 89.5
        for pos_label in ordered_positions:
            pos_squad = squad_df[squad_df['Position'] == pos_label]
            
            if not pos_squad.empty:
                rect = plt.Rectangle((4, y_pos-1), 92, 2.2, color='#f0f2f6', zorder=0)
                ax.add_patch(rect)
                ax.text(5, y_pos, f"{pos_label}", fontsize=10, fontweight='bold', color='black', va='center')
                y_pos -= 3.5

                for _, player in pos_squad.iterrows():
                    ax.text(10, y_pos, f"{player['Player']}", fontsize=9, fontweight='bold')
                    ax.text(5, y_pos, f"({player['Age']}y)", fontsize=8, color='gray')

                    ax.text(44, y_pos, f"{player['Team']}", fontsize=8)
                    ax.text(62, y_pos, f"{player['Grade']}", fontsize=8)

                    if pos_label == "GK":
                        ax.text(70, y_pos, f"Goalkeeping: {player['Goalkeeping']:.0f}", color='#333333', fontsize=7.5)
                    else:
                        metrics_str = " | ".join([f"{cat[:2]}:{player[cat]:.0f}" for cat in outfield_cats])
                        ax.text(70, y_pos, metrics_str, fontsize=7.5, color='#444444')

                    y_pos -= 3.5 
                    ax.axhline(y_pos+2.2, color='#eeeeee', linewidth=0.5, xmin=0.05, xmax=0.95)

        plt.tight_layout()
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', dpi=200)
        st.download_button(
            label="💾 Download PNG Report",
            data=buf.getvalue(),
            file_name=f"{base_team}_squad_report.png",
            mime="image/png"
        )

elif page == "Profile Clusters":
    st.write("""---""")
    st.title("16 - Position Profile Clusters")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.set_page_config(layout="wide")
    st.subheader("🛠️ Search Settings")
        
    def apply_ward_clustering(dataframe, n_clusters=4):

            default_metrics = ["Goal-Scoring","Assist-Creation", "Attack", "Dribbling", "Possession", "Defense", "Physical"]
            include_age = st.checkbox("Include ***Age*** metric in the Clustering?", value=False)
            current_metrics = default_metrics.copy()

            if include_age:
                    current_metrics.append("Age")

            metrics = current_metrics
            df_c = dataframe.dropna(subset=metrics).copy()

            if len(df_c) < n_clusters:
                df_c['Ward_Cluster'] = "Insufficient Data"
                return df_c
                            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_c[metrics])
                            
            ward_model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
            df_c['Ward_Cluster'] = ward_model.fit_predict(X_scaled)
            df_c['Ward_Cluster'] = df_c['Ward_Cluster'].apply(lambda x: f"Profile {x+1}")

            pca = PCA(n_components=2)
            pca_components = pca.fit_transform(X_scaled)
            df_c['PC1'] = pca_components[:, 0]
            df_c['PC2'] = pca_components[:, 1]

            loadings = pd.DataFrame(
                pca.components_.T, 
                columns=['PC1', 'PC2'], 
                index=metrics)

            with st.expander("🔍 What does the X and Y axis mean?"):
                st.write("Since we used PCAs, the axis are mathematical blends of all the metrics. Here is how much each stat contributed to the axis orientation:")
                st.dataframe(loadings.style.background_gradient(cmap='coolwarm'))    
            return df_c

    league_hierarchy = {
            'Liga Portugal': 1, 
            'Liga 2': 2, 
            'Liga 3': 3, 
            'Campeonato de Portugal': 4,
            'Liga Revelação U23': 5
        }

    viz_pos = st.selectbox("Select Position:", 
                            ["CB", "FB & WB", "MF", "AM & W", "CF"])

    col1, col2 = st.columns(2)

    with col1:
            season_list = sorted(df['Season'].dropna().unique().tolist(), reverse=True)
            # CHANGED: selectbox is now a multiselect. Default is set to the most recent season.
            selected_seasons = st.multiselect("Filter by Season(s):", options=season_list, default=[season_list[0]])
            
    # CHANGED: We use .isin() to filter for multiple items in a list instead of ==
    df_season = df[df['Season'].isin(selected_seasons)]

    with col2:
            raw_leagues = df_season['League'].dropna().unique().tolist()
            league_list = sorted(raw_leagues, key=lambda x: league_hierarchy.get(x, 99))
            selected_league = st.selectbox("Filter by League:", league_list)

    df_league = df_season[df_season['League'] == selected_league]

    viz_df = df_league[df_league['Position'] == viz_pos].copy()

    # The code will naturally bypass rendering the chart if the user removes all seasons (viz_df becomes empty)
    if not viz_df.empty:
            st.divider()
                        
            n_profiles = st.slider("Number of Tactical Profiles to find:", 
                                min_value=2, 
                                max_value=9, 
                                value=4)
                        
            viz_df = apply_ward_clustering(viz_df, n_clusters=n_profiles)

            if "Ward_Cluster" in viz_df.columns and viz_df['Ward_Cluster'].iloc[0] != "Insufficient Data":
                        
                orig_profiles = sorted(viz_df['Ward_Cluster'].unique())
                        
                with st.expander("🛠️ Rename Profiles Names"):
                    st.caption("Give custom tactical names to the algorithmic clusters based on where they land on the map. Check some profiles in the end to rename them!")
                            
                    rename_cols = st.columns(len(orig_profiles))
                    rename_map = {}
                            
                    for i, p in enumerate(orig_profiles):
                        with rename_cols[i]:
                            custom_name = st.text_input(f"Rename {p}:", value=p, key=f"rename_{p}")
                            rename_map[p] = custom_name
                            
                    viz_df['Ward_Cluster'] = viz_df['Ward_Cluster'].map(rename_map)

                updated_profiles = sorted(viz_df['Ward_Cluster'].unique())
                selected_profile = st.selectbox("Specific Profile Filter:", ["All Profiles"] + updated_profiles)
                        
                if selected_profile != "All Profiles":
                    viz_df = viz_df[viz_df['Ward_Cluster'] == selected_profile]

                x_axis = 'PC1'
                y_axis = 'PC2'
                        
                viz_df['Player_Label'] = viz_df['Player'].apply(lambda x: f"<b>{x}</b>")
                        
                # CHANGED: Title formatting to combine all selected seasons with a comma
                seasons_display = ", ".join([str(s) for s in selected_seasons])
                title_str = f"Ward Clusters: {viz_pos} | Seasons: {seasons_display}"
                if selected_league != "All Leagues": title_str += f" | League: {selected_league}"
                if selected_profile != "All Profiles": title_str += f" | {selected_profile} Only"

                fig = px.scatter(
                    viz_df, x=x_axis, y=y_axis, 
                    color='Ward_Cluster',        
                    text='Player_Label',      
                    hover_name='Player',      
                    title=title_str,
                    height=900,
                    category_orders={"Ward_Cluster": updated_profiles},
                    hover_data={
                        'Team': True, 
                        'Age': True, 
                        'Ward_Cluster': True,
                        'Goal-Scoring': True, 
                        'Assist-Creation': True, 
                        'Attack': True,
                        'Possession': True, 
                        'Dribbling': True,  
                        'Defense': True, 
                        'Physical': True, 
                        'Player_Label': False 
                    }
                )
                
                fig.update_traces(
                    textposition='bottom center', 
                    textfont=dict(size=11),       
                    marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey'))
                )

                fig.update_layout(
                    plot_bgcolor='#EAEAEA',  
                    xaxis_title="PC1",        
                    yaxis_title="PC2",        
                    xaxis=dict(showgrid=True, gridcolor='white', zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=True, gridcolor='white', zeroline=False, showticklabels=False),
                    legend_title_text="Tactical Profiles"
                )
                
                # CHANGED: Replaced slashes and spaces in the seasons list so the PNG file saves correctly
                safe_season_string = "_".join([str(s) for s in selected_seasons]).replace("/", "-").replace(" ", "")
                
                chart_config = {
                    'displayModeBar': True,
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'PCA_Cluster_Map_{viz_pos}_{safe_season_string}',
                        'height': 900,
                        'width': 1600,
                    }
                }
                    
                st.plotly_chart(fig, use_container_width=True, config=chart_config)

                with st.expander("🔍 Some of the Profiles to use in the renaming section:"):
                    st.write("""                        
        - **CB :** Defensive CB, Ball-Playing CB, Wide Progressor CB, Physical Monster CB, Libero.
        - **FB & WB :** Defensive FB, Attacking FB, Playmaker, False Winger, Locomotive FB.
        - **MF :** Defensive MF, Ball Winner MF, Box-to-Box, Deep Lying Playmaker, Advanced Playmaker, Box Crasher.
        - **AM & W :** Playmaker, Winger, Dribbling Monster, Inside Forward, Pressing Forward, Shadow Striker.
        - **CF :** Poacher, Target Man, Pressing CF, False 9, Second Striker, Link-Up Foward.""")

    else:
            st.info("No players match this combination of filters. Try adjusting the Season, League, or Team.")


elif page == "Re-Sale Value Calculator":
    st.write("""---""")
    st.title("17 - Re-Sale Value Calculator")
    st.info(
    """
    Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23
    """, icon="ℹ️")

    st.set_page_config(layout="wide")
    
    def prepare_market_data(df):

        df = df[df['League'] != 'Liga Revelação U23']    
        df = df[df['League'] != 'Campeonato de Portugal']    
        #df = df[df['League'] != 'Liga 3']    
        df = df[df.Position != "GK"]

        df_m = df.copy().sort_values(['Player', 'Season'])

        league_hierarchy = {
            'Liga Portugal': 1,
            'Liga 2': 2,
            'Liga 3': 3
        }

        df_m['League_Level'] = df_m['League'].map(league_hierarchy).fillna(6)

        record_sales_dict = {
            "Benfica": 127000000, "Sporting CP": 66900000, "Porto": 60000000,
            "SC Braga": 32000000, "Famalicão": 24500000, "Gil Vicente": 23000000,
            "Vitória SC": 18000000, "Alverca": 7500000, "Casa Pia AC": 6500000,
            "Estrela Amadora": 6000000, "Tondela": 2500000, "AVS (Vilafranquense)": 3000000,
            "Arouca": 10000000, "Estoril": 6500000, "Moreirense": 5250000,
            "Nacional": 4500000, "Rio Ave": 7200000, "Santa Clara": 4000000,
            "Farense": 5500000, "Boavista": 2500000, "Chaves": 4000000,
            "Portimonense": 35000000, "Vizela": 5000000, "Marítimo": 4500000,
            "Paços de Ferreira": 7000000, "CF Os Belenenses": 5000000, "Académico de Viseu F.C.": 6000000,
            "Feirense": 7200000, "Felgueiras 1932": 850000, "Leixões": 2000000,
            "Lusitania FC Lourosa": 0, "Penafiel": 1400000, "Torreense": 4500000,
            "UD Oliveirense": 250000, "União de Leiria": 4000000, "Mafra": 4000000,
            "Vilaverdense": 0, "Sporting Covilhã": 100000, "Trofense": 250000,"Varzim": 700000,
            "1º Dezembro":0,"AD Marco 09": 0,"Amarante": 0, "Amora": 4000000, "Atlético CP": 0,
            "Caldas": 0, "Fafe": 0, "Lusitano Évora 1911": 0, "Paredes": 0, "Sanjoanense": 500000,
            "São João Ver": 0, "União Santarém": 0, "Anadia": 0, "Lusitânia": 0, "Oliveira Hospital": 0,
            "Vianense": 0, "Pêro Pinheiro": 0, "Canelas 2010": 50000, "Vitória Setúbal": 2750000, 
            "Real SC": 4000000, "Fontinhas": 0, "Moncarapachense": 0, "Montalegre":0, 
            "Vitória SC B": 1000000, "SC Braga B": 5000000, "Porto B": 2500000, "Benfica B": 2500000, "Sporting B": 5000000

}

        df_m['Team_Record_Sale'] = df_m['Team'].map(record_sales_dict).fillna(0).astype(int)

        Position_sales_dict = {
            "CB": 71600000,
            "FB & WB": 50000000,
            "MF": 121000000,
            "AM & W": 127000000,
            "CF": 85000000}

        df_m['Position_Record_Sale'] = df_m['Position'].map(Position_sales_dict).fillna(0).astype(int)

        if 'Cost' in df_m.columns:
            df_m['Cost'] = pd.to_numeric(df_m['Cost'], errors='coerce')
        else:
            df_m['Cost'] = np.nan
           
        sales_only = df_m.dropna(subset=['Sale'])
        season_sale_stats = sales_only.groupby('Season')['Sale'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'Season_Sale_Mean', 'median': 'Season_Sale_Median', 'max': 'Season_Sale_Max'})

        team_sale_stats = sales_only.groupby('Team')['Sale'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'Team_Sale_Mean', 'median': 'Team_Sale_Median', 'max': 'Team_Sale_Max'})

        league_sale_stats = sales_only.groupby('League')['Sale'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'League_Sale_Mean', 'median': 'League_Sale_Median', 'max': 'League_Sale_Max'})

        costs_only = df_m[df_m['Cost'] > 0].dropna(subset=['Cost'])

        season_cost_stats = costs_only.groupby('Season')['Cost'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'Season_Cost_Mean', 'median': 'Season_Cost_Median', 'max': 'Season_Cost_Max'})

        team_cost_stats = costs_only.groupby('Team')['Cost'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'Team_Cost_Mean', 'median': 'Team_Cost_Median', 'max': 'Team_Cost_Max'})

        league_cost_stats = costs_only.groupby('League')['Cost'].agg(['mean', 'median', 'max']).rename(
            columns={'mean': 'League_Cost_Mean', 'median': 'League_Cost_Median', 'max': 'League_Cost_Max'})

        df_m = df_m.merge(season_sale_stats, on='Season', how='left')
        df_m = df_m.merge(team_sale_stats, on='Team', how='left')
        df_m = df_m.merge(league_sale_stats, on='League', how='left')
        df_m = df_m.merge(season_cost_stats, on='Season', how='left')
        df_m = df_m.merge(team_cost_stats, on='Team', how='left')
        df_m = df_m.merge(league_cost_stats, on='League', how='left')     

        market_cols = [
            'Season_Sale_Mean', 'Season_Sale_Median', 'Season_Sale_Max',
            'Team_Sale_Mean', 'Team_Sale_Median', 'Team_Sale_Max',
            'League_Sale_Mean', 'League_Sale_Median', 'League_Sale_Max',
            'Season_Cost_Mean', 'Season_Cost_Median', 'Season_Cost_Max',  
            'Team_Cost_Mean', 'Team_Cost_Median', 'Team_Cost_Max',        
            'League_Cost_Mean', 'League_Cost_Median', 'League_Cost_Max']

        df_m[market_cols] = df_m[market_cols].fillna(0)
        df_m['Cost'] = df_m['Cost'].fillna(0)
        df_m['Value_Prev_Year'] = df_m.groupby('Player')['Sale'].shift(1).fillna(0)
        df_m['Value_Next_Year'] = df_m.groupby('Player')['Sale'].shift(-1).fillna(0)
        df_m['Prev_Team'] = df_m.groupby('Player')['Team'].shift(1)
        df_m['Next_Team'] = df_m.groupby('Player')['Team'].shift(-1)

        df_m['Value_Prev_Year_Same_Team'] = np.where(
            (df_m['Team'] == df_m['Prev_Team']) & (df_m['Value_Prev_Year'] > 0),
            df_m['Value_Prev_Year'], 0)

        df_m['Value_Next_Year_Same_Team'] = np.where(
            (df_m['Team'] == df_m['Next_Team']) & (df_m['Value_Next_Year'] > 0),
            df_m['Value_Next_Year'], 0)

        squad_stats_prev = df_m.groupby(['Team', 'Season'])['Value_Prev_Year'].agg(['sum', 'mean']).reset_index()
        squad_stats_prev = squad_stats_prev.rename(columns={'sum': 'Total_Squad_Value_Prev', 'mean': 'Avg_Player_Value_Prev'})     
        squad_stats_next = df_m.groupby(['Team', 'Season'])['Value_Next_Year'].agg(['sum', 'mean']).reset_index()
        squad_stats_next = squad_stats_next.rename(columns={'sum': 'Total_Squad_Value_Next', 'mean': 'Avg_Player_Value_Next'})

        df_m = df_m.merge(squad_stats_prev, on=['Team', 'Season'], how='left')
        df_m['Total_Squad_Value_Prev'] = df_m['Total_Squad_Value_Prev'].fillna(0)
        df_m['Avg_Player_Value_Prev'] = df_m['Avg_Player_Value_Prev'].fillna(0)
        df_m['Player_Value_Share_Prev'] = np.where(
            df_m['Total_Squad_Value_Prev'] > 0, df_m['Value_Prev_Year'] / df_m['Total_Squad_Value_Prev'], 0)

        df_m['Player_To_Avg_Ratio_Prev'] = np.where(
            df_m['Avg_Player_Value_Prev'] > 0, df_m['Value_Prev_Year'] / df_m['Avg_Player_Value_Prev'], 0)
        
        df_m = df_m.merge(squad_stats_next, on=['Team', 'Season'], how='left')
        df_m['Total_Squad_Value_Next'] = df_m['Total_Squad_Value_Next'].fillna(0)
        df_m['Avg_Player_Value_Next'] = df_m['Avg_Player_Value_Next'].fillna(0)

        df_m['Player_Value_Share_Next'] = np.where(
            df_m['Total_Squad_Value_Next'] > 0, df_m['Value_Next_Year'] / df_m['Total_Squad_Value_Next'], 0)

        df_m['Player_To_Avg_Ratio_Next'] = np.where(
            df_m['Avg_Player_Value_Next'] > 0, df_m['Value_Next_Year'] / df_m['Avg_Player_Value_Next'], 0)
        
        df_m['League_Jump'] = (df_m.groupby('Player')['League_Level'].shift(1) - df_m['League_Level']).fillna(0)

        return df_m

    @st.cache_resource
    def train_valuation_model(_data):
        train_df = _data.dropna(subset=['Sale']).copy()

        if len(train_df) < 5: return None, None, {}
        cat_features = ['Season', 'League', 'Team', 'Position', 'Grade']
        encoders = {}

        for col in cat_features:
            le = LabelEncoder()
            le.fit(_data[col].astype(str).unique().tolist() + ['Unknown'])
            train_df[f'{col}_ID'] = le.transform(train_df[col].astype(str))
            encoders[col] = le

        features = [
            'Age', 'Goal-Scoring','Assist-Creation', 'Attack', 'Dribbling', 'Possession', 'Defense', 'Physical',
            #'Goalkeeping',
            'League_Level',
            'Team_Record_Sale','Position_Record_Sale',
            'Value_Prev_Year_Same_Team', 'Value_Next_Year_Same_Team',
            'Player_Value_Share_Prev','Player_To_Avg_Ratio_Prev',
            'Player_Value_Share_Next','Player_To_Avg_Ratio_Next',
            'Cost',
            'Season_Sale_Mean', 'Season_Sale_Median', 'Season_Sale_Max',
            'Team_Sale_Mean', 'Team_Sale_Median', 'Team_Sale_Max',      
            'League_Sale_Mean', 'League_Sale_Median', 'League_Sale_Max',
            'Season_Cost_Mean', 'Season_Cost_Median', 'Season_Cost_Max',  
            'Team_Cost_Mean', 'Team_Cost_Median', 'Team_Cost_Max',        
            'League_Cost_Mean', 'League_Cost_Median', 'League_Cost_Max',    
            'Season_ID', 'League_ID', 'Team_ID', 'Position_ID', 'Grade_ID']

        y = np.log1p(train_df['Sale'])

        X = train_df[features]

        model = RandomForestRegressor(n_estimators=800, max_depth=12,min_samples_leaf=6, random_state=42)
        #model = RandomForestRegressor(n_estimators=400,max_depth=12,max_features=0.3,min_samples_leaf=3,n_jobs=-1,random_state=42)
        #model = LGBMRegressor(n_estimators=500,learning_rate=0.03,max_depth=8,random_state=42)

        model.fit(X, y)

        return model, features, encoders

    if "df" in locals():

        df_enriched = prepare_market_data(df)
        model_v, feat_cols, encoders = train_valuation_model(df_enriched)
        st.header("🏢 Squad Analysis and Market Values")

        col1, col2, col3 = st.columns(3)

        with col1:
            Season_list = sorted(df_enriched['Season'].unique(), reverse=True)
            Season_filter = st.selectbox("Season:", Season_list)
            df_enriched1 = df_enriched[df_enriched['Season'] == Season_filter]

        with col2:
            ordered_leagues_df = df_enriched1[['League', 'League_Level']].drop_duplicates().sort_values('League_Level')
            ordered_leagues_list = ordered_leagues_df['League'].tolist()
            League_filter = st.selectbox("League:", ordered_leagues_list)
            df_enriched2 = df_enriched1[df_enriched1['League'] == League_filter]

        with col3:
            Team_filter = st.selectbox("Team:", sorted(df_enriched2['Team'].unique()))
            df_enriched3 = df_enriched2[df_enriched2['Team'] == Team_filter]

        if Team_filter and Season_filter:
            team_season_df = df_enriched3[(df_enriched3['Team'] == Team_filter) &
                                        (df_enriched3['Season'] == Season_filter)].copy()
        
            if not team_season_df.empty and model_v:
                results = []

                for _, row in team_season_df.iterrows():
                    try:
                        input_row = []

                        for col in feat_cols:
                            orig_col = col.replace('_ID', '')

                            if orig_col in encoders:
                                val = str(row[orig_col])

                                try:
                                    encoded_val = encoders[orig_col].transform([val])[0]

                                except:
                                    encoded_val = encoders[orig_col].transform(['Unknown'])[0]
                                input_row.append(encoded_val)

                            else:

                                input_row.append(row[col])

                        pred_log = model_v.predict(np.array(input_row).reshape(1, -1))[0]
                        market_value_raw = np.expm1(pred_log)
                        market_value = float(max(0, round(market_value_raw / 1000) * 1000))

                        results.append({
                            "Player": row['Player'],
                            "Position": row['Position'],
                            "Age": int(row['Age']),
                            "Grade": row['Grade'],
                            "Re-Sale Value": market_value})

                    except Exception as e:          

                        st.error(f"Error predicting {row['Player']}: {e}")

                        continue

                if results:

                    res_df = pd.DataFrame(results)
                    res_df = res_df.sort_values(by="Re-Sale Value", ascending=False).reset_index(drop=True)
                    res_df["Rank"] = res_df["Re-Sale Value"].rank(method="min", ascending=False).astype(int)

                    st.subheader(f"Squad Analysis: {Team_filter} | {Season_filter}")

                    total_value = res_df["Re-Sale Value"].sum()

                    st.metric("Total Team Value", f"€ {total_value:,.0f}".replace(",", "."))
                    res_df["Re-Sale Value"] = res_df["Re-Sale Value"].apply(lambda x: f"€ {int(x):,}".replace(",", "."))
                    table_cols = ["Rank", "Player", "Position", "Age", "Grade", "Re-Sale Value"]

                    st.dataframe(res_df[table_cols], use_container_width=True, hide_index=True)
                else:
                    st.warning("It was not possible to calculate values for this team.")
    else:
        st.error("Error: DataFrame is not defined.") 

elif page == "Ternary Graph":
        st.write("""---""")
        st.title("18 - Ternary Graph")
        st.info(
            "Liga Portugal  -  Liga Portugal 2  -  Liga 3  -  Campeonato de Portugal  -  Liga Revelação U23", icon="ℹ️")

        df = df[df.Position != "GK"]

        col1, col2, col3 = st.columns(3)
        with col1:
            selected_season = st.selectbox("Season:", sorted(df['Season'].unique(), reverse=True), key="ternary_season")
        with col2:
            selected_league = st.selectbox("League:", df['League'].unique(), key="ternary_league")
        with col3:
            selected_position = st.selectbox("Position:", df['Position'].unique(), key="ternary_position")
            
        df_filtered = df[(df['Season'] == selected_season) & 
                         (df['League'] == selected_league) & 
                         (df['Position'] == selected_position)]
        
        def normalize_metric(metric_series):
            max_val = metric_series.max()
            min_val = metric_series.min()
            if max_val == min_val:
                return metric_series * 0 
            return ((metric_series - min_val) / (max_val - min_val)) * 100

        df_filtered["Goal-Scoring"] = normalize_metric(df_filtered["Goal-Scoring"])
        df_filtered["Attack"] = normalize_metric(df_filtered["Attack"])
        df_filtered["Defense"] = normalize_metric(df_filtered["Defense"])
        df_filtered["Possession"] = normalize_metric(df_filtered["Possession"])

        st.divider()
        st.subheader("📋 Custom Tactical Map")

        available_metrics = ["Goal-Scoring", "Assist-Creation", "Attack", "Dribbling", "Possession", "Defense", "Physical"]
        
        selected_metrics = st.multiselect(
            "Choose exactly 3 metrics for the Ternary Graph:",
            options=available_metrics,
            default=["Attack", "Possession", "Defense"],
            max_selections=3
        )

        if len(selected_metrics) == 3:
            
            plot_df = df_filtered.copy()
            plot_df = plot_df.dropna(subset=selected_metrics + ['Player'])
            plot_df = plot_df[(plot_df[selected_metrics[0]] > 0) | 
                              (plot_df[selected_metrics[1]] > 0) | 
                              (plot_df[selected_metrics[2]] > 0)]

            if not plot_df.empty:
                import plotly.express as px
                
                fig = px.scatter_ternary(
                    plot_df,
                    a=selected_metrics[0],
                    b=selected_metrics[1],
                    c=selected_metrics[2],
                    color="Team",
                    hover_name="Player",
                    hover_data=["Team", "Age"], 
                    title=f"{selected_league} ({selected_season}) - {selected_position}",
                    template="plotly_white"
                )
                
                fig.update_traces(
                    marker=dict(size=10, line=dict(width=0.5, color='DarkSlateGrey')),
                    selector=dict(mode='markers'),
                    cliponaxis=False
                )
                
                fig.update_layout(
                        height=700,
                        margin=dict(l=40, r=40, t=60, b=40), 
                        showlegend=True,
                        ternary=dict(
                            sum=None,
                            aaxis=dict(title_font=dict(size=14), tickfont=dict(size=10), layer="below traces"),
                            baxis=dict(title_font=dict(size=14), tickfont=dict(size=10), layer="below traces"),
                            caxis=dict(title_font=dict(size=14), tickfont=dict(size=10), layer="below traces")
                        )
                    )
                    
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data available to plot these specific metrics for the selected filters.")
        else:
            st.warning("Please select exactly 3 metrics from the dropdown above to generate the chart.")

elif page == "Team Global Analysis":
        st.write("""---""")
        st.title("19 - Team Global Analysis")
        st.info("This section aggregates individual player metrics to map out team-wide tactical identities and styles.")

        df_clean = df.dropna(subset=['Team', 'Position']).copy()

        outfield_metrics = ["Goal-Scoring", "Assist-Creation", "Attack", "Dribbling", "Possession", "Defense", "Physical"]
        gk_metric = "Goalkeeping"

        if not df_clean.empty:

            df_clean['Player_Rating'] = 0.0
            
            outfield_mask = df_clean['Position'] != 'GK'
            df_clean.loc[outfield_mask, 'Player_Rating'] = df_clean.loc[outfield_mask, outfield_metrics].mean(axis=1)
            
            gk_mask = df_clean['Position'] == 'GK'
            df_clean.loc[gk_mask, 'Player_Rating'] = df_clean.loc[gk_mask, gk_metric]
            
            df_clean = df_clean.dropna(subset=['Player_Rating'])

            outfield_df = df_clean[df_clean['Position'] != 'GK']
            team_profiles = outfield_df.groupby(['Season', 'League', 'Team'])[outfield_metrics].mean().reset_index()
            
            team_profiles['Attacking_Pillar'] = team_profiles[['Goal-Scoring', 'Assist-Creation', 'Attack']].mean(axis=1)
            team_profiles['Control_Pillar'] = team_profiles[['Dribbling', 'Possession']].mean(axis=1)
            team_profiles['Defensive_Pillar'] = team_profiles[['Defense', 'Physical']].mean(axis=1)
            
            median_control_map = team_profiles.groupby(['Season', 'League'])['Control_Pillar'].median().to_dict()
            
            #def classify_tactical_archetype(row):
                #pillars = {
                    #'Attacking Powerhouse': row['Attacking_Pillar'],
                    #'Possession & Control Engine': row['Control_Pillar'],
                    #Defensive Rock / Resilient Block': row['Defensive_Pillar']
                #}
                #dominant_style = max(pillars, key=pillars.get)
                #current_median = median_control_map.get((row['Season'], row['League']), team_profiles['Control_Pillar'].median())
                
                #if dominant_style == 'Possession & Control Engine' and row['Attacking_Pillar'] > row['Defensive_Pillar']:
                    #return 'Fluid Attacking Control'
                #elif dominant_style == 'Defensive Rock / Resilient Block' and row['Control_Pillar'] < current_median:
                    #return 'Direct Counter-Attacking / Low-Block'
                #return dominant_style

            #team_profiles['Archetype'] = team_profiles.apply(classify_tactical_archetype, axis=1)

            position_strength_df = df_clean.groupby(['Season', 'League', 'Team', 'Position'])['Player_Rating'].mean().unstack(fill_value=0).reset_index()
            available_positions = sorted(df_clean['Position'].unique().tolist())

            enable_compare = st.checkbox("Compare with another team/season?", value=False)

            c_sel1, c_sel2 = st.columns(2)
            with c_sel1:
                st.markdown("### 1. Main Team Target")
                s1 = st.selectbox("Season:", sorted(df_clean['Season'].unique(), reverse=True), key="team_season_1")
                l1_opts = sorted(df_clean[df_clean['Season'] == s1]['League'].unique())
                l1 = st.selectbox("League:", l1_opts, key="team_league_1")
                t1_opts = sorted(team_profiles[(team_profiles['Season'] == s1) & (team_profiles['League'] == l1)]['Team'].unique())
                selected_team = st.selectbox("Select Main Team:", t1_opts, key="team_main")
                
            with c_sel2:
                st.markdown("### 2. Comparison Target")
                if enable_compare:
                    s2 = st.selectbox("Season:", sorted(df_clean['Season'].unique(), reverse=True), key="team_season_2")
                    l2_opts = sorted(df_clean[df_clean['Season'] == s2]['League'].unique())
                    l2 = st.selectbox("League:", l2_opts, key="team_league_2")
                    t2_opts = sorted(team_profiles[(team_profiles['Season'] == s2) & (team_profiles['League'] == l2)]['Team'].unique())
                    compare_team = st.selectbox("Select Team to Compare:", t2_opts, key="team_compare")
                else:
                    s2, l2, compare_team = None, None, None

            st.divider()

            def display_team_cards(team_name, season, league):
                meta_filter = (team_profiles['Team'] == team_name) & (team_profiles['Season'] == season) & (team_profiles['League'] == league)
                team_meta = team_profiles[meta_filter].iloc[0]
                squad_size = len(df_clean[(df_clean['Team'] == team_name) & (df_clean['Season'] == season) & (df_clean['League'] == league)])
                
                pos_filter = (position_strength_df['Team'] == team_name) & (position_strength_df['Season'] == season) & (position_strength_df['League'] == league)
                team_pos_row = position_strength_df[pos_filter].iloc[0]
                valid_positions = [pos for pos in available_positions if pos in team_pos_row.index]
                ranked_positions = team_pos_row[valid_positions].sort_values(ascending=False)
                
                ranking_html = ""
                for i, (pos, score) in enumerate(ranked_positions.items()):
                    ranking_html += f"{i+1}. **{pos}** ({score:.2f})<br>"
                
                st.markdown(f"#### {team_name} <span style='font-size:0.75em; color:gray;'>({season})</span>", unsafe_allow_html=True)
                #mc1, mc2, mc3 = st.columns(3)
                mc1, mc3 = st.columns(2)
                mc1.metric("Squad Size", squad_size)
                #mc2.markdown(f"**Archetype:**<br>`{team_meta['Archetype']}`", unsafe_allow_html=True)
                mc3.markdown(f"**Positional Ranking:**<br><span style='font-size:0.9em;'>{ranking_html}</span>", unsafe_allow_html=True)

            st.write("")
            if compare_team:
                t1_col, t2_col = st.columns(2)
                with t1_col: display_team_cards(selected_team, s1, l1)
                with t2_col: display_team_cards(compare_team, s2, l2)
            else:
                display_team_cards(selected_team, s1, l1)
            
            league_pos_avg = df_clean[(df_clean['Season'] == s1) & (df_clean['League'] == l1)].groupby('Position').mean(numeric_only=True)
            radar_categories = []
            league_vals = []
            cat_positions = [] 
            
            for pos in available_positions:
                pos_metrics = [gk_metric] if pos == 'GK' else outfield_metrics
                for m in pos_metrics:
                    radar_categories.append(f"<b>{pos}</b><br>{m}")
                    cat_positions.append(pos)
                    if pos in league_pos_avg.index and m in league_pos_avg.columns and not pd.isna(league_pos_avg.loc[pos, m]):
                        league_vals.append(league_pos_avg.loc[pos, m])
                    else:
                        league_vals.append(0)

            def get_team_radar_vals(team_name, season, league):
                t_df = df_clean[(df_clean['Team'] == team_name) & (df_clean['Season'] == season) & (df_clean['League'] == league)]
                t_pos_avg = t_df.groupby('Position').mean(numeric_only=True)
                t_vals = []
                for pos in available_positions:
                    p_metrics = [gk_metric] if pos == 'GK' else outfield_metrics
                    for m in p_metrics:
                        if pos in t_pos_avg.index and m in t_pos_avg.columns and not pd.isna(t_pos_avg.loc[pos, m]):
                            t_vals.append(t_pos_avg.loc[pos, m])
                        else:
                            t_vals.append(0)
                return t_vals

            team1_vals = get_team_radar_vals(selected_team, s1, l1)
            team2_vals = get_team_radar_vals(compare_team, s2, l2) if compare_team else []
            
            if compare_team and team1_vals and team2_vals:
                v1 = np.array(team1_vals)
                v2 = np.array(team2_vals)
                
                v1_centered = v1 - np.mean(v1)
                v2_centered = v2 - np.mean(v2)
                
                denom = (np.linalg.norm(v1_centered) * np.linalg.norm(v2_centered))
                if denom > 0:
                    r_val = np.dot(v1_centered, v2_centered) / denom
                    similarity_score = (r_val + 1) / 2 * 100
                else:
                    similarity_score = 100.0 if np.array_equal(v1, v2) else 0.0
                
                st.write("")
                col_metric, _ = st.columns([1, 2])
                with col_metric:
                    st.metric(
                        label="Squad Playstyle Similarity Score", 
                        value=f"{similarity_score:.2f}%",
                        help="Calculated using a normalized profile correlation."
                    )
            
            if radar_categories:
                radar_categories.append(radar_categories[0])
                league_vals.append(league_vals[0])
                cat_positions.append(cat_positions[0])
                if team1_vals: team1_vals.append(team1_vals[0])
                if team2_vals: team2_vals.append(team2_vals[0])

            fig = go.Figure()
            
            all_plotted_vals = league_vals + team1_vals + team2_vals
            max_val = max(all_plotted_vals) if all_plotted_vals else 100
            bg_radius = max_val + 5
            
            bg_colors = [
                'rgba(31, 119, 180, 0.07)', 'rgba(214, 39, 40, 0.06)', 'rgba(148, 103, 189, 0.07)', 
                'rgba(230, 171, 2, 0.06)', 'rgba(227, 119, 194, 0.07)', 'rgba(23, 190, 207, 0.07)', 'rgba(44, 160, 44, 0.06)'
            ]
            
            for i, pos in enumerate(available_positions):
                color = bg_colors[i % len(bg_colors)]
                r_bg = [bg_radius if cp == pos else 0 for cp in cat_positions]
                fig.add_trace(go.Scatterpolar(r=r_bg, theta=radar_categories, fill='toself', fillcolor=color, line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'))
            
            fig.add_trace(go.Scatterpolar(r=team1_vals, theta=radar_categories, fill='toself', name=f"{selected_team} ({s1})", line_color='#2ca02c', fillcolor='rgba(44, 160, 44, 0.25)'))
            
            if compare_team:
                fig.add_trace(go.Scatterpolar(r=team2_vals, theta=radar_categories, fill='toself', name=f"{compare_team} ({s2})", line_color='#ff7f0e', fillcolor='rgba(255, 127, 14, 0.25)'))
            
            fig.add_trace(go.Scatterpolar(r=league_vals, theta=radar_categories, fill='toself', name=f"Baseline: {l1} Avg ({s1})", line_color='#7f7f7f', fillcolor='rgba(127, 127, 127, 0.03)', line=dict(dash='dash')))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, bg_radius])),
                height=850,
                margin=dict(l=90, r=90, t=60, b=60),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            
            st.write("### 📋 Squad Positional Fingerprint")
            st.caption("Hover over the chart and click the **📸 Camera Icon** in the top right to download a high-res PNG.")
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': True,
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f"{selected_team}_vs_{compare_team}_Fingerprint" if compare_team else f"{selected_team}_Fingerprint",
                        'height': 1000,
                        'width': 1000,
                        'scale': 2
                    }
                }
            )
            
            st.write("### 📋 Top Contributing Players")
            display_columns = ['Player', 'Position', 'Age', 'Player_Rating', gk_metric] + outfield_metrics
            
            def get_roster_df(team_name, season, league):
                mask = (df_clean['Team'] == team_name) & (df_clean['Season'] == season) & (df_clean['League'] == league)
                r_df = df_clean[mask][display_columns].copy()
                
                metric_cols = ['Player_Rating', gk_metric] + outfield_metrics
                for col in metric_cols:
                    r_df[col] = pd.to_numeric(r_df[col], errors='coerce')
                
                r_df = r_df.sort_values(by="Player_Rating", ascending=False)
                
                format_rules = {col: "{:.2f}" for col in metric_cols}
                if 'Age' in r_df.columns:
                    r_df['Age'] = pd.to_numeric(r_df['Age'], errors='coerce')
                    format_rules['Age'] = "{:.0f}"
                
                styled_df = r_df.style.format(
                    formatter=format_rules,
                    na_rep="-"
                ).set_properties(
                    subset=['Player_Rating'],
                    **{
                        'background-color': '#e6f2ff',  
                        'color': '#003366',             #Column color
                        'font-weight': 'bold'
                    }
                )
                return styled_df
            
            if compare_team:
                tab1, tab2 = st.tabs([f"{selected_team} ({s1})", f"{compare_team} ({s2})"])
                with tab1: 
                    st.dataframe(get_roster_df(selected_team, s1, l1), hide_index=True, use_container_width=True)
                with tab2: 
                    st.dataframe(get_roster_df(compare_team, s2, l2), hide_index=True, use_container_width=True)
            else:
                st.dataframe(get_roster_df(selected_team, s1, l1), hide_index=True, use_container_width=True)

        else:
            st.warning("No player metrics available to construct profiles with the underlying dataset context.")

        def calculate_similarity(v1, v2):
                v1_arr = np.array(v1)
                v2_arr = np.array(v2)
                v1_centered = v1_arr - np.mean(v1_arr)
                v2_centered = v2_arr - np.mean(v2_arr)
                
                denom = (np.linalg.norm(v1_centered) * np.linalg.norm(v2_centered))
                if denom > 0:
                    r_val = np.dot(v1_centered, v2_centered) / denom
                    return (r_val + 1) / 2 * 100
                else:
                    return 100.0 if np.array_equal(v1_arr, v2_arr) else 0.0

        if compare_team and team1_vals and team2_vals:
                similarity_score = calculate_similarity(team1_vals, team2_vals)
                
                st.write("")
                col_metric, _ = st.columns([1, 2])
                with col_metric:
                    st.metric(
                        label="Squad Playstyle Similarity Score", 
                        value=f"{similarity_score:.2f}%",
                        help="Calculated using a normalized profile correlation."
                    )
                    
        st.divider()
        st.write("### 🔍 Top 10 Most Similar Playstyles")
        st.caption(f"Finding squads historically most similar to **{selected_team} ({s1})**.")
        st.info("Leave these filters empty to search across your entire database.")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
                available_pool_seasons = sorted(team_profiles['Season'].unique(), reverse=True)
                filter_seasons = st.multiselect("Limit search to specific Season(s):", available_pool_seasons)
        with f_col2:
                available_pool_leagues = sorted(team_profiles['League'].unique())
                filter_leagues = st.multiselect("Limit search to specific League(s):", available_pool_leagues)

        base_team1_vals = team1_vals[:-1] if len(team1_vals) > len(available_positions) else team1_vals
            
        if base_team1_vals:
                similarity_results = []
                
                pool_combinations = team_profiles[['Season', 'League', 'Team']].drop_duplicates()
                
                if filter_seasons:
                    pool_combinations = pool_combinations[pool_combinations['Season'].isin(filter_seasons)]
                if filter_leagues:
                    pool_combinations = pool_combinations[pool_combinations['League'].isin(filter_leagues)]
                
                for _, row in pool_combinations.iterrows():
                    t_season = row['Season']
                    t_league = row['League']
                    t_name = row['Team']
                    
                    if t_name == selected_team and t_season == s1 and t_league == l1:
                        continue
                        
                    t_vals = get_team_radar_vals(t_name, t_season, t_league)
                    
                    if len(t_vals) == len(base_team1_vals) and len(t_vals) > 0:
                        sim_score = calculate_similarity(base_team1_vals, t_vals)
                        similarity_results.append({
                            "Team": t_name,
                            "Season": t_season,
                            "League": t_league,
                            "Similarity (%)": sim_score
                        })
                
                if similarity_results:
                    sim_df = pd.DataFrame(similarity_results)
                    sim_df = sim_df.sort_values(by="Similarity (%)", ascending=False).head(10)
                    
                    sim_df.index = np.arange(1, len(sim_df) + 1) 
                    st.dataframe(
                        sim_df.style.format({"Similarity (%)": "{:.2f}%"}).background_gradient(cmap='Greens', subset=['Similarity (%)']),
                        use_container_width=True
                    )
                else:
                    st.warning("No teams found matching those specific filter criteria to compare against.")       