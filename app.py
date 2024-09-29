import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load your dataset here (assuming you have the dataset available)
df = pd.read_csv('your_dataset.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the server for deployment
server = app.server  # This is required for Gunicorn to work

# Define the layout
app.layout = html.Div(children=[
    html.H1("Dengue Cases in the Philippines Dashboard"),
    html.P("This dashboard presents an overview of dengue cases in the Philippines."),

    # Dropdown for selecting the year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
        value=df['Year'].min(),
        clearable=False
    ),

    # Graph 1: Dengue Cases Over Time (scatter plot)
    dcc.Graph(id='cases-over-time'),

    # Graph 2: Pie chart for cases distribution by region
    dcc.Graph(id='cases-distribution'),

    # Graph 3: Bar chart for cases by region
    dcc.Graph(id='cases-by-region'),

    # Conclusion section
    html.H4("Conclusion"),
    html.P(id='conclusion-text')
])

# Callback to update graphs based on year selection
@app.callback(
    [dash.dependencies.Output('cases-by-region', 'figure'),
     dash.dependencies.Output('cases-distribution', 'figure'),
     dash.dependencies.Output('cases-over-time', 'figure'),
     dash.dependencies.Output('conclusion-text', 'children')],
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_graphs(selected_year):
    # Filter the data based on selected year
    filtered_df = df[df['Year'] == selected_year]

    # Graph 1: Dengue Cases Over the Years (scatter plot)
    scatter_fig = px.scatter(df, x='Year', y='Dengue_Cases', title="Dengue Cases Over the Years")

    # Graph 2: Pie chart for cases distribution by region
    pie_fig = px.pie(filtered_df, values='Dengue_Cases', names='Region', title=f"Dengue Cases Distribution by Region for {selected_year}")

    # Graph 3: Bar chart for cases by region
    bar_fig = px.bar(filtered_df, x='Region', y='Dengue_Cases', title=f"Dengue Cases by Region for {selected_year}")

    # Conclusion text
    conclusion = (f"In {selected_year}, the region with the highest cases was {filtered_df.loc[filtered_df['Dengue_Cases'].idxmax(), 'Region']}. "
                  f"Since the Philippines is a tropical country, it provides an ideal environment for the spread of dengue fever. "
                  f"The abundance of stagnant water, high rainfall, and humidity create breeding grounds for mosquitoes, which transmit the dengue virus. "
                  f"Factors such as urbanization and population density further contribute to the disease's spread.")

    return bar_fig, pie_fig, scatter_fig, conclusion

if __name__ == '__main__':
    app.run_server(debug=True)
