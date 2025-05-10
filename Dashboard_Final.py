import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
import os
from dash import Dash
import dash_bootstrap_components as dbc
import plotly.io as pio
import plotly.graph_objects as go

# Custom CSS
CUSTOM_CSS = {
    'font-family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    'background-color': '#f8f9fa',
    'color': '#2c3e50'
}

# Define a consistent color scheme
COLORS = {
    'background': '#f8f9fa',
    'text': '#2c3e50',
    'primary': '#3498db',
    'secondary': '#95a5a6',
    'accent': '#e74c3c',
    'dark_gray': '#34495e',
    'medium_gray': '#7f8c8d',
    'light_gray': '#bdc3c7'
}

# Card styles
CARD_STYLE = {
    'border': 'none',
    'border-radius': '8px',
    'box-shadow': '0 2px 4px rgba(0,0,0,0.05), 0 4px 8px rgba(0,0,0,0.05)',
    'background-color': 'white',
    'transition': 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out'
}

CARD_HEADER_STYLE = {
    'background-color': 'white',
    'border-bottom': '1px solid #e9ecef',
    'border-radius': '8px 8px 0 0',
    'padding': '1rem'
}

CARD_BODY_STYLE = {
    'padding': '1.25rem'
}

# Load the CSV files
ai_subset = pd.read_excel("Salary_Sub.xlsx")

