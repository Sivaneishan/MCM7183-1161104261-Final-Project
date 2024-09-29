import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dengue dataset
df = pd.read_csv('denguecases.csv')

# Convert 'year' column to work with the slider (assuming you have a 'year' column)
df['year'] = pd.to_datetime(df['year'], format='%Y')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Dengue Cases in Philippines Dashboard'),
    
    html.P(children="These charts show the dengue cases in the Philippines across different years and regions."),
    
    # Dropdown for selecting the graph
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Bar Chart: Dengue Cases by Region', 'value': 'bar'},
            {'label': 'Pie Chart: Dengue Cases by Region', 'value': 'pie'},
            {'label': 'Scatter Plot: Dengue Cases vs Year', 'value': 'scatter'}
        ],
        value='bar',  # Default graph
        clearable=False
    ),
    
    # Graph that will change based on the dropdown selection
    dcc.Graph(id='main-graph'),
    
    # Slider for filtering by year
    html.Label('Select Year:'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].dt.year.min(),
        max=df['year'].dt.year.max(),
        step=1,
        value=df['year'].dt.year.min(),  # Default value
        marks={str(year): str(year) for year in range(df['year'].dt.year.min(), df['year'].dt.year.max() + 1)}
    ),
    
    # Checklist to filter by region
    html.Label('Filter by Region:'),
    dcc.Checklist(
        id='region-selector',
        options=[{'label': region, 'value': region} for region in df['region'].unique()],
        value=df['region'].unique(),  # Default value
        inline=True
    ),
    
    # Dynamic Conclusion Section
    html.Div(id='dynamic-conclusion', style={'margin-top': '20px'})
])

# Define callback to update the graph and dynamic conclusion based on interactions
@app.callback(
    [Output('main-graph', 'figure'),
     Output('dynamic-conclusion', 'children')],  # New output for dynamic conclusion
    [Input('graph-selector', 'value'),
     Input('year-slider', 'value'),
     Input('region-selector', 'value')]
)
def update_graph_and_notes(selected_graph, selected_year, selected_regions):
    # Filter data based on selected year and regions
    filtered_df = df[(df['year'].dt.year == selected_year) & (df['region'].isin(selected_regions))]
    
    # Select graph and generate dynamic conclusion based on user input
    if selected_graph == 'bar':
        fig = px.bar(filtered_df, x='region', y='cases', title=f'Dengue Cases by Region in {selected_year}', barmode='group')
        top_region = filtered_df.groupby('region')['cases'].sum().idxmax()
        conclusion_text = f"In {selected_year}, {top_region} had the highest number of dengue cases."
    
    elif selected_graph == 'pie':
        fig = px.pie(filtered_df, names='region', values='cases', title=f'Dengue Cases by Region in {selected_year}')
        top_region = filtered_df.groupby('region')['cases'].sum().idxmax()
        conclusion_text = f"In {selected_year}, {top_region} had the highest proportion of dengue cases."
    
    elif selected_graph == 'scatter':
        fig = px.scatter(filtered_df, x='year', y='cases', color='region', title=f'Dengue Cases vs Year for Selected Regions')
        conclusion_text = f"This scatter plot shows the dengue cases over the years for the selected regions."

    # Return both the graph and the dynamic conclusion
    return fig, html.P(conclusion_text)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
