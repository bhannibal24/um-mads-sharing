#!/usr/bin/env python
# coding: utf-8

# # Assignment 3

# name: Ben Hannibal
# email: bhann@umich.edu
# github repo link: https://github.com/bhannibal24/um-mads-sharing/tree/main

# # Basketball Shot Data Exploration
# 
# After playing basketball from childhood through college, my career in sports and my interest in deeping my professional connection to basketball I figured it would be good to explore some shot data from the 2015-2020 NBA seasons. We'll be visualizing trends of shot type distributions, efficiency by distance, shot locations and yearly shifts in efficiency by team and player. The purpose of this exploration is to identify emerging trends and interact with the data through filters. We'll use scatter plots to track shot locations, stacked bar to view type distributions, histograms to view efficiency by distance

# ## Scatter Plot Visualization Technique
# 
# Scatter plots are primarily used to show relationships between two variables (numeric). The points on a scatter plot can aid one in determining trends within the data.
# The points on scatter plots can be adjusted to change shape, color, and size depending on what it is you want to visualize. 
# 
# In this notebook, we'll use scatter plots to chart shot locations based on their X and Y components on a basketball court. The final scatter plot will also be interactive to allow for other
# explorations into how shot location changes based on shot type, player, make or miss, and game situation.
# 
# ___
# 
# ## Considerations for Library Selection
# We'll use Plotly for our exploration as interactivity is native out of the box, it has a seamless integration with Streamlit for displaying our dashboard and it's efficient in spatial rendering.
# 
# Streamlit is a light weight way to turn data scripts into ewb apps without having to write a bunch of web script, the layout utilities are easy to use and it can be deployed from our github repository to a live URL quickly.

# ## Installing the Libraries
# 
# run the following command
# 
# %pip install streamlit plotly pandas

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from pathlib import Path


# ## Step 1: Page Configuration
# 
# Set up the dashboard page and configurations in streamlit

# In[2]:


st.set_page_config(page_title = "NBA Shot Analytics", layout='wide',initial_sidebar_state="expanded")
st.title("NBA Shot Analysis Dashboard (2015-2020)")
st.markdown("An interactive look into shooting patterns and player efficiency")


# ## Step 2: Load Data
# 
# Cache your data for streamlit. In streamlit, any time a user interacts with a widget the whole script is rerun from top to bottom. By cacheing the data, we can speed up user interface

# In[5]:


@st.cache_data

def load_data():
    current_dir = Path.cwd()
    if current_dir.name == 'notebooks':
        project_root = current_dir.parent
    else:
        project_root = current_dir
    data_path = project_root / 'data' / 'nba_shots_optimized.csv'
    df = pd.read_csv(data_path)
    df = df.dropna(subset=['player.player_name', 'Season', 'player.team_name'])
    df['Season'] = df['Season'].astype(str).str.extract(r'(\d{4})')
    df['Season'] = df['Season'].astype(int)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("couldn't find nba_shots_optimized.csv. Is your data or path in the right spot?")
    st.stop()


# In[6]:


df.head()


# ## Setting Up the Sidebar Widgets
# 
# We're using Streamlit's st.sidebar to shove all our filters over to the left side of the screen. This keeps the main area clean and dedicated entirely to our shot charts.
# 
# The Player Dropdown:
# st.sidebar.selectbox grabs every unique name from player.player_name, sorts them A-to-Z, and drops them into a searchable dropdown. Whichever name the user clicks gets saved to selected_player.
# 
# The Team Dropdown:
# st.sidebar.selectbox grabs every unique name from player.team_name, sorts them A-to-Z, and drops them into a searchable dropdown. Whichever team the user clicks gets saved to selected_team.
# 
# The Season Slider:
# st.sidebar.slider looks at the minimum and maximum years in our Season column. By passing a tuple of both (min_season, max_season) as the starting point, Streamlit automatically turns it into a range slider with two draggable handles.
# 
# The Shot Action Selector:
# st.sidebar.multiselect gets a list of specific play types (like a Step Back Jump Shot or Running Dunk). We drop any empty values with .dropna() so the UI stays clean. This starts empty, meaning the user can select as many specific play types as they want—or none at all.
# 
# The Clutch Toggle:
# A simple st.sidebar.checkbox that returns True or False. We also added a help hover-tooltip to explain exactly what "Clutch" means in our app.
# 
# 

# In[7]:


st.sidebar.header("Dashboard Filters")



# Filter: Team Selector
all_teams = sorted(df['player.team_name'].unique().tolist())
selected_team = st.sidebar.multiselect("Select a Team", options=all_teams, default=[],help='Leave blank to include all teams.')

if selected_team:
    available_players_df = df[df['player.team_name'].isin(selected_team)]
else:
    available_players_df = df

# Filter: Player Selector
all_players = sorted(available_players_df['player.player_name'].unique())

