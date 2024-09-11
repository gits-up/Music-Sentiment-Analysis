# !pip install snscrape transformers pandas plotly scikit-learn
# !pip install praw pandas textblob matplotlib dash plotly
# !pip install dash dash-core-components dash-html-components plotly pyngrok
# !pip install --upgrade pyngrok

import praw
import pandas as pd
from textblob import TextBlob
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

reddit = praw.Reddit(
    client_id='DiK91scTVA47kQa7hYawKg', 
    client_secret='Gqsp16iJ9LTkdp5PvtJILUWtVUt4Wg', 
    user_agent='MusicSentimentApp'
)

# Function to fetch Reddit posts
def fetch_reddit_data(subreddit_name, query, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for submission in subreddit.search(query, limit=limit):
        posts.append([submission.title, submission.selftext, submission.created_utc])

    # Convert to DataFrame
    df = pd.DataFrame(posts, columns=['Title', 'Body', 'Created'])
    return df

# Function to categorize sentiment
def categorize_sentiment(polarity):
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Function to perform sentiment analysis
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Fetch data and perform sentiment analysis
df = fetch_reddit_data('music', 'new music release', limit=100)
df['Sentiment_Title'] = df['Title'].apply(get_sentiment)
df['Sentiment_Body'] = df['Body'].apply(get_sentiment)
df['Sentiment_Title_Category'] = df['Sentiment_Title'].apply(categorize_sentiment)
df['Sentiment_Body_Category'] = df['Sentiment_Body'].apply(categorize_sentiment)
df['Created'] = pd.to_datetime(df['Created'], unit='s')
df['Date'] = df['Created'].dt.date

# Define the interactive dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sentiment Analysis of New Music Releases"),
    dcc.Dropdown(
        id='sentiment-dropdown',
        options=[
            {'label': 'Title Sentiment', 'value': 'Sentiment_Title_Category'},
            {'label': 'Body Sentiment', 'value': 'Sentiment_Body_Category'}
        ],
        value='Sentiment_Title_Category'
    ),
    dcc.Graph(id='sentiment-graph')
])

@app.callback(
    Output('sentiment-graph', 'figure'),
    [Input('sentiment-dropdown', 'value')]
)
def update_graph(sentiment_type):
    fig = px.histogram(df, x='Date', color=sentiment_type, title=f'Sentiment Distribution Over Time ({sentiment_type})')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)




from pyngrok import ngrok

ngrok.set_auth_token('2lueFFlAg0j2KJLCMYNd7BGovrW_6ToFU2GAAM5k1aiypu5L1')

public_url = ngrok.connect(8050)
print('Public URL:', public_url)
