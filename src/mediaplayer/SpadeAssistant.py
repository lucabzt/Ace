import tkinter as tk
import pygame
import random
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL for image handling

# Initialize Pygame for audio playback
pygame.mixer.init()

# Create main application window
root = tk.Tk()
root.title("Spade Audio Visualizer")
root.attributes('-fullscreen', True)  # Set window to fullscreen
root.configure(bg='#2f2e31')  # Set background to dark

# Create a canvas for the logo and audio bars that takes up the whole screen
canvas = tk.Canvas(root, bg='#2f2e31', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Create a list to store the audio bars
bars = []
bar_width = 8  # Set bar width to 10 for larger bars
vertical_center = root.winfo_screenheight() // 2  # Calculate vertical center of the canvas

# Load the spade logo image
spade_image_path = "/Users/sebastianrogg/PycharmProjects/Spade/images/spade_assistant_1920x1080.png"  # Path to your spade logo image
spade_image = Image.open(spade_image_path)
# Resize the image to be much larger to fit fullscreen
spade_image = spade_image.resize((root.winfo_screenwidth(), int(root.winfo_screenwidth()*0.5)), Image.LANCZOS)  # Resize the image
spade_logo = ImageTk.PhotoImage(spade_image)

# Function to draw the spade logo image
def draw_spade_logo(center_x, center_y):
    # Draw the spade logo on the canvas
    canvas.create_image(center_x, center_y+200, image=spade_logo)

# Function to create audio bars
def create_bars():
    global bars, vertical_center  # Ensure we modify the global bars list and access vertical_center
    bars.clear()  # Clear previous bars if they exist
    num_bars = 30  # Number of bars
    canvas.delete("bars")  # Clear previous bars from canvas

    # Center position for the bars
    center_x = root.winfo_screenwidth() // 2
    start_x = center_x - (num_bars * 15)  # Adjust starting position based on number of bars

    for i in range(num_bars):
        x_position = start_x + (i * 30)  # Adjust spacing between bars
        # Create initial bar with height 0 at the baseline
        bar = canvas.create_rectangle(
            x_position, vertical_center,  # Set baseline to vertical center
            x_position + bar_width, vertical_center,
            fill="white", outline="", tags="bars")  # Changed fill color to black
        bars.append(bar)

    # Draw the Poker Spade logo in the center
    draw_spade_logo(center_x, vertical_center - 200)  # Adjust logo position if necessary

# Function to animate audio bars with a smooth gradient height
def animate_bars():
    if pygame.mixer.music.get_busy():
        center_index = len(bars) // 2  # Find the center bar index
        max_height = 150  # Maximum height for the bars

        for i, bar in enumerate(bars):
            # Calculate height based on distance from the center
            distance_from_center = abs(center_index - i)
            height_factor = max(0, 1 - (distance_from_center / center_index))  # Increase height towards center

            # Calculate the height of the bar
            up_height = int(max_height * height_factor * random.uniform(0.5, 1))  # Randomize height
            down_height = int(max_height * height_factor * random.uniform(0.5, 1))  # Randomize downward height

            # Update bar to extend from the center line
            canvas.coords(bar,
                          canvas.coords(bar)[0],
                          vertical_center - up_height,  # Upward height from the vertical center
                          canvas.coords(bar)[0] + bar_width,
                          vertical_center + down_height)  # Downward height from the vertical center
        canvas.after(100, animate_bars)  # Repeat every 100ms
    else:
        # Return all bars to baseline after audio ends
        for bar in bars:
            canvas.coords(bar,
                          canvas.coords(bar)[0],
                          vertical_center,  # Reset to vertical center
                          canvas.coords(bar)[0] + bar_width,
                          vertical_center)  # Bar width is still 10

# Function to play audio and start animation
def play_audio():
    pygame.mixer.music.load(
        "/Users/sebastianrogg/PycharmProjects/Spade/sounds/LUSTIG/Checks like a pussy.mp3")  # Audio file path
    pygame.mixer.music.play()
    animate_bars()  # Start animating bars

# Create play button
play_button = tk.Button(root, text="Play", command=lambda: [create_bars(), play_audio()], bg='black', fg='white',
                        font=("Arial", 24))
play_button.pack(pady=20)

# Start the main event loop
root.mainloop()
