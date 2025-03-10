import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime

# Load the CSV files
ai_subset = pd.read_csv("Salary_Sub.csv")

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AI Job Market Dashboard"),
    
    dcc.Dropdown(
        id='skill-filter',
        options=[{'label': skill, 'value': skill} for skill in ai_subset['skill_name'].unique()],
        multi=True,
        placeholder="Filter by Skill"
    ),
    
    dcc.Dropdown(
        id='education-filter',
        options=[{'label': edu, 'value': edu} for edu in ai_subset['min_edulevels_name'].unique()],
        multi=True,
        placeholder="Filter by Education Level"
    ),
    
    dcc.RangeSlider(
        id='year-filter',
        min=ai_subset['year'].min(),
        max=ai_subset['year'].max(),
        marks={year: str(year) for year in range(ai_subset['year'].min(), ai_subset['year'].max()+1, 2)},
        value=[ai_subset['year'].min(), ai_subset['year'].max()]
    ),
    
    dcc.Graph(id='education-requirements-plot'),
    dcc.Graph(id='degree-trend-plot'),
    dcc.Graph(id='salary-distribution-plot'),
    dcc.Graph(id='education-by-city-plot')
])

@app.callback(
    [Output('education-requirements-plot', 'figure'),
     Output('degree-trend-plot', 'figure'),
     Output('salary-distribution-plot', 'figure'),
     Output('education-by-city-plot', 'figure')],
    [Input('skill-filter', 'value'),
     Input('education-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_plots(skills, education_levels, years):
    filtered_df = ai_subset[(ai_subset['year'] >= years[0]) & (ai_subset['year'] <= years[1])]
    if skills:
        filtered_df = filtered_df[filtered_df['skill_name'].isin(skills)]
    if education_levels:
        filtered_df = filtered_df[filtered_df['min_edulevels_name'].isin(education_levels)]
    
    # Plot 1: Education Requirements by Skill
    skill_edu_counts = filtered_df.groupby(['skill_name', 'min_edulevels_name']).size().reset_index(name='count')
    fig1 = px.bar(skill_edu_counts, x='skill_name', y='count', color='min_edulevels_name', title="Education Requirements by Skill")
    
    # Plot 2: Degree Trend Over Time
    edu_trend = filtered_df.groupby(['year', 'min_edulevels_name']).size().reset_index(name='count')
    fig2 = px.line(edu_trend, x='year', y='count', color='min_edulevels_name', title="Degree Requirements Over Time")
    
    # Plot 3: Salary Distribution by Education Level
    fig3 = px.box(filtered_df, x='min_edulevels_name', y='salary', color='min_edulevels_name', title="Salary Distribution by Education")
    
    # Plot 4: Education Level by City
    top_cities = filtered_df['city_name'].value_counts().nlargest(10).index
    city_edu_counts = filtered_df[filtered_df['city_name'].isin(top_cities)].groupby(['city_name', 'min_edulevels_name']).size().reset_index(name='count')
    fig4 = px.bar(city_edu_counts, x='city_name', y='count', color='min_edulevels_name', title="Education Level by Top Cities")
    
    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=10000)
