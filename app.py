import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('denguecases.csv')

# Initialize the app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Dengue Cases in the Philippines Dashboard"),
    html.P("This dashboard presents an overview of dengue cases in the Philippines."),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in df['Year'].unique()],
        value=df['Year'].min()
    ),
    dcc.Graph(id='cases-by-region'),
    dcc.Graph(id='cases-distribution'),
    dcc.Graph(id='cases-over-time'),
    html.H4("Conclusion"),
    html.P(id='conclusion-text')
])

# Define callback to update graphs and conclusion
@app.callback(
    [Output('cases-by-region', 'figure'),
     Output('cases-distribution', 'figure'),
     Output('cases-over-time', 'figure'),
     Output('conclusion-text', 'children')],
    [Input('year-dropdown', 'value')]
)
def update_dashboard(selected_year):
    # Filter data by selected year
    filtered_df = df[df['Year'] == selected_year]

    # Bar chart for dengue cases by region
    bar_fig = px.bar(filtered_df, x='Region', y='Dengue_Cases',
                     title=f'Dengue Cases by Region for {selected_year}')
    
    # Pie chart for dengue cases distribution by region
    pie_fig = px.pie(filtered_df, names='Region', values='Dengue_Cases',
                     title=f'Dengue Cases Distribution by Region for {selected_year}')
    
    # Scatter plot for dengue cases over the years
    scatter_fig = px.scatter(df, x='Year', y='Dengue_Cases',
                             title='Dengue Cases Over the Years',
                             color='Region')

    # Generate conclusion text
    max_region = filtered_df.loc[filtered_df['Dengue_Cases'].idxmax()]['Region']
    conclusion = (f"In {selected_year}, the region with the highest cases was {max_region}. "
                  f"Since the Philippines is a tropical country, it provides an ideal environment for the spread of dengue fever. "
                  f"The abundance of stagnant water, high rainfall, and humidity create breeding grounds for mosquitoes, "
                  f"which transmit the dengue virus. Factors such as urbanization and population density further contribute to the disease's spread.")

    return bar_fig, pie_fig, scatter_fig, conclusion

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