selected_players = st.sidebar.multiselect(
    "Select Player(s)", 
    options=all_players, 
    default=[],
    help="Select one or multiple players. Leave empty to show all players."
)
# Filter: Season Range Slider
clean_seasons = df['Season'].dropna()
min_season = int(clean_seasons.min())
max_season = int(clean_seasons.max())
selected_seasons = st.sidebar.slider(
    "Select Season Range", 
    min_season, 
    max_season, 
    (min_season, max_season)
)

# Filter: Action Type
all_actions = sorted(df['player.action_type'].dropna().unique())
selected_actions = st.sidebar.multiselect(
    "Filter by Shot Action (Optional)", 
    all_actions, 
    default=[]
)

# Filter: Clutch Toggle
clutch_only = st.sidebar.checkbox(
    "Clutch Situations Only", 
    value=False,
    help="Filters for shots taken in the 4th Quarter or Overtime with 5 or fewer minutes remaining."
)


# In[8]:


filtered_df = df[
    (df['Season'].between(selected_seasons[0], selected_seasons[1])) &
    (df['player.shot_distance'] <=45) &
    (df['player.loc_y'] < 300)
].copy()

filtered_df['x_scaled'] = filtered_df['player.loc_x']*10
filtered_df['y_scaled'] = filtered_df['player.loc_y'] * 10
filtered_df['plot_y'] = (51.05 - filtered_df['player.loc_y']) * 10

filtered_df['plot_y'] = 500 - (filtered_df['y_scaled'] + 50)

if selected_players:
    filtered_df = filtered_df[filtered_df['player.player_name'].isin(selected_players)]

if 'selected_teams' in locals() and selected_teams:
    filtered_df = filtered_df[filtered_df['player.team_name'].isin(selected_teams)]
if selected_actions:
    filtered_df = filtered_df[filtered_df['player.action_type'].isin(selected_actions)]

if clutch_only:
    filtered_df = filtered_df[
        (filtered_df['player.period'] >= 4) & 
        (filtered_df['player.minutes_remaining'] <= 5)
    ]


# In[9]:


total_shots = len(filtered_df)
if total_shots >0:
    made_shots = filtered_df['player.shot_made_numeric'].sum()
    fg_pct = (made_shots / total_shots) * 100
else:
    fg_pct = 0.0

#Header
players_label = ", ".join(selected_players) if selected_players else "No Players Selected"
st.markdown(f"### Current View: **{players_label}** | Total Shots: `{total_shots}` | FG%: `{fg_pct:.1f}%`")


# In[10]:


row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)


# Above we set up our dashboard grid. By default, streamlit piles everything into one long column. st.columns() lets you break that into multiple columns. 
# 
# by using st.columns(2) we tell streamlit to split the horizontal width of the page into two equal side by side columns. to put stuff in the columns we can use the with statement

# # Shot Locations
# 
# We used Plotly's px.scatter functionality to map individual shot attempts, utilizing x_scaled and y_scaled coordinates to plot each shot with high precision. To provide spatial context, we overlay this data on a custom half-court background image using fig_map.add_layout_image.
# 
# Technical Challenge: Coordinate Geometry & Alignment
# During development, we encountered a significant challenge: aligning the scatter data with the background image geometry. By default, Plotly handles image coordinate mapping based on a standard Cartesian plane. Initially, our shot data points and the court image were misaligned—the background image appeared inverted or scaled incorrectly relative to our x and y axes.
# 
# To resolve this, we explored two potential approaches:
# 
# Coordinate Transformation: Adjusting the sizex, sizey, x, and y parameters within the add_layout_image dictionary to flip the image orientation programmatically. While powerful, this requires precise calibration of the x and y anchor points to prevent the image from being pushed out of the plot frame.
# 
# Pre-processing (The Solution): To ensure consistent alignment and simplify our code, we performed a 180-degree rotation on the source image file itself. This allowed us to map the image using a standard, positive-value Cartesian coordinate system (x=-250, y=-50), ensuring the court geometry maps seamlessly to our shot data without needing complex scaling hacks.
# 
# Finally, we implemented interactivity by toggling the color parameter, allowing users to dynamically switch between viewing shot data by individual player or by team, enabling a quick comparison of both shot volume and efficiency across different cohorts.
# 
# 

# In[11]:


current_dir = Path.cwd()
if current_dir.name == 'notebooks':
    project_root = current_dir.parent
else:
    project_root = current_dir
datapath = project_root / 'data' / "court image.png"


