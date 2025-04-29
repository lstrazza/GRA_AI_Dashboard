AI Job Market Dashboard
Overview
This project is an interactive dashboard built using Dash and Plotly to visualize trends in the AI job market. The dashboard allows users to filter job listings by skills, education levels, skill subcategories, and year range, providing a dynamic view of how different factors influence job requirements and salaries over time.

The dashboard visualizes the following:

Education Requirements by Skill

Degree Requirements Over Time

Salary Distribution by Education Level

Education Level Distribution Across Top Cities

Project Structure
app.py: The main Python script containing the Dash app code.

Salary_Sub.xlsx: The Excel file containing job listing data used by the dashboard.

Features
Multi-select dropdowns to filter by Skill, Education Level, and Skill Subcategory.

Range slider to filter jobs by year.

Interactive plots built using Plotly Express:

Bar charts, Line charts, and Box plots.

Automatic updates of plots based on selected filters.

Top cities identified dynamically for the city-level education visualization.

Requirements
Python 3.7+

Required Python libraries:

pandas

numpy

plotly

dash

seaborn

matplotlib

flask

openpyxl (needed for reading .xlsx files)

You can install all necessary libraries using:

bash
Copy
Edit
pip install pandas numpy plotly dash seaborn matplotlib flask openpyxl
How to Run the App
Make sure Salary_Sub.xlsx is in the same directory as the Python script, or update the file path in the script.

Run the following command in your terminal:

bash
Copy
Edit
python app.py
Open your browser and navigate to: https://gra-ai-dashboard.onrender.com/ 

The dashboard will automatically refresh as you adjust the dropdowns and slider.

Callback Explanation
The app uses a callback to dynamically update four graphs based on user input:

Inputs:

skill-filter

education-filter

year-filter

subcategory-filter

Outputs:

Education Requirements Bar Plot

Degree Trend Line Plot

Salary Distribution Box Plot

Education by City Bar Plot

The callback filters the dataset based on user selections and updates the plots in real-time.

Notes
If running on a web server (like Heroku or AWS), uncomment the port line and set the appropriate environment variable for the port.

The server = app.server line is important if you plan to deploy this app.