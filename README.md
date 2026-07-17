# um-mads-sharing
Repo for UM MADS Projects
Basketball Shot Dashboard
This project is a data visualization dashboard built to analyze basketball shot performance, player efficiency, and team shot selection patterns using Python, Streamlit, and Plotly.

Overview
This dashboard allows users to:

Visualize Shot Charts: View shot locations overlaid on a professional basketball court diagram.

Toggle Views: Switch between individual player and team-level visualizations dynamically.

Analyze Trends: Examine shot selection breakdowns (2-pointers vs. 3-pointers) across different seasons.

Interactive Filtering: Use built-in filters to compare performance metrics and shot efficiency.

Installation & Running Locally
To run this dashboard on your local machine, follow these steps:

Clone the repository:

Bash
git clone https://github.com/bhannibal24/um-mads-sharing.git
cd um-mads-sharing
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
streamlit run app.py
Project Deliverables
Live Dashboard: [Insert Link to your Streamlit App URL Here]

Jupyter Notebook: View the Analysis Notebook

Data Source: Note: Raw datasets are excluded from this repository due to size constraints.

Troubleshooting
Legend display: If the legend shows individual players when teams are selected, ensure the color parameter in your px.scatter call is mapped to the team-name column.

Image Alignment: The background court image requires specific coordinate scaling to align with the scatter plot (x and y range). If the image appears distorted, verify your layout parameters in fig_map.add_layout_image.

Dependencies
This project uses:

streamlit

pandas

plotly

