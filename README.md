# Content-Based Movie Recommendation System

This project contains a complete end-to-end Content-Based Movie Recommendation System using the TMDB 5000 Movie Dataset.
The entire machine learning pipeline and a simple Streamlit interface generation step have been consolidated into a single Jupyter Notebook.

## Features
- **Data Cleaning & Preprocessing**: Merging datasets, parsing JSON-like features, and engineering a holistic `tags` column.
- **Stemming**: Utilizing `nltk.stem.porter.PorterStemmer` to standardize text.
- **Vectorization**: Transforming text into vectors using `sklearn.feature_extraction.text.CountVectorizer`.
- **Similarity Calculation**: Computing distances between movie vectors using `sklearn.metrics.pairwise.cosine_similarity`.
- **Recommendation Logic**: A custom `recommend()` function built to retrieve the top 5 most similar movies.
- **Model Serialization**: Saving trained models using `pickle`.
- **Streamlit App Generation**: A final cell to generate an `app.py` UI script that uses the TMDB API to fetch movie posters.

## Dataset
This project uses the TMDB 5000 Movie Dataset from Kaggle:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

## Usage
1. Open up `Movie_Recommendation_System.ipynb` in your preferred Jupyter Notebook environment.
2. Run all cells from top to bottom.
3. Once the models are evaluated and saved, the final cell will generate `app.py`.
4. Run the Streamlit application via your terminal:
   ```bash
   pip install streamlit pandas requests
   streamlit run app.py
   ```
