import base64
from io import BytesIO
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from matplotlib import pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import emoji
import base64
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

app = Flask(__name__)
CORS(app)  # Esto permite las peticiones desde tu frontend de Angular


API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.route("/")
def home():
    return "¡Hola, Docker y Flask están funcionando correctamente!"

def extract_video_id(url):
    # Extraer el ID del video de diferentes formatos de URL de YouTube
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
        r"(?:shorts\/)([0-9A-Za-z_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def filter_comments(comments, uploader_channel_id):
    hyperlink_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    threshold_ratio = 0.2
    relevant_comments = []

    for comment in comments:
        comment_text = comment.lower().strip()
        emojis = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r"\s", "", comment_text))

        if any(
            char.isalnum() for char in comment_text
        ) and not hyperlink_pattern.search(comment_text):
            if (
                emojis == 0
                or (text_characters / (text_characters + emojis)) > threshold_ratio
            ):
                relevant_comments.append(comment_text)

    return relevant_comments


def analyze_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    polarities = []
    comments_with_polarity = []

    for comment in comments:
        sentiment_dict = analyzer.polarity_scores(comment)
        polarity = sentiment_dict["compound"]
        polarities.append(polarity)
        comments_with_polarity.append({
            "text": comment,
            "polarity": polarity
        })

    if not polarities:
        return {
            "avg_polarity": 0,
            "sentiment": "neutral",
            "most_positive_comment": "",
            "most_negative_comment": "",
            "comments": []
        }

    avg_polarity = sum(polarities) / len(polarities)

    sentiment = "neutral"
    if avg_polarity > 0.05:
        sentiment = "positive"
    elif avg_polarity < -0.05:
        sentiment = "negative"

    max_polarity_index = polarities.index(max(polarities))
    min_polarity_index = polarities.index(min(polarities))

    return {
        "avg_polarity": round(avg_polarity, 3),
        "sentiment": sentiment,
        "most_positive_comment": comments[max_polarity_index],
        "most_negative_comment": comments[min_polarity_index],
        "comments": comments_with_polarity  # Incluye los comentarios con su polaridad
    }

def generate_wordcloud(comments):
    # Unir todos los comentarios en un solo texto
    text = " ".join(comments)

    # Configurar las stopwords en español
    stoplist = set(stopwords.words("spanish"))

    # Términos adicionales que deseas agregar
    terminos_a_agregar = [
        "br",
        "quot",
        "xd",
        "si",
        "quote",
        "video",
        "día",
        "dia",
        "b",
        "q",
    ]

    # Agregar los nuevos términos a la lista de stopwords
    stoplist.update(terminos_a_agregar)

    # Generar la nube de palabras
    wordcloud = WordCloud(
        width=1300,
        height=800,
        background_color="white",
        colormap="viridis",
        stopwords=stoplist,  # Eliminar palabras comunes
        min_font_size=10,
    ).generate(text)

    # Convertir la imagen a base64
    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return image_base64


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        print("Request received")
        data = request.json
        if not data:
            print("No data")
            return jsonify({'error': 'No data provided'}), 400
        print(f"Received data: {data}")  # Esto imprimirá el JSON recibido

        video_url = data.get("videoUrl")

        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        youtube = build("youtube", "v3", developerKey=API_KEY)

        # Obtener ID del canal del uploader
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()

        uploader_channel_id = video_response["items"][0]["snippet"]["channelId"]

        # Recolectar comentarios
        comments = []
        nextPageToken = None

        while len(comments) < 100:  # Limitamos a 100 comentarios para este ejemplo
            requests = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken,
            )
            response = requests.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                if comment["authorChannelId"]["value"] != uploader_channel_id:
                    comments.append(comment["textDisplay"])

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break

        # Filtrar y analizar comentarios
        filtered_comments = filter_comments(comments, uploader_channel_id)
        analysis_result = analyze_sentiment(filtered_comments)

        # Generar la nube de palabras
        wordcloud_image = generate_wordcloud(filtered_comments)

        # Agregar la nube de palabras al resultado
        analysis_result["wordcloud"] = wordcloud_image

        return jsonify(analysis_result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Error analyzing comments: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