# Dash app setup with Bootstrap theme
app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap'
])

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Education Trends in AI Job Market</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: ''' + CUSTOM_CSS['font-family'] + ''';
                background-color: ''' + CUSTOM_CSS['background-color'] + ''';
                color: ''' + CUSTOM_CSS['color'] + ''';
            }
            .card {
                border: ''' + CARD_STYLE['border'] + ''';
                border-radius: ''' + CARD_STYLE['border-radius'] + ''';
                box-shadow: ''' + CARD_STYLE['box-shadow'] + ''';
                background-color: ''' + CARD_STYLE['background-color'] + ''';
                transition: ''' + CARD_STYLE['transition'] + ''';
            }
            .card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1);
            }
            .card-no-hover {
                transition: none;
            }
            .card-no-hover:hover {
                transform: none;
                box-shadow: ''' + CARD_STYLE['box-shadow'] + ''';
            }
            .card-header {
                background-color: ''' + CARD_HEADER_STYLE['background-color'] + ''';
                border-bottom: ''' + CARD_HEADER_STYLE['border-bottom'] + ''';
                border-radius: ''' + CARD_HEADER_STYLE['border-radius'] + ''';
                padding: ''' + CARD_HEADER_STYLE['padding'] + ''';
            }
            .card-body {
                padding: ''' + CARD_BODY_STYLE['padding'] + ''';
            }
            .nav-tabs {
                border-bottom: none;
                margin-bottom: 0;
                background-color: white;
                padding: 0 1rem;
                border-radius: 8px 8px 0 0;
            }
            .nav-tabs .nav-link {
                color: #4a5568;
                font-weight: 500;
                border: none;
                padding: 1rem 1.5rem;
                margin-right: 0.5rem;
                border-radius: 8px 8px 0 0;
                transition: all 0.2s ease-in-out;
                margin-bottom: -1px;
            }
            .nav-tabs .nav-link:hover {
                color: #2d3748;
                background-color: rgba(0,0,0,0.03);
            }
            .nav-tabs .nav-link.active {
                color: #1a202c;
                font-weight: 600;
                background-color: white;
                border: none;
                box-shadow: none;
                position: relative;
            }
            .nav-tabs .nav-link.active::after {
                content: '';
                position: absolute;
                bottom: -1px;
                left: 0;
                right: 0;
                height: 1px;
                background-color: white;
            }
            h1 {
                font-weight: 600;
                letter-spacing: -0.5px;
                color: #1a202c;
            }
            h5 {
                font-weight: 500;
                letter-spacing: -0.25px;
                color: #2d3748;
            }
            .Select-control {
                border-radius: 6px !important;
                border: 1px solid #e2e8f0 !important;
            }
            .Select-control:hover {
                border-color: #cbd5e0 !important;
            }
            .Select-menu-outer {
                border: none !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                border-radius: 8px !important;
            }
            .Select-option {
                color: #4a5568 !important;
            }
            .Select-option:hover {
                background-color: #f7fafc !important;
                color: #2d3748 !important;
            }
            .Select-option.is-selected {
                background-color: #edf2f7 !important;
                color: #1a202c !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = dbc.Container([
    html.H1("Education Trends in the AI Job Market", 
            className="text-center my-3",
            style={'color': COLORS['text']}),
    
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Education Requirements', value='tab1', children=[
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Education Requirements Analysis", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.H5("Filters", className="mb-0")
                                ]),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        id='skill-filter',
                                        options=[{'label': skill, 'value': skill} for skill in ai_subset['skill_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='education-filter',
                                        options=[{'label': edu, 'value': edu} for edu in ai_subset['min_edulevels_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Education Level",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='subcategory-filter',
                                        options=[{'label': subcat, 'value': subcat} for subcat in ai_subset['skill_subcategory_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill Subcategory",
                                        className="mb-3"
                                    ),
                                    dcc.RangeSlider(
                                        id='year-filter',
                                        min=ai_subset['year'].min(),
                                        max=ai_subset['year'].max(),
                                        marks={year: str(year) for year in range(ai_subset['year'].min(), ai_subset['year'].max()+1, 2)},
                                        value=[ai_subset['year'].min(), ai_subset['year'].max()],
                                        className="mb-3"
                                    )
                                ])
                            ], className="mb-4")
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='education-requirements-plot')
                                ])
                            ])
                        ], width=9)
                    ])
                ])
            ], className="mt-0 card-no-hover")
        ]),
        
        dcc.Tab(label='Degree Trends', value='tab2', children=[
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Degree Requirements Analysis", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.H5("Filters", className="mb-0")
                                ]),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        id='degree-skill-filter',
                                        options=[{'label': skill, 'value': skill} for skill in ai_subset['skill_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='degree-education-filter',
                                        options=[{'label': edu, 'value': edu} for edu in ai_subset['min_edulevels_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Education Level",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='degree-subcategory-filter',
                                        options=[{'label': subcat, 'value': subcat} for subcat in ai_subset['skill_subcategory_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill Subcategory",
                                        className="mb-3"
                                    ),
                                    dcc.RangeSlider(
                                        id='degree-year-filter',
                                        min=ai_subset['year'].min(),
                                        max=ai_subset['year'].max(),
                                        marks={year: str(year) for year in range(ai_subset['year'].min(), ai_subset['year'].max()+1, 2)},
                                        value=[ai_subset['year'].min(), ai_subset['year'].max()],
                                        className="mb-3"
                                    )
                                ])
                            ], className="mb-4")
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='degree-trend-plot')
                                ])
                            ])
                        ], width=9)
                    ])
                ])
            ], className="mt-0 card-no-hover")
        ]),
        
        dcc.Tab(label='Salary Analysis', value='tab3', children=[
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Salary Distribution Analysis", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.H5("Filters", className="mb-0")
                                ]),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        id='salary-skill-filter',
                                        options=[{'label': skill, 'value': skill} for skill in ai_subset['skill_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='salary-education-filter',
                                        options=[{'label': edu, 'value': edu} for edu in ai_subset['min_edulevels_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Education Level",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='salary-subcategory-filter',
                                        options=[{'label': subcat, 'value': subcat} for subcat in ai_subset['skill_subcategory_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill Subcategory",
                                        className="mb-3"
                                    ),
                                    dcc.RangeSlider(
                                        id='salary-year-filter',
                                        min=ai_subset['year'].min(),
                                        max=ai_subset['year'].max(),
                                        marks={year: str(year) for year in range(ai_subset['year'].min(), ai_subset['year'].max()+1, 2)},
                                        value=[ai_subset['year'].min(), ai_subset['year'].max()],
                                        className="mb-3"
                                    )
                                ])
                            ], className="mb-4")
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='salary-distribution-plot')
                                ])
                            ])
                        ], width=9)
                    ])
                ])
            ], className="mt-0 card-no-hover")
        ]),
        
        dcc.Tab(label='Geographic Analysis', value='tab4', children=[
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Geographic Distribution Analysis", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader([
                                    html.H5("Filters", className="mb-0")
                                ]),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        id='geo-skill-filter',
                                        options=[{'label': skill, 'value': skill} for skill in ai_subset['skill_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='geo-education-filter',
                                        options=[{'label': edu, 'value': edu} for edu in ai_subset['min_edulevels_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Education Level",
                                        className="mb-3"
                                    ),
                                    dcc.Dropdown(
                                        id='geo-subcategory-filter',
                                        options=[{'label': subcat, 'value': subcat} for subcat in ai_subset['skill_subcategory_name'].unique()],
                                        multi=True,
                                        placeholder="Filter by Skill Subcategory",
                                        className="mb-3"
                                    ),
                                    dcc.RangeSlider(
                                        id='geo-year-filter',
                                        min=ai_subset['year'].min(),
                                        max=ai_subset['year'].max(),
                                        marks={year: str(year) for year in range(ai_subset['year'].min(), ai_subset['year'].max()+1, 2)},
                                        value=[ai_subset['year'].min(), ai_subset['year'].max()],
                                        className="mb-3"
                                    )
                                ])
                            ], className="mb-4")
                        ], width=3),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='education-by-city-plot')
                                ])
                            ])
                        ], width=9)
                    ])
                ])
            ], className="mt-0 card-no-hover")
        ])
    ])
], fluid=True, style={'padding': '0'})

