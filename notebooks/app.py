import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from pathlib import Path
import os
import gdown

BASE_DIR = Path(__file__).resolve().parent

FOLDER_URL = "https://drive.google.com/drive/folders/1OD1In1PqYsqGKwXDOZI3NlNd5BTpmhoZ?usp=sharing"

if not (BASE_DIR/"data").exists():
    gdown.download_folder(
        url=FOLDER_URL,
        output=str(BASE_DIR),
        quiet=False,
        remaining_ok=True
    )

print("Current directory:", BASE_DIR)
print("Files:", os.listdir(BASE_DIR))

# Check both possible folder structures
if (BASE_DIR / "data" / "cleaned_data.csv").exists():
    cleaned_data_path = BASE_DIR / "data" / "cleaned_data.csv"
    transformed_data_path = BASE_DIR / "data" / "transformed_data.npz"
elif (BASE_DIR / "data" / "data" / "cleaned_data.csv").exists():
    cleaned_data_path = BASE_DIR / "data" / "data" / "cleaned_data.csv"
    transformed_data_path = BASE_DIR / "data" / "data" / "transformed_data.npz"
else:
    raise FileNotFoundError("Data folder was not downloaded correctly.")

# load the data
data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data = load_npz(transformed_data_path)

# Title
st.title('Welcome to the Spotify Song Recommender!')

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)

# lowercase the input
song_name = song_name.lower()

# k recommndations
k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)

# Button
if st.button('Get Recommendations'):
    if (data["name"] == song_name).any():
        st.write('Recommendations for', f"**{song_name}**")
        recommendations = recommend(song_name,data,transformed_data,k)
            
        # Display Recommendations
        for ind , recommendation in recommendations.iterrows():
            song_name = recommendation['name'].title()
            artist_name = recommendation['artist'].title()
                
            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(f"#### **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            elif ind == 1:   
                st.markdown("### Next Up 🎵")
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            else:
                st.markdown(f"#### {ind}. **{song_name}** by **{artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
    else:
        st.write(f"Sorry, we couldn't find {song_name} in our database. Please try another song.")
            