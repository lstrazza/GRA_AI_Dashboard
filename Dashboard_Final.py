import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
from flask import Flask
import os
from dash import Dash

# Load the CSV files
ai_subset = pd.read_excel("Salary_Sub.xlsx")

# Dash app setup
app = Dash(__name__)



app.layout = html.Div([
    html.H1("Education Trends in the AI Job Market"),
    
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
    
    dcc.Dropdown(
    id='subcategory-filter',
    options=[{'label': subcat, 'value': subcat} for subcat in ai_subset['skill_subcategory_name'].unique()],
    multi=True,
    placeholder="Filter by Skill Subcategory"
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
     Input('year-filter', 'value'),
     Input('subcategory-filter', 'value')]  # <-- New Input for Skill Subcategory
)
def update_plots(skills, education_levels, years, skill_subcategories):
    # Updated function code as shown above
    filtered_df = ai_subset[(ai_subset['year'] >= years[0]) & (ai_subset['year'] <= years[1])]
    
    if skills:
        filtered_df = filtered_df[filtered_df['skill_name'].isin(skills)]
        
    if education_levels:
        filtered_df = filtered_df[filtered_df['min_edulevels_name'].isin(education_levels)]
        
    if skill_subcategories:
        filtered_df = filtered_df[filtered_df['skill_subcategory_name'].isin(skill_subcategories)]

    # Plot 1: Education Requirements by Skill
    skill_edu_counts = filtered_df.groupby('min_edulevels_name').size().reset_index(name='count')

    fig1 = px.bar(
        skill_edu_counts,
        x='min_edulevels_name',
        y='count',
        color='min_edulevels_name',
        title="Education Requirements by Skill"
    )

    # Customizing Axis Titles
    fig1.update_layout(
        xaxis_title="Minimum Education Level",  
        yaxis_title="Number of Job Listings",  
        title_font_size=20  )
    

    # Plot 2: Degree Trend Over Time
    edu_trend = filtered_df.groupby(['year', 'min_edulevels_name']).size().reset_index(name='count')
    fig2 = px.line(
        edu_trend,
        x='year',
        y='count',
        color='min_edulevels_name',
        title="Degree Requirements Over Time"
    )
    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Job Listings"
    )

    # Plot 3: Salary Distribution by Education Level
    fig3 = px.box(
        filtered_df,
        x='min_edulevels_name',
        y='salary',
        color='min_edulevels_name',
        title="Salary Distribution by Education"
    )
    fig3.update_layout(
        xaxis_title="Minimum Education Level",
        yaxis_title="Salary (USD)"
    )

    # Plot 4: Education Level by City
    top_cities = filtered_df['city_name'].value_counts().nlargest(10).index
 
    city_edu_counts = filtered_df[filtered_df['city_name'].isin(top_cities)]\
    .groupby('city_name').size().reset_index(name='count')


    # Plot with combined labels to remove gaps
    fig4 = px.bar(
        city_edu_counts,
        x='city_name',
        y='count',
        color='city_name',  # Retain color for visual clarity
        title="Education Level by Top Cities"
    )

    # Customizing Axis Titles
    fig4.update_layout(
        xaxis_title="City - Minimum Education Level",
        yaxis_title="Number of Job Listings"
    )

    
    return fig1, fig2, fig3, fig4

#port = int(os.getenv('PORT', 10000))
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
