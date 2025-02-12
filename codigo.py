!pip install emoji
!pip install vaderSentiment
!pip install google-api-python-client

# For Fetching Comments
from googleapiclient.discovery import build
# For filtering comments
import re
# For filtering comments with just emojis
import emoji
# Analyze the sentiments of the comment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# For visualization
import matplotlib.pyplot as plt

# Make sure to put in the API KEY as it won't work otherwise
API_KEY = 'AIzaSyAqzHzWTWOZgvMQlfoTGaEhThsQCOrT_3E'# Put in your API Key

youtube = build('youtube', 'v3', developerKey=API_KEY) # initializing Youtube API

# Taking input from the user and slicing for video id
video_id = input('Enter Youtube Video URL: ')[-11:]
print("video id: " + video_id)

# Getting the channelId of the video uploader
video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()

# Splitting the response for channelID
video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']
print("channel id: " + uploader_channel_id)

# Fetch comments
print("Fetching Comments...")
comments = []
nextPageToken = None
while len(comments) < 9999:
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=9999,  # You can fetch up to 100 comments per request
        pageToken=nextPageToken
    )
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        # Check if the comment is not from the video uploader
        if comment['authorChannelId']['value'] != uploader_channel_id:
            comments.append(comment['textDisplay'])
    nextPageToken = response.get('nextPageToken')

    if not nextPageToken:
        break
print(comments)

hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

threshold_ratio = 0.2

relevant_comments = []

# Inside your loop that processes comments
for comment_text in comments:

    comment_text = comment_text.lower().strip()

    emojis = emoji.emoji_count(comment_text)

    # Count text characters (excluding spaces)
    text_characters = len(re.sub(r'\s', '', comment_text))

    if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
        if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
            relevant_comments.append(comment_text)
print(relevant_comments)

f = open("ytcomments.txt", 'w', encoding='utf-8')
for idx, comment in enumerate(relevant_comments):
    f.write(str(comment)+"\n")
f.close()
print("Comments stored successfully!")

def sentiment_scores(comment, polarity):

  # Creating a SentimentIntensityAnalyzer object.
  sentiment_object = SentimentIntensityAnalyzer()

  sentiment_dict = sentiment_object.polarity_scores(comment)
  polarity.append(sentiment_dict['compound'])
  print(sentiment_dict)

  return polarity


polarity = []
positive_comments = []
negative_comments = []
neutral_comments = []

f = open("ytcomments.txt", 'r', encoding='`utf-8')
print("Reading Comments...")
comments = f.readlines()
f.close()
print("Analysing Comments...")
for index, items in enumerate(comments):
    polarity = sentiment_scores(items, polarity)


    if polarity[-1] > 0.05:
        positive_comments.append(items)
    elif polarity[-1] < -0.05:
        negative_comments.append(items)
    else:
        neutral_comments.append(items)

print(polarity)

avg_polarity = sum(polarity)/len(polarity)
print("Average Polarity:", avg_polarity)
if avg_polarity>0.05:
    print("The Video has got a Positive response")
elif avg_polarity<-0.05:
    print("The Video has got a Negative response")
else:
    print("The Video has got a Neutral response")

print("The comment with most positive sentiment:", comments[polarity.index(max(polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]))
print("The comment with most negative sentiment:", comments[polarity.index(min(polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]))

positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)

# labels and data for Bar chart
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

# Creating bar chart
plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

# Adding labels and title to the plot
plt.xlabel('Sentiment')
plt.ylabel('Comment Count')
plt.title('Sentiment Analysis of Comments')

# Displaying the chart
plt.show()

from wordcloud import WordCloud, STOPWORDS
import nltk
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import requests
import re #limpieza de texto
import unicodedata #caracteres especiales del idioma
import datetime
import nltk #procesamiento de lenguaje natural
from nltk.corpus import stopwords #analisis de palabras irrelevantes
nltk.download('stopwords')

result_string = ''.join(comments)
#print(result_string)  # Output: a b c d

from nltk.corpus import stopwords
stoplist = set(stopwords.words("spanish"))

# Términos adicionales que deseas agregar
terminos_a_agregar = ["br", "quot", "xd",'si','quote','video','día','dia','b','q']

# Agregar los nuevos términos a la lista de stopwords
stoplist.update(terminos_a_agregar)


#print(result_string)
wordcloud = WordCloud(width = 1300, height = 800,
                background_color ='white',
                colormap = 'viridis',
                stopwords = stoplist, # Opcional: eliminar palabras comunes
                min_font_size = 10).generate(result_string)

plt.figure(figsize = (8, 8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()