with row1_col1:
    st.markdown("#### Shot Charts")
    if not filtered_df.empty:
        color_column = 'player.team_name' if len(selected_team) > 1 else 'player.player_name'
        if len(selected_team) > 1:
            filtered_df = filtered_df[filtered_df['player.team_name'].isin(selected_team)]

        fig_map = px.scatter(
            filtered_df,
            x='x_scaled',
            y='y_scaled',
            symbol = 'player.shot_made_flag',
            symbol_map = {1: 'circle-open', 0: 'x'},
            color=color_column, 
            hover_data=['player.action_type', 'player.shot_distance', 'player.shot_made_flag'],
            opacity=0.8,
            title="Shot Coordinates"
        )

        court_image_path = datapath
        if os.path.exists(court_image_path):
            with open(court_image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode()
            court_data_uri = f"data:image/png;base64,{encoded_string}"

            fig_map.add_layout_image(
                dict(
                    source=court_data_uri,
                    xref="x",
                    yref="y",
                    x=-250,        
                    y=550,         
                    sizex=-500,     
                    sizey=575,     
                    sizing="stretch",
                    opacity=1.0,
                    layer="below"  
                )
            )
        else:
            st.warning("Could not find 'court.png' in your local directory. Please save the image there.")

        fig_map.update_xaxes(range=[-250, 250], showgrid=False, zeroline=False, visible=False)
        fig_map.update_yaxes(range=[-50, 550], scaleanchor='x',scaleratio=1, showgrid=False, zeroline=False, visible=False)

        fig_map.update_layout(
            width=500, 
            height=450, 
            legend_title="Player/Team",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            autosize=False,
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(
                orientation='v',
                yanchor='top',
                xanchor='left',
                itemclick='toggleothers',
                itemsizing='constant',
                x=1.02,
                y=1
            )
        )
        st.plotly_chart(fig_map, width='content')
    else:
        st.info("No shot data available for this player combination.")        


# ## Shot Breakdown
# 
# Here we use a stacked bar to get a visual distribution of the % of 2s and 3s taken over the selected seasons. We use this to determine efficiency of the shots. 

# In[1]:


num_players = filtered_df['player.player_name'].nunique()
num_teams = filtered_df['team_name'].nunique()

if num_players > 1:
    group_col = 'player.player_name'
    bar_mode = 'group'
elif num_teams > 1:
    group_col = 'team_name'
    bar_mode = 'group'
else:
    group_col = 'player.shot_type' 
    bar_mode = 'relative'
with row1_col2:
    st.markdown("#### 2-Pointers vs 3-Pointers")
    if not filtered_df.empty:
        type_by_season = (
            filtered_df.groupby(['Season',group_col, 'player.shot_type'], observed=False)
            .size()
            .reset_index(name='Shot Count')
        )

        fig_bar = px.bar(
            type_by_season,
            x='Season',
            y='Shot Count',
            color=group_col,
            title="Yearly Shot Selection Breakdown",
            barmode=barmode, 
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'player.shot_type': 'Shot Type', 'Shot Count': 'Number of Attempts'}
        )

        fig_bar.update_layout(
            height=400,
            xaxis=dict(tickmode='linear'),
            legend_title="Shot Type"
        )

        st.plotly_chart(fig_bar, width='stretch')
    else:
        st.info("No shot data available.")


# ## Shot Distance Histogram
# 
# We can use a histogram to show the distance ranges teams and players are shooting from. We use this histogram to show the distribution of ranges where players are shooting from

# In[ ]:


with row2_col1:
    st.markdown("#### Shot Frequency by Distance")
    if not filtered_df.empty:

        filtered_df['distance_bin'] = pd.cut(
            filtered_df['player.shot_distance'], 
            bins=[-1, 5, 10, 15, 20, 25, 40], 
            labels=['0-5 ft', '6-10 ft', '11-15 ft', '16-20 ft', '21-25 ft', '26+ ft']
        )

        dist_grouped = (
            filtered_df.groupby(['distance_bin', group_col], observed=False)
            .size()
            .reset_index(name='Attempts')
        )

        fig_dist = px.bar(
            dist_grouped, 
            x='distance_bin', 
            y='Attempts', 
            color=group_col, 
            barmode=bar_mode,
            labels={'distance_bin': 'Shot Distance (Feet)', group_col: 'Group'},
            title="Attempts Volume by Distance Range"
        )
        fig_dist.update_layout(height=400)
        st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.info("No shot data available.")


# ## FG% Trend
# 
# A line chart is the perfect medium to display a yearly trend for how efficient teams and players are.

# In[ ]:


with row2_col2:
    st.markdown("#### Efficiency Trend Across Seasons (2015-2020)")
    if not filtered_df.empty:
        # Group by both Season and the selected entity
        trend_df = (
            filtered_df.groupby(['Season', group_col], observed=False)['player.shot_made_numeric']
            .mean()
            .reset_index()
        )
        trend_df['Field Goal %'] = trend_df['player.shot_made_numeric'] * 100

        fig_trend = px.line(
            trend_df, 
            x='Season', 
            y='Field Goal %', 
            color=group_col,  # Multiple lines for comparison
            markers=True, 
            title="Yearly Shooting Accuracy Trend"
        )
        fig_trend.update_yaxes(range=[0, 100])
        fig_trend.update_layout(height=400, xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No progression data available.")


# ## Deployment Instructions
# Once your code is ready and pushed to GitHub, you can deploy it instantly using Streamlit Community Cloud:
# 
# Sign in: Head to share.streamlit.io and connect your GitHub account.
# 
# Deploy: Click "New app" and select your repository, the main branch, and your script file (e.g., app.py).
# 
# Launch: Streamlit will automatically detect your requirements.txt file, install the necessary dependencies, and provide a live URL for your dashboard.
# 
# my dashboard is at https://nba-shot-charts.streamlit.app/

# In[ ]:




