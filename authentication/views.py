# Creating  views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from .models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib import messages
from authentication.models import ClassificationHistory
from django.contrib.auth import logout
#----------------------For user profile section in mav-bar-------------------

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm

#converting mp3 to .wav
# from pydub import AudioSegment


def landing(request):
    return render(request, 'landing.html')

#using the get_user_model function from django.contrib.auth to retrieve the user model specified in  AUTH_USER_MODEL setting.
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                # return render(request, 'signup_success.html')
                return redirect('login') 
            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#Creating view for login page

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()  # Retrieve the first matching user
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def signup_success(request):
    return render(request, 'signup_success.html')

def signup_view(request):
    return render(request, 'signup.html')
    # Your signup logic goes here
    #pass

@login_required
def home_view(request): 
    # Logic for the home view 
    return render(request, 'home.html') 

def about(request):
    return render(request, 'about.html')

#-----------------------------------------------------------------------------------------------------------

# ML MODEL VIEW PART STARTS HERE

from django.shortcuts import render
from django.conf import settings
import os
import joblib
import pickle
from .Metadata import getmetadata
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import time

def generate_bar_graph(genre_probabilities, genres, file_path, lookup_genre_name):
    genre_names = [lookup_genre_name[genre] for genre in genres]  # Get the genre names using lookup_genre_name
    # Create a bar graph of genre percentage distribution
    fig, ax = plt.subplots()  # Create a figure and axes
    ax.bar(genre_names, genre_probabilities)  # Use genre_names instead of genres
    ax.set_title("Genre Percentage Distribution")  # Set the title
    ax.set_xlabel("Genre")  # Set the x-label
    ax.set_ylabel("Percentage")  # Set the y-label
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

