import matplotlib.pyplot as plt
import librosa.display
import numpy as np


def generate_bar_graph(genre_probabilities, genres, file_path, lookup_genre_name):
    genre_names = [lookup_genre_name[genre] for genre in genres]  # Get the genre names using lookup_genre_name
    # Create a bar graph of genre percentage distribution
    plt.figure()
    plt.title("Genre Percentage Distribution")
    plt.bar(genre_names, genre_probabilities)  # Use genre_names instead of genres
    plt.xlabel("Genre")
    plt.ylabel("Percentage")
    plt.xticks(rotation=45)
    plt.savefig(file_path)
    plt.close()

def generate_mel_spectrogram(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Compute the mel-spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Display the mel-spectrogram
    plt.figure()
    librosa.display.specshow(mel_spectrogram_db, x_axis='time', y_axis='mel')
    plt.title("Mel-Spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.savefig(file_path)
    plt.close()
