# Music Recommendation System

This repository contains a **Music Recommendation System** that integrates Spotify's API and Genius API to provide personalized music recommendations based on song lyrics and user playlists. The application is built using **Streamlit** for the front end and uses **machine learning models** for generating recommendations.

---

## Features

- **Spotify Integration**: Allows users to log in with their Spotify account, fetch their playlists, and recommend similar tracks.
- **Lyrics Analysis**: Scrapes and analyzes lyrics using Genius API for better recommendation accuracy.
- **Custom Recommendations**: Generates song recommendations using **TF-IDF vectorization** and **cosine similarity** on the lyrics.
- **Hover Effects**: Adds an interactive hover and zoom-in effect for song posters and names.
- **Scalable Backend**: Modular design to support additional features in the future.

---

## Technologies Used

### Backend Technologies
- **Python**: Core programming language.
- **Spotipy**: Spotify API integration for fetching user playlists and track details.
- **Genius API**: For fetching song lyrics.
- **pandas**: Data manipulation and cleaning.
- **nltk**: Tokenization and stemming for natural language processing.
- **scikit-learn**: TF-IDF vectorization and cosine similarity calculations.
- **langdetect**: Detects non-English lyrics.

### Frontend Technologies
- **Streamlit**: For creating an interactive web interface.
- **HTML/CSS**: Embedded in Streamlit for enhanced styling (hover effects, navbar, etc.).

---

## Setup Instructions

Follow these steps to set up and run the Music Recommendation System on your local machine:

### 1. Clone the Repository
```bash
$ git clone https://github.com/Om1513/MusicRecommendationSystem.git
$ cd music-recommendation-system
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed. Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory with the following keys:

```env
SPOTIPY_CLIENT_ID=<your-spotify-client-id>
SPOTIPY_CLIENT_SECRET=<your-spotify-client-secret>
SPOTIPY_REDIRECT_URI=<your-redirect-uri>
GENIUS_ACCESS_TOKEN=<your-genius-access-token>
```

To obtain these credentials:
- **Spotify API**: [Create a Spotify Developer App](https://developer.spotify.com/dashboard/).
- **Genius API**: [Get an API Key](https://genius.com/api-clients).

### 4. Prepare the Dataset (Optional)
If you wish to use your own dataset, ensure it is a CSV file with the following structure:

| song       | artist         | lyrics          |
|------------|----------------|-----------------|
| Song Name  | Artist Name    | Song Lyrics     |

Place the file in the root directory and update the file path in the `app.py` script.

### 5. Run the Application
Run the Streamlit application:

```bash
$ streamlit run app.py
```

The application will be accessible in your browser at `http://localhost:8501`.

---

## How It Works

1. **Spotify Login**: Users log in with their Spotify credentials to fetch playlists.
2. **Lyrics Scraping**: The app retrieves song lyrics from Genius for playlist songs.
3. **Preprocessing**:
   - Removes non-English lyrics.
   - Tokenizes and stems lyrics using NLTK.
4. **Recommendation Model**:
   - Uses TF-IDF vectorization to convert lyrics into numerical vectors.
   - Calculates cosine similarity to find similar songs.
5. **Interactive UI**:
   - Displays recommended songs with hover effects for posters and names.

---

## Folder Structure

```plaintext
Music-Recommendation-System/
├── app.py                    # Main application script
├── requirements.txt          # Required dependencies
├── dataset.csv               # Initial dataset (optional)
├── similarity.pkl            # Precomputed similarity matrix
├── README.md                 # Project documentation
├── .env                      # Environment variables
```

---

## Customization

### Using a New Dataset
Replace the `playlist_songs_with_lyrics.csv` file with your own dataset and update the file path in `app.py`. Run the following function to generate a new similarity matrix:

```python
from app import generate_similarity_pickle

generate_similarity_pickle('your_dataset.csv', 'your_similarity.pkl')
```

Update the `similarity.pkl` file in your app.

### Adding Features
You can enhance the app by adding:
- **Genre-Based Recommendations**: Use Spotify's track features like tempo, danceability, and energy.
- **User Preferences**: Save user preferences for personalized results.

---

## Known Issues

1. **Rate Limits**: Both Spotify and Genius APIs have rate limits. If you hit the limit, wait for some time before retrying.
2. **Incomplete Data**: Some songs may not have lyrics available on Genius, which might lead to exclusions.

---

## Contribution Guidelines

We welcome contributions! If you'd like to improve the project, please fork the repository and create a pull request.

### Steps to Contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Added new feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request in the main repository.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

If you have any questions or suggestions, feel free to reach out at:
- **Email**: [oss9762@nyu.edu](mailto:oss9762@nyu.edu)
- **GitHub**: [https://github.com/Om1513](https://github.com/Om1513)