def generate_mel_spectrogram(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Compute the mel-spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    # Display the mel-spectrogram
    fig, ax = plt.subplots()  # Create a figure and axes
    img = librosa.display.specshow(mel_spectrogram_db, x_axis='time', y_axis='mel', ax=ax)
    ax.set_title("Mel-Spectrogram")  # Set the title
    fig.colorbar(img, format="%+2.0f dB")  # Add a colorbar
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

def generate_beat_graph(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Detect the beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # Create a beat graph
    fig, ax = plt.subplots()  # Create a figure and axes
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    ax.plot(beat_times, np.ones_like(beat_times), marker='o', markersize=3, linestyle='', color='r')
    # Annotate the BPM count on the graph
    ax.annotate(f'BPM: {int(tempo)}', xy=(0.5, 0.95), xycoords='axes fraction',
                fontsize=12, ha='center', va='center')
    ax.set_title("Beat Graph")  # Set the title
    ax.set_xlabel("Time (seconds)")  # Set the x-label
    ax.set_ylabel("Beat")  # Set the y-label
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

def generate_chord_progression_graph(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Extract the harmonic components using the harmonic-percussive source separation
    harmonic = librosa.effects.harmonic(y)
    
    # Compute the chroma features
    chroma = librosa.feature.chroma_cens(y=harmonic, sr=sr)
    
    # Create a chord progression graph
    fig, ax = plt.subplots()  # Create a figure and axes
    librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', ax=ax, cmap='coolwarm')
    ax.set_title("Chord Progression")  # Set the title
    ax.set_xlabel("Time")  # Set the x-label
    ax.set_ylabel("Chroma")  # Set the y-label
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

#--------------------------Optional--------------------------------

def generate_beat_rhythm_graph(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Detect onsets using the onset detection function
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # Create a beat and rhythm graph
    fig, ax = plt.subplots()  # Create a figure and axes
    ax.vlines(onset_times, 0, 1, color='r', alpha=0.7)  # Plot the onsets as vertical lines
    ax.set_title("Beat and Rhythm")  # Set the title
    ax.set_xlabel("Time (seconds)")  # Set the x-label
    ax.set_ylabel("Intensity")  # Set the y-label
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

#--------------------------Optional--------------------------------

def generate_pitch_frequency_graph(audio_file, file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file)
    
    # Compute the chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    # Create a pitch and frequency graph (pitch contour)
    fig, ax = plt.subplots()  # Create a figure and axes
    librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', ax=ax, cmap='coolwarm')
    ax.set_title("Pitch and Frequency (Pitch Contour)")  # Set the title
    ax.set_xlabel("Time")  # Set the x-label
    ax.set_ylabel("Pitch Class")  # Set the y-label
    plt.tight_layout()  # Adjust the layout
    plt.savefig(file_path)  # Save the figure
    plt.close(fig)  # Close the figure

#--------------------------Optional--------------------------------
# def generate_harmonic_analysis_graph(audio_file, file_path):
#     # Load the audio file
#     y, sr = librosa.load(audio_file)
    
#     # Compute the harmonic spectrum
#     harm_spectrum = librosa.feature.spectral_contrast(y=y, sr=sr)
    
#     # Create a harmonic analysis graph
#     fig, ax = plt.subplots()  # Create a figure and axes
#     ax.imshow(harm_spectrum, aspect='auto', origin='lower', cmap='hot')
#     ax.set_title("Harmonic Analysis")  # Set the title
#     ax.set_xlabel("Time")  # Set the x-label
#     ax.set_ylabel("Frequency Band")  # Set the y-label
#     plt.tight_layout()  # Adjust the layout
#     plt.savefig(file_path)  # Save the figure
#     plt.close(fig)  # Close the figure

#importing time for classification history
import time

def upload(request):
    if request.method == 'POST' and request.FILES['music_file']:
        music_file = request.FILES['music_file']

        # # Check if the uploaded file is an MP3 file
        # if music_file.name.endswith('.mp3'):
        #     # Convert MP3 file to WAV format
        #     audio = AudioSegment.from_mp3(music_file)
        #     file_path = os.path.join(settings.BASE_DIR, 'authentication', 'static', 'temp0.wav')
        #     audio.export(file_path, format='wav')
        # else:
        #     # Save the uploaded file directly to a temporary location
        #     file_path = os.path.join(settings.BASE_DIR, 'authentication', 'static', 'temp.wav')
        #     with open(file_path, 'wb') as f:
        #         for chunk in music_file.chunks():
        #             f.write(chunk)

        # -------------------------------------------------------------
        # Save the uploaded file to a temporary location
        file_path = os.path.join('authentication', 'static', 'temp.wav')
        # file_path = os.path.join(settings.STATIC_ROOT, 'temp.wav')
        with open(file_path, 'wb') as f:
            for chunk in music_file.chunks():
                f.write(chunk)

        #----------------------------------------
        
        # Extract features from the uploaded file
        features = getmetadata(file_path)
        
        # Load the saved ML model
        model_path = os.path.join(settings.BASE_DIR, 'models.pkl')
        model_dict = pickle.load(open(model_path, 'rb'))
        # model = pickle.load(open(model_path, 'rb'))

        scaler = model_dict['norma']
        knn = model_dict['svmp']
        lookup_genre_name = model_dict['lgn']

        # Accuracy dictionary
        genre_accuracy = {
            'blues': 51,
            'classical': 90,
            'country': 62,
            'disco': 57,
            'hiphop': 58,
            'jazz': 73,
            'metal': 76,
            'pop': 71,
            'reggae': 60,
            'rock': 62,
        }

        # Preprocess the features using the loaded scaler
        scaled_features = scaler.transform([features])

         # Make predictions using the loaded model
        genre_probabilities = knn.predict_proba(scaled_features)[0]
        genres = knn.classes_

       # Get the genre with the highest probability
        classified_genre = lookup_genre_name[genres[genre_probabilities.argmax()]]
        timestamp = str(int(time.time()))  # Get the current timestamp as a string
        
        #-------------------------------------------------------------------
        bar_graph_file_name = f'bar_graph.jpg'
        bar_graph_file_path = os.path.join('authentication', 'static', bar_graph_file_name)
        generate_bar_graph(genre_probabilities, genres, bar_graph_file_path, lookup_genre_name)

        # mel_spectrogram_file_name = f'mel_spectrogram_{timestamp}.jpg'  # Append the timestamp to the file name
        mel_spectrogram_file_name = f'mel_spectrogram.jpg'
        mel_spectrogram_file_path = os.path.join('authentication', 'static', mel_spectrogram_file_name)
        generate_mel_spectrogram(file_path, mel_spectrogram_file_path)
        
        # --------------------------------------
        beat_graph_file_name = f'beat_graph.jpg'
        beat_graph_file_path = os.path.join('authentication', 'static', beat_graph_file_name)
        generate_beat_graph(file_path, beat_graph_file_path)

        # --------------------------------------
        chord_progression_file_name = f'chord_progression.jpg'
        chord_progression_file_path = os.path.join('authentication', 'static', chord_progression_file_name)
        generate_chord_progression_graph(file_path, chord_progression_file_path)

        # --------------------------------------
        beat_rhythm_graph_file_name = f'beat_rhythm_graph.jpg'
        beat_rhythm_graph_file_path = os.path.join('authentication', 'static', beat_rhythm_graph_file_name)
        generate_beat_rhythm_graph(file_path, beat_rhythm_graph_file_path)
        #---------------------------------------
        pitch_frequency_graph_file_name = f'pitch_frequency_graph.jpg'
        pitch_frequency_graph_file_path = os.path.join('authentication', 'static', pitch_frequency_graph_file_name)
        generate_pitch_frequency_graph(file_path, pitch_frequency_graph_file_path)
        #-----------------------------------------

        # harmonic_analysis_file_name = f'harmonic_analysis.jpg'
        # harmonic_analysis_file_path = os.path.join('authentication', 'static', harmonic_analysis_file_name)
        # generate_harmonic_analysis_graph(file_path, harmonic_analysis_file_path)

        #-----------------------------------------
      
        # Save the classification result in the database
        history = ClassificationHistory(
            user=request.user,
            music_file_name=music_file.name,
            classified_genre=classified_genre
        )
        history.save()

        return render(request, 'result.html', {
            'classified_genre': classified_genre,
            'accuracy': genre_accuracy.get(classified_genre, None),
            'bar_graph_file_name': bar_graph_file_name,
            'mel_spectrogram_file_name': mel_spectrogram_file_name,
            'beat_graph_file_name': beat_graph_file_name,
            'chord_progression_file_name': chord_progression_file_name,
            # 'beat_rhythm_graph_file_name': beat_rhythm_graph_file_name,
            # 'pitch_frequency_graph_file_name': pitch_frequency_graph_file_name,
            # 'harmonic_analysis_file_name': harmonic_analysis_file_name,
            'bar_graph_file_path': bar_graph_file_path,
            'mel_spectrogram_file_path': mel_spectrogram_file_path,
            'beat_graph_file_path': beat_graph_file_path,
            'chord_progression_file_path': chord_progression_file_path,
            # 'harmonic_analysis_file_path': harmonic_analysis_file_path
            # 'beat_rhythm_graph_file_path': beat_rhythm_graph_file_path,
            # 'pitch_frequency_graph_file_path': pitch_frequency_graph_file_path,
         })
    else:
        return render(request, 'upload.html')
    
#classification history
def history_view(request):
    history = ClassificationHistory.objects.filter(user=request.user).order_by('-classification_date')
    return render(request, 'history.html', {'history': history})

#Resetting History
def reset_history(request):
    if request.method == 'POST':
        # Assuming you have a ForeignKey from ClassificationHistory to User as 'user'
        ClassificationHistory.objects.filter(user=request.user).delete()
        # messages.success(request, 'Classification history has been reset successfully.')
    return redirect('history')  # Redirect back to the classification history page

#Log-out view
def logout_view(request):
    logout(request)
    return redirect('landing')

#User profile section in nav-bar

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'update_password.html', {'form': form})

#For Forget password

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import render

def password_reset(request):
    return auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    )(request)

def password_reset_done(request):
    return auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')(request)

def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    )(request, uidb64=uidb64, token=token)

def password_reset_complete(request):
    return auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')(request)

# #Views for google authentication
# from allauth.account.adapter import DefaultAccountAdapter
# from django.shortcuts import reverse

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#         return reverse('home')  # Replace 'home' with the name of your home view