@app.callback(
    [Output('education-requirements-plot', 'figure'),
     Output('degree-trend-plot', 'figure'),
     Output('salary-distribution-plot', 'figure'),
     Output('education-by-city-plot', 'figure')],
    [Input('skill-filter', 'value'),
     Input('education-filter', 'value'),
     Input('year-filter', 'value'),
     Input('subcategory-filter', 'value'),
     Input('degree-skill-filter', 'value'),
     Input('degree-education-filter', 'value'),
     Input('degree-year-filter', 'value'),
     Input('degree-subcategory-filter', 'value'),
     Input('salary-skill-filter', 'value'),
     Input('salary-education-filter', 'value'),
     Input('salary-year-filter', 'value'),
     Input('salary-subcategory-filter', 'value'),
     Input('geo-skill-filter', 'value'),
     Input('geo-education-filter', 'value'),
     Input('geo-year-filter', 'value'),
     Input('geo-subcategory-filter', 'value')]
)
def update_plots(skills, education_levels, years, skill_subcategories,
                degree_skills, degree_education, degree_years, degree_subcategories,
                salary_skills, salary_education, salary_years, salary_subcategories,
                geo_skills, geo_education, geo_years, geo_subcategories):
    
    # Education Requirements Plot
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
        title="Education Requirements by Skill",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig1.update_layout(
        xaxis_title="Minimum Education Level",
        yaxis_title="Number of Job Listings",
        title_font_size=20,
        showlegend=False,
        font=dict(family="Inter, sans-serif", size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Degree Trends Plot
    degree_df = ai_subset[(ai_subset['year'] >= degree_years[0]) & (ai_subset['year'] <= degree_years[1])]
    if degree_skills:
        degree_df = degree_df[degree_df['skill_name'].isin(degree_skills)]
    if degree_education:
        degree_df = degree_df[degree_df['min_edulevels_name'].isin(degree_education)]
    if degree_subcategories:
        degree_df = degree_df[degree_df['skill_subcategory_name'].isin(degree_subcategories)]

    # Plot 2: Degree Trend Over Time
    edu_trend = degree_df.groupby(['year', 'min_edulevels_name']).size().reset_index(name='count')
    fig2 = px.line(
        edu_trend,
        x='year',
        y='count',
        color='min_edulevels_name',
        title="Degree Requirements Over Time",
        template="plotly_white",
        color_discrete_sequence=['#440154', '#3b528b', '#21918c', '#5ec962', '#b8de29', '#fde725']
    )
    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Job Listings",
        font=dict(family="Inter, sans-serif", size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Salary Distribution Plot
    salary_df = ai_subset[(ai_subset['year'] >= salary_years[0]) & (ai_subset['year'] <= salary_years[1])]
    if salary_skills:
        salary_df = salary_df[salary_df['skill_name'].isin(salary_skills)]
    if salary_education:
        salary_df = salary_df[salary_df['min_edulevels_name'].isin(salary_education)]
    if salary_subcategories:
        salary_df = salary_df[salary_df['skill_subcategory_name'].isin(salary_subcategories)]

    # Plot 3: Salary Distribution by Education Level
    fig3 = px.box(
        salary_df,
        x='min_edulevels_name',
        y='salary',
        color='min_edulevels_name',
        title="Salary Distribution by Education",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig3.update_layout(
        xaxis_title="Minimum Education Level",
        yaxis_title="Salary (USD)",
        showlegend=False,
        font=dict(family="Inter, sans-serif", size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Geographic Analysis Plot
    geo_df = ai_subset[(ai_subset['year'] >= geo_years[0]) & (ai_subset['year'] <= geo_years[1])]
    if geo_skills:
        geo_df = geo_df[geo_df['skill_name'].isin(geo_skills)]
    if geo_education:
        geo_df = geo_df[geo_df['min_edulevels_name'].isin(geo_education)]
    if geo_subcategories:
        geo_df = geo_df[geo_df['skill_subcategory_name'].isin(geo_subcategories)]

    # Plot 4: Education Level by City
    top_cities = geo_df['city_name'].value_counts().nlargest(10).index
    city_edu_counts = geo_df[geo_df['city_name'].isin(top_cities)]\
        .groupby('city_name').size().reset_index(name='count')
    
    fig4 = px.bar(
        city_edu_counts,
        x='city_name',
        y='count',
        color='city_name',
        title="Education Level by Top Cities",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig4.update_layout(
        xaxis_title="City - Minimum Education Level",
        yaxis_title="Number of Job Listings",
        showlegend=False,
        font=dict(family="Inter, sans-serif", size=14),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig1, fig2, fig3, fig4

server = app.server

if __name__ == "__main__":
    app.run(debug=False)
