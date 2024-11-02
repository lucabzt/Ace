import tkinter as tk
import pygame
import cv2
import numpy as np
from PIL import Image, ImageTk

# Initialize Pygame for audio playback
pygame.mixer.init()

# Create main application window
root = tk.Tk()
root.title("Spade Audio Visualizer")
root.attributes('-fullscreen', True)  # Set window to fullscreen
root.configure(bg='#2f2e31')  # Set background to dark

# Create a canvas for the video playback
canvas = tk.Canvas(root, bg='#2f2e31', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Load the video and initialize OpenCV
video_path = "/Users/sebastianrogg/PycharmProjects/Spade/images/video.mp4"  # Replace with the path to your video file
video_capture = cv2.VideoCapture(video_path)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Function to show the first frame of the video
def show_first_frame():
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Go to the first frame
    ret, frame = video_capture.read()  # Read the first frame
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        img = Image.fromarray(frame)  # Create an Image object
        img = img.resize((screen_width, screen_height), Image.LANCZOS)  # Resize to full screen
        img = ImageTk.PhotoImage(img)  # Convert to PhotoImage
        canvas.create_image(0, 0, anchor=tk.NW, image=img)  # Display it on canvas
        canvas.image = img  # Keep a reference to avoid garbage collection

# Function to play video on the canvas
def play_video():
    if pygame.mixer.music.get_busy():  # Check if audio is still playing
        ret, frame = video_capture.read()  # Read the next frame
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            img = Image.fromarray(frame)  # Create an Image object
            img = img.resize((screen_width, screen_height), Image.LANCZOS)  # Resize to full screen
            img = ImageTk.PhotoImage(img)  # Convert to PhotoImage

            # Display the image on the canvas
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.image = img  # Keep a reference to avoid garbage collection

            # Schedule the next frame, adjust the delay based on the video frame rate
            canvas.after(33, play_video)  # Call this function again after ~33 ms (~30 FPS)
        else:
            # Video has ended; reset to the first frame and continue playing
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            play_video()  # Continue playing video
    else:
        # Stop video playback when audio ends
        show_first_frame()  # Reset to the first frame

# Function to play audio and start video
def play_audio():
    audio_path = "/Users/sebastianrogg/PycharmProjects/Spade/sounds/Phrases/Spade_Initiation.mp3"  # Audio file path
    pygame.mixer.music.load(audio_path)  # Load audio file
    pygame.mixer.music.play()  # Play audio
    play_video()  # Start playing video

# Create play button
play_button = tk.Button(root, text="Play", command=play_audio, bg='black', fg='white', font=("Arial", 24))

# Place the button at the bottom of the canvas
button_y_position = screen_height - 50  # 50 pixels from the bottom
canvas.create_window(screen_width // 2, button_y_position, window=play_button)

# Show the first frame initially
show_first_frame()

# Start the main event loop
root.mainloop()

# Clean up resources on close
video_capture.release()
pygame.mixer.quit()
