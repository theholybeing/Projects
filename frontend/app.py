import streamlit as st

st.set_page_config(page_title="📚 Book Recommender", layout="centered")

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

@st.cache_data
def load_data():
    books = pd.read_csv('data/Books.csv', low_memory=False)
    books = books.rename(columns={
        'Book-Title': 'title',
        'Book-Author': 'authors'
    })
    books['description'] = books['Publisher'].fillna('')
    books['title_lower'] = books['title'].str.lower()
    books = books.drop_duplicates(subset='title_lower')
    books = books.drop(columns='title_lower')
    books['combined'] = books['title'].fillna('') + ' ' + books['authors'].fillna('') + ' ' + books['description'].fillna('')
    return books

# Load the data
books = load_data()

# TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books['combined'])

# Nearest Neighbors
nn_model = NearestNeighbors(metric='cosine', algorithm='brute')
nn_model.fit(tfidf_matrix)


books = books.reset_index()
indices = pd.Series(books.index, index=books['title'].str.lower())

# Recommender function
def recommend_books(title, n=5):
    title = title.lower()
    if title not in indices:
        return ["❌ Book not found."]
    idx = indices[title]
    distances, indices_nn = nn_model.kneighbors(tfidf_matrix[idx], n_neighbors=n + 1)
    rec_indices = indices_nn.flatten()[1:]
    return books['title'].iloc[rec_indices].tolist()

st.title("📚 Book Recommendation System")
st.markdown("Get suggestions based on your favorite book.")

book_titles = books['title'].dropna().unique().tolist()
user_input = st.selectbox("Select a book title:", sorted(book_titles))

if st.button("Recommend"):
    with st.spinner("Finding similar books..."):
        recommendations = recommend_books(user_input)
        st.subheader("📖 Recommendations:")
        for i, book in enumerate(recommendations, start=1):
            st.markdown(f"{i}. **{book}**")
