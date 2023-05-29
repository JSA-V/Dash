import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import wordcloud
#from jupyter_dash import JupyterDash

# Load data from CSV file
df = pd.read_csv('comments.csv')

# Initialize the Dash app

#app=JupyterDash(__name__)
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='time-series'),
    ], className='six columns', style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='barplot'),
    ], className='six columns', style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='word-cloud'),
    ], className='six columns', style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(id='dropdown',
                     options=[{'label': s, 'value': s} for s in df.source.unique()],
                     multi=True,
                     placeholder='Select source...'),
        dcc.Graph(id='subset-plot'),
    ], className='six columns', style={'width': '50%', 'display': 'inline-block'}),
], className='row')


# Define the callback for the time-series graph
@app.callback(Output('time-series', 'figure'),
              Input('dropdown', 'value'))
def update_time_series(selected_sources):
    if selected_sources:
        filtered_df = df[df.source.isin(selected_sources)]
    else:
        filtered_df = df
    fig = px.line(filtered_df, x='date', y='sentiment', title='Sentiment over time')
    return fig

# Define the callback for the barplot graph
@app.callback(Output('barplot', 'figure'),
              Input('dropdown', 'value'))
def update_barplot(selected_sources):
    if selected_sources:
        filtered_df = df[df.source.isin(selected_sources)]
    else:
        filtered_df = df
    fig = px.histogram(filtered_df, x='source', color='sentiment', barmode='group', title='Sentiment by source')
    return fig

# Define the callback for the word cloud
@app.callback(Output('word-cloud', 'figure'),
              Input('dropdown', 'value'))
def update_word_cloud(selected_sources):
    if selected_sources:
        filtered_df = df[df.source.isin(selected_sources)]
    else:
        filtered_df = df
    text = ' '.join(filtered_df.comments)
    wc = wordcloud.WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
    fig = go.Figure(go.Image(z=wc.to_array()))
    fig.update_layout(title='Word cloud of comments')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

# Define the callback for the subset plot
@app.callback(Output('subset-plot', 'figure'),
              Input('dropdown', 'value'))
def update_subset_plot(selected_sources):
    if selected_sources:
        filtered_df = df[df.source.isin(selected_sources)]
    else:
        filtered_df = df
    fig = px.histogram(filtered_df, x='comments', color='sentiment', barmode='group', title='Sentiment by comment')
    return fig

# Run the app
if __name__ == '__main__':
  app.run_server(debug=True)
