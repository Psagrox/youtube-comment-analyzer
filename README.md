# YouTube Comment Analyzer

![YouTube Logo](https://img.icons8.com/?size=100&id=115362&format=png&color=000000)

## Overview

The **YouTube Comment Analyzer** is a web application that allows users to analyze the sentiment of comments on a YouTube video. It provides insights into the overall sentiment (positive, negative, or neutral) and displays the most positive and negative comments. Additionally, it generates a word cloud based on the comments.

This project is built using modern web technologies and integrates with the YouTube Data API to fetch comments and perform sentiment analysis.

## Features

* **Sentiment Analysis**: Analyze the sentiment of YouTube video comments using the VADER sentiment analysis tool
* **Word Cloud**: Generate a word cloud from the comments to visualize the most frequent words
* **Interactive Charts**: Display the polarity of comments in an interactive bar chart
* **Material Design**: A clean and responsive user interface built with Angular Material

## Technologies Used

### Frontend
* **Angular**: A TypeScript-based framework for building dynamic web applications
* **Angular Material**: UI component library for Angular, providing Material Design components
* **Chart.js**: A JavaScript library for creating interactive charts
* **HTML/CSS**: Standard web technologies for structuring and styling the application

### Backend
* **Flask**: A lightweight Python web framework used to build the backend API
* **YouTube Data API**: Fetches comments from YouTube videos
* **VADER Sentiment Analysis**: A tool for sentiment analysis that is specifically attuned to sentiments expressed in social media
* **WordCloud**: A Python library for generating word clouds from text

### Deployment
* **Firebase Hosting**: Used to deploy the frontend application
* **Firebase Functions**: (Optional) Can be used to deploy the backend API if needed

## Getting Started

### Prerequisites

Before you begin, ensure you have installed:
* Node.js
* Python
* Firebase CLI

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/youtube-comment-analyzer.git
cd youtube-comment-analyzer
```

2. **Set Up the Frontend**
```bash
cd frontend
npm install
```

3. **Set Up the Backend**
```bash
cd ../backend
pip install -r requirements.txt
```

4. **Configure Environment Variables**

Create a `.env` file in the backend folder:
```env
YOUTUBE_API_KEY=your_api_key_here
```

## Running the Application

### Start the Backend
```bash
cd backend
python app.py
```
The backend will start on `http://localhost:5000`

### Start the Frontend
```bash
cd frontend
ng serve
```
The frontend will start on `http://localhost:4200`

### Access the Application
Open your browser and navigate to `http://localhost:4200`

## Deployment

### Frontend (Firebase Hosting)

1. Build the Angular application:
```bash
cd frontend
ng build --configuration production
```

2. Deploy to Firebase:
```bash
firebase deploy
```

### Backend
You can deploy the backend using Firebase Functions or other hosting services like Heroku, Render, or AWS.

## Web-live

![Web-live](https://comment-analyzer-2ff73.web.app/)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeatureName`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeatureName`)
5. Open a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

* YouTube Data API for providing access to YouTube comments
* VADER Sentiment Analysis for the sentiment analysis tool
* Angular Material for the beautiful UI components
* Chart.js for the interactive charts

## Contact

* Email: waljaviergalvan@gmail.com
* GitHub: Psagrox

* 
   
