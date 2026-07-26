import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from pathlib import Path
import os
import zipfile
import gdown

import sys
import subprocess

print("Python:", sys.version)

try:
    import joblib
    print("Joblib version:", joblib.__version__)
except Exception as e:
    print("Joblib import failed:", e)

print(subprocess.run(["pip", "list"], capture_output=True, text=True).stdout)

BASE_DIR = Path(__file__).resolve().parent

# Google Drive File ID of data.zip
FILE_ID = "1ikeYE3KvatvydZ6AC09rHbciZofKNRsm"

ZIP_PATH = BASE_DIR / "data.zip"

# Download and extract only if the data folder doesn't exist
if not (BASE_DIR / "data").exists():

    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        str(ZIP_PATH),
        quiet=False
    )

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(BASE_DIR)

print("Current directory:", BASE_DIR)
print("Files:", os.listdir(BASE_DIR))

# Detect folder structure automatically
if (BASE_DIR / "data" / "cleaned_data.csv").exists():
    cleaned_data_path = BASE_DIR / "data" / "cleaned_data.csv"
    transformed_data_path = BASE_DIR / "data" / "transformed_data.npz"

elif (BASE_DIR / "data" / "data" / "cleaned_data.csv").exists():
    cleaned_data_path = BASE_DIR / "data" / "data" / "cleaned_data.csv"
    transformed_data_path = BASE_DIR / "data" / "data" / "transformed_data.npz"

else:
    raise FileNotFoundError(
        f"""
Data folder was not extracted correctly.

BASE_DIR = {BASE_DIR}

Folders = {os.listdir(BASE_DIR)}
"""
    )

# Load data
data = pd.read_csv(cleaned_data_path)

# Load transformed data
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
            