{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "bc11746c-c1f2-408a-a389-1822078f3731",
   "metadata": {},
   "source": [
    "# Assignment 3"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4ff721c2-2206-4d15-be9a-978ae83fff59",
   "metadata": {},
   "source": [
    "# Basketball Shot Data Exploration\n",
    "\n",
    "After playing basketball from childhood through college, my career in sports and my interest in deeping my professional connection to basketball I figured it would be good to explore some shot data from the 2015-2020 NBA seasons. We'll be visualizing trends of shot type distributions, efficiency by distance, shot locations and yearly shifts in efficiency by team and player. The purpose of this exploration is to identify emerging trends and interact with the data through filters. We'll use scatter plots to track shot locations, stacked bar to view type distributions, histograms to view efficiency by distance"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e65af46d-5e17-442f-807a-204826878aef",
   "metadata": {},
   "source": [
    "## Scatter Plot Visualization Technique\n",
    "\n",
    "Scatter plots are primarily used to show relationships between two variables (numeric). The points on a scatter plot can aid one in determining trends within the data.\n",
    "The points on scatter plots can be adjusted to change shape, color, and size depending on what it is you want to visualize. \n",
    "\n",
    "In this notebook, we'll use scatter plots to chart shot locations based on their X and Y components on a basketball court. The final scatter plot will also be interactive to allow for other\n",
    "explorations into how shot location changes based on shot type, player, make or miss, and game situation.\n",
    "\n",
    "___\n",
    "\n",
    "## Considerations for Library Selection\n",
    "We'll use Plotly for our exploration as interactivity is native out of the box, it has a seamless integration with Streamlit for displaying our dashboard and it's efficient in spatial rendering.\n",
    "\n",
    "Streamlit is a light weight way to turn data scripts into ewb apps without having to write a bunch of web script, the layout utilities are easy to use and it can be deployed from our github repository to a live URL quickly."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "dbbf532f-1700-4585-8633-8531da8805df",
   "metadata": {},
   "source": [
    "## Installing the Libraries\n",
    "\n",
    "run the following command\n",
    "\n",
    "%pip install streamlit plotly pandas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "0ea12f89-b447-49a6-9189-3ea7710487be",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: streamlit in /opt/anaconda3/lib/python3.13/site-packages (1.51.0)\n",
      "Requirement already satisfied: plotly in /opt/anaconda3/lib/python3.13/site-packages (6.3.0)\n",
      "Requirement already satisfied: pandas in /opt/anaconda3/lib/python3.13/site-packages (2.3.3)\n",
      "Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.5.0)\n",
      "Requirement already satisfied: blinker<2,>=1.5.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (1.9.0)\n",
      "Requirement already satisfied: cachetools<7,>=4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.5.1)\n",
      "Requirement already satisfied: click<9,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (8.2.1)\n",
      "Requirement already satisfied: numpy<3,>=1.23 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (2.3.5)\n",
      "Requirement already satisfied: packaging<26,>=20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (25.0)\n",
      "Requirement already satisfied: pillow<13,>=7.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (12.0.0)\n",
      "Requirement already satisfied: protobuf<7,>=3.20 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (5.29.3)\n",
      "Requirement already satisfied: pyarrow<22,>=7.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (21.0.0)\n",
      "Requirement already satisfied: requests<3,>=2.27 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (2.32.5)\n",
      "Requirement already satisfied: tenacity<10,>=8.1.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (9.1.2)\n",
      "Requirement already satisfied: toml<2,>=0.10.1 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.4.0 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (4.15.0)\n",
      "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (3.1.45)\n",
      "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /opt/anaconda3/lib/python3.13/site-packages (from streamlit) (6.5.1)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /opt/anaconda3/lib/python3.13/site-packages (from pandas) (2025.2)\n",
      "Requirement already satisfied: jinja2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.1.6)\n",
      "Requirement already satisfied: jsonschema>=3.0 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (4.25.0)\n",
      "Requirement already satisfied: narwhals>=1.14.2 in /opt/anaconda3/lib/python3.13/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2.7.0)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in /opt/anaconda3/lib/python3.13/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.0)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (3.4.4)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (3.11)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /opt/anaconda3/lib/python3.13/site-packages (from requests<3,>=2.27->streamlit) (2026.6.17)\n",
      "Requirement already satisfied: attrs>=22.2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (25.4.0)\n",
      "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2025.9.1)\n",
      "Requirement already satisfied: referencing>=0.28.4 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.37.0)\n",
      "Requirement already satisfied: rpds-py>=0.7.1 in /opt/anaconda3/lib/python3.13/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.28.0)\n",
      "Requirement already satisfied: six>=1.5 in /opt/anaconda3/lib/python3.13/site-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in /opt/anaconda3/lib/python3.13/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.0.2)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "%pip install streamlit plotly pandas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "02b11b8e-3bb4-4abc-8066-213adf9e1e64",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ef7d6f45-a899-4e18-8b21-78c210198050",
   "metadata": {},
   "source": [
    "## Step 1: Page Configuration\n",
    "\n",
    "Set up the dashboard page and configurations in streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "cbcf8617-a10d-4417-a511-16c722cc3476",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 19:34:56.688 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.689 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.736 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run /opt/anaconda3/lib/python3.13/site-packages/ipykernel_launcher.py [ARGUMENTS]\n",
      "2026-07-15 19:34:56.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:34:56.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.set_page_config(page_title = \"NBA Shot Analytics\", layout='wide',initial_sidebar_state=\"expanded\")\n",
    "st.title(\"NBA Shot Analysis Dashboard (2015-2020)\")\n",
    "st.markdown(\"An interactive look into shooting patterns and player efficiency\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "bb111419-598b-496d-9a94-e3e894e8c217",
   "metadata": {},
   "source": [
    "## Step 2: Load Data\n",
    "\n",
    "Cache your data for streamlit. In streamlit, any time a user interacts with a widget the whole script is rerun from top to bottom. By cacheing the data, we can speed up user interface"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "99d285b8-5948-4227-b2e4-fca6b67ae9ca",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 19:37:40.739 No runtime found, using MemoryCacheStorageManager\n",
      "2026-07-15 19:37:40.741 No runtime found, using MemoryCacheStorageManager\n",
      "2026-07-15 19:37:40.742 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:40.743 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:40.744 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:40.744 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.264 Thread 'Thread-6': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.264 Thread 'Thread-6': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.377 Thread 'Thread-6': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.738 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:37:41.738 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "@st.cache_data\n",
    "def load_data():\n",
    "    df = pd.read_csv('nba_shots_optimized.csv')\n",
    "    df = df.dropna(subset=['player.player_name', 'Season', 'player.team_name'])\n",
    "    df['Season'] = df['Season'].astype(str).str.extract(r'(\\d{4})')\n",
    "    df['Season'] = df['Season'].astype(int)\n",
    "    return df\n",
    "\n",
    "try:\n",
    "    df = load_data()\n",
    "except FileNotFoundError:\n",
    "    st.error(\"couldn't find nba_shots_optimized.csv. Is your data or path in the right spot?\")\n",
    "    st.stop()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0dd8c247-ba58-400f-86f8-4392d19835fb",
   "metadata": {},
   "source": [
    "## Setting Up the Sidebar Widgets\n",
    "\n",
    "We're using Streamlit's st.sidebar to shove all our filters over to the left side of the screen. This keeps the main area clean and dedicated entirely to our shot charts.\n",
    "\n",
    "The Player Dropdown:\n",
    "st.sidebar.selectbox grabs every unique name from player.player_name, sorts them A-to-Z, and drops them into a searchable dropdown. Whichever name the user clicks gets saved to selected_player.\n",
    "\n",
    "The Team Dropdown:\n",
    "st.sidebar.selectbox grabs every unique name from player.team_name, sorts them A-to-Z, and drops them into a searchable dropdown. Whichever team the user clicks gets saved to selected_team.\n",
    "\n",
    "The Season Slider:\n",
    "st.sidebar.slider looks at the minimum and maximum years in our Season column. By passing a tuple of both (min_season, max_season) as the starting point, Streamlit automatically turns it into a range slider with two draggable handles.\n",
    "\n",
    "The Shot Action Selector:\n",
    "st.sidebar.multiselect gets a list of specific play types (like a Step Back Jump Shot or Running Dunk). We drop any empty values with .dropna() so the UI stays clean. This starts empty, meaning the user can select as many specific play types as they want—or none at all.\n",
    "\n",
    "The Clutch Toggle:\n",
    "A simple st.sidebar.checkbox that returns True or False. We also added a help hover-tooltip to explain exactly what \"Clutch\" means in our app.\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "934ed1be-9d80-495a-a5a6-6fa25a6ec928",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 19:43:05.349 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.351 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.351 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.397 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.398 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.398 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.398 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.399 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.399 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.438 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.439 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.439 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.439 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.440 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.440 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.440 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.452 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.452 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.453 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.453 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.453 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.453 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.502 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.502 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.502 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.502 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.503 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.503 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.503 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.503 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.503 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.504 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.504 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:43:05.504 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "st.sidebar.header(\"Dashboard Filters\")\n",
    "\n",
    "\n",
    "\n",
    "# Filter: Team Selector\n",
    "all_teams = sorted(df['player.team_name'].unique().tolist())\n",
    "selected_team = st.sidebar.multiselect(\"Select a Team\", options=all_teams, default=[],help='Leave blank to include all teams.')\n",
    "\n",
    "if selected_team:\n",
    "    available_players_df = df[df['player.team_name'].isin(selected_teams)]\n",
    "else:\n",
    "    available_players_df = df\n",
    "\n",
    "# Filter: Player Selector\n",
    "all_players = sorted(available_players_df['player.player_name'].unique())\n",
    "selected_player = st.sidebar.selectbox(\"Select a Player\", all_players, index=0)\n",
    "\n",
    "# Filter: Season Range Slider\n",
    "clean_seasons = df['Season'].dropna()\n",
    "min_season = int(clean_seasons.min())\n",
    "max_season = int(clean_seasons.max())\n",
    "selected_seasons = st.sidebar.slider(\n",
    "    \"Select Season Range\", \n",
    "    min_season, \n",
    "    max_season, \n",
    "    (min_season, max_season)\n",
    ")\n",
    "\n",
    "# Filter: Action Type\n",
    "all_actions = sorted(df['player.action_type'].dropna().unique())\n",
    "selected_actions = st.sidebar.multiselect(\n",
    "    \"Filter by Shot Action (Optional)\", \n",
    "    all_actions, \n",
    "    default=[]\n",
    ")\n",
    "\n",
    "# Filter: Clutch Toggle\n",
    "clutch_only = st.sidebar.checkbox(\n",
    "    \"Clutch Situations Only\", \n",
    "    value=False,\n",
    "    help=\"Filters for shots taken in the 4th Quarter or Overtime with 5 or fewer minutes remaining.\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "3e0e1ced-bf03-4d0a-96c0-ba36f82de8a4",
   "metadata": {},
   "outputs": [],
   "source": [
    "filtered_df = df[\n",
    "    (df['player.player_name'] == selected_player) & \n",
    "    (df['Season'].between(selected_seasons[0],selected_seasons[1]))\n",
    "    ]\n",
    "\n",
    "if selected_team:\n",
    "    filtered_df = filtered_df[filtered_df['player.team_name'].isin(selected_team)]\n",
    "\n",
    "if selected_actions:\n",
    "    filtered_df = filtered_df[filtered_df['player.action_type'].isin(selected_actions)]\n",
    "\n",
    "if clutch_only:\n",
    "    filtered_df = filtered_df[\n",
    "        (filtered_df['player.period'] >= 4) & \n",
    "        (filtered_df['player.minutes_remaining'] <= 5)\n",
    "    ]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "05c2ce4a-69a5-4463-be35-73a3913aac30",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 19:50:58.771 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:50:58.771 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:50:58.772 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "total_shots = len(filtered_df)\n",
    "if total_shots >0:\n",
    "    made_shots = filtered_df['player.shot_made_numeric'].sum()\n",
    "    fg_pct = (made_shots / total_shots) * 100\n",
    "else:\n",
    "    fg_pct = 0.0\n",
    "\n",
    "# Header\n",
    "st.markdown(f\"### Current View: **{selected_player}** | Total Shots: `{total_shots}` | FG%: `{fg_pct:.1f}%`\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "03acfc52-cedc-423e-8118-d2d4a2baf6e2",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 19:52:14.847 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:52:14.849 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:52:14.850 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:52:14.851 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:52:14.851 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 19:52:14.852 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "row1_col1, row1_col2 = st.columns(2)\n",
    "row2_col1, row2_col2 = st.columns(2)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "51f396ba-6fcc-4d32-9f29-3d1a48f5abf2",
   "metadata": {},
   "source": [
    "Above we set up our dashboard grid. By default, streamlit piles everything into one long column. st.columns() lets you break that into multiple columns. \n",
    "\n",
    "by using st.columns(2) we tell streamlit to split the horizontal width of the page into two equal side by side columns. to put stuff in the columns we can use the with statement"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6600a3ef-d440-40e5-bd6c-5c331f8de5f8",
   "metadata": {},
   "source": [
    "# Shot Locations\n",
    "\n",
    "We'll use the plotly scatter functionality to build out our shots on court. We can map shot locations using loc_x and loc_y to represent the x and y coordinates on the court."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "d258e7ed-3c05-4946-8143-81a43e7060bd",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 20:11:12.935 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.938 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.938 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.978 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
      "2026-07-15 20:11:12.987 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.987 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.988 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.988 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:11:12.988 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "with row1_col1:\n",
    "    st.markdown(\"#### Shot Chart Location\")\n",
    "    if not filtered_df.empty:\n",
    "        # Create our base scatter plot\n",
    "        fig_map = px.scatter(\n",
    "            filtered_df,\n",
    "            x='player.loc_x',\n",
    "            y='player.loc_y',\n",
    "            color='player.shot_made_flag',\n",
    "            hover_data=['player.action_type', 'player.shot_distance'],\n",
    "            color_discrete_map={'Made Shot': '#2ca02c', 'Missed Shot': '#d62728'},\n",
    "            opacity=0.75, \n",
    "            title=\"Court Coordinates\"\n",
    "        )\n",
    "        \n",
    "        fig_map.add_layout_image(\n",
    "            dict(\n",
    "                source=\"https://raw.githubusercontent.com/gmf05/nba-shots/master/court.png\",\n",
    "                xref=\"x\",\n",
    "                yref=\"y\",\n",
    "                x=-250,      \n",
    "                y=418,       \n",
    "                sizex=500,   \n",
    "                sizey=470,   \n",
    "                sizing=\"stretch\",\n",
    "                opacity=0.5, \n",
    "                layer=\"below\" \n",
    "            )\n",
    "        )\n",
    "\n",
    "        fig_map.update_xaxes(\n",
    "            range=[-250, 250], \n",
    "            showgrid=False, \n",
    "            zeroline=False, \n",
    "            visible=False \n",
    "        )\n",
    "        fig_map.update_yaxes(\n",
    "            range=[-52, 418], \n",
    "            autorange=\"reversed\", \n",
    "            showgrid=False, \n",
    "            zeroline=False, \n",
    "            visible=False \n",
    "        )\n",
    "        \n",
    "        # Clean up chart layout\n",
    "        fig_map.update_layout(\n",
    "            width=500, \n",
    "            height=400, \n",
    "            legend_title=\"Outcome\",\n",
    "            plot_bgcolor=\"rgba(0,0,0,0)\", \n",
    "            paper_bgcolor=\"rgba(0,0,0,0)\"\n",
    "        )\n",
    "        \n",
    "        st.plotly_chart(fig_map, use_container_width=True)\n",
    "    else:\n",
    "        st.info(\"No shot data available for this player combination.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "84a10e72-89d5-4813-a01d-06dac66a6819",
   "metadata": {},
   "source": [
    "## Shot Breakdown\n",
    "\n",
    "Here we use a stacked bar to get a visual distribution of the % of 2s and 3s taken over the selected seasons."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "4c598f40-d097-4b15-ac35-e23f045ca16f",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 20:15:33.615 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.617 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.617 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.652 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
      "2026-07-15 20:15:33.653 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.654 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.654 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.654 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:15:33.655 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "with row1_col2:\n",
    "    st.markdown(\"#### 2-Pointers vs 3-Pointers\")\n",
    "    if not filtered_df.empty:\n",
    "        type_by_season = (\n",
    "            filtered_df.groupby(['Season', 'player.shot_type'], observed=False)\n",
    "            .size()\n",
    "            .reset_index(name='Shot Count')\n",
    "        )\n",
    "        \n",
    "        fig_bar = px.bar(\n",
    "            type_by_season,\n",
    "            x='Season',\n",
    "            y='Shot Count',\n",
    "            color='player.shot_type',\n",
    "            title=\"Yearly Shot Selection Breakdown\",\n",
    "            barmode='stack', \n",
    "            color_discrete_sequence=px.colors.qualitative.Set2,\n",
    "            labels={'player.shot_type': 'Shot Type', 'Shot Count': 'Number of Attempts'}\n",
    "        )\n",
    "        \n",
    "        fig_bar.update_layout(\n",
    "            height=400,\n",
    "            xaxis=dict(tickmode='linear'),\n",
    "            legend_title=\"Shot Type\"\n",
    "        )\n",
    "        \n",
    "        st.plotly_chart(fig_bar, use_container_width=True)\n",
    "    else:\n",
    "        st.info(\"No shot data available.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6b30060d-15c1-4776-b458-d610dea9ecf6",
   "metadata": {},
   "source": [
    "## Shot Distance Histogram\n",
    "\n",
    "We can use a histogram to show the distance ranges teams and players are shooting from"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "dfee8dc9-1de3-4bf4-8b2e-e35767097178",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 20:17:47.431 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.433 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.434 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "/var/folders/nc/rp01x1r53k12vk5f23w_z4zh0000gn/T/ipykernel_26262/263725117.py:4: SettingWithCopyWarning:\n",
      "\n",
      "\n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "\n",
      "2026-07-15 20:17:47.481 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
      "2026-07-15 20:17:47.482 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.482 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.483 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.483 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:17:47.483 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "with row2_col1:\n",
    "    st.markdown(\"#### 📏 Shot Frequency by Distance\")\n",
    "    if not filtered_df.empty:\n",
    "        filtered_df['distance_bin'] = pd.cut(\n",
    "            filtered_df['player.shot_distance'], \n",
    "            bins=[-1, 5, 10, 15, 20, 25, 40], \n",
    "            labels=['0-5 ft', '6-10 ft', '11-15 ft', '16-20 ft', '21-25 ft', '26+ ft']\n",
    "        )\n",
    "        dist_grouped = filtered_df.groupby('distance_bin', observed=False).size().reset_index(name='Attempts')\n",
    "        \n",
    "        fig_dist = px.bar(\n",
    "            dist_grouped,\n",
    "            x='distance_bin',\n",
    "            y='Attempts',\n",
    "            labels={'distance_bin': 'Shot Distance (Feet)'},\n",
    "            title=\"Attempts Volume by Distance Range\"\n",
    "        )\n",
    "        fig_dist.update_layout(height=400)\n",
    "        st.plotly_chart(fig_dist, use_container_width=True)\n",
    "    else:\n",
    "        st.info(\"No shot data available.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e9fd49f9-9790-4cff-9d7e-4ee51582feb5",
   "metadata": {},
   "source": [
    "## FG% Trend\n",
    "\n",
    "A line chart is the perfect medium to display a yearly trend for how efficient teams and players are."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "baa922c6-0146-4437-84b2-4f50955923e5",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-15 20:21:01.634 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.636 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.637 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.677 Please replace `use_container_width` with `width`.\n",
      "\n",
      "`use_container_width` will be removed after 2025-12-31.\n",
      "\n",
      "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
      "2026-07-15 20:21:01.678 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.679 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-07-15 20:21:01.680 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "with row2_col2:\n",
    "    st.markdown(\"#### Efficiency Trend Across Seasons (2015-2020)\")\n",
    "    if not filtered_df.empty:\n",
    "        trend_df = filtered_df.groupby('Season')['player.shot_made_numeric'].mean().reset_index()\n",
    "        trend_df['Field Goal %'] = trend_df['player.shot_made_numeric'] * 100\n",
    "        \n",
    "        fig_trend = px.line(\n",
    "            trend_df,\n",
    "            x='Season',\n",
    "            y='Field Goal %',\n",
    "            markers=True,\n",
    "            title=\"Yearly Shooting Accuracy Trend\"\n",
    "        )\n",
    "        fig_trend.update_yaxes(range=[0, 100])\n",
    "        fig_trend.update_layout(height=400, xaxis=dict(tickmode='linear'))\n",
    "        st.plotly_chart(fig_trend, use_container_width=True)\n",
    "    else:\n",
    "        st.info(\"No progression data available.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d5b62e8f-189a-44f2-9cc0-6d189c8d1081",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
