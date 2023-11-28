import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageSequence
import os

from backend import Backend



def process_input(input_value):
    
    
    Backend(input_value)
    
    show_gif('Vanni_script\\Gifoutput\\output.gif')
    
    # result = model.predict(input_value)
    # print("Result:", result)

def toggle_animation():
    global gif_running, frame_counter, gif_frames, total_frames
    if not gif_running or frame_counter == total_frames:
        frame_counter = 0  # Reset frame counter when starting a new cycle
        gif_frames = iter([ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(original_image)])
    gif_running = not gif_running
    if gif_running:
        animate_gif()

def animate_gif():
    global gif_frames, frame_counter, total_frames,gif_running
    if gif_running:
        try:
            next_frame = next(gif_frames)
            label_gif.configure(image=next_frame)
            app.after(980, animate_gif)  # Adjust the delay (in milliseconds) as needed
            frame_counter += 1
            if frame_counter == total_frames:  # Stop after one cycle
                gif_running = False
        except StopIteration:
            pass
def show_gif(path):
    global gif_path, default_gif, label_gif, gif_frames, total_frames, frame_counter, original_image
    gif_path = path

    if gif_path and os.path.exists(gif_path):
        # Load the selected GIF file
        original_image = Image.open(gif_path)
        # Resize the image to fit within a 300x225 box while preserving its aspect ratio
        original_image.thumbnail((300, 225))
        default_gif = ImageTk.PhotoImage(original_image)

        # Display the resized GIF
        label_gif.configure(image=default_gif)
        label_gif.image = default_gif  # Keep a reference to avoid garbage collection
        label_gif.pack(pady=10)

        # Initialize gif_frames with frames from the GIF
        gif_frames = iter([ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(original_image)])
        total_frames = len(list(ImageSequence.Iterator(original_image)))
        frame_counter = 0

    else:
        show_no_gif_message()
        
        
def browse_gif():
    global gif_path, default_gif, label_gif, gif_frames, total_frames, frame_counter, original_image
    gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])

    if gif_path and os.path.exists(gif_path):
        # Load the selected GIF file
        original_image = Image.open(gif_path)
        # Resize the image to fit within a 300x225 box while preserving its aspect ratio
        original_image.thumbnail((300, 225))
        default_gif = ImageTk.PhotoImage(original_image)

        # Display the resized GIF
        label_gif.configure(image=default_gif)
        label_gif.image = default_gif  # Keep a reference to avoid garbage collection
        label_gif.pack(pady=10)

        # Initialize gif_frames with frames from the GIF
        gif_frames = iter([ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(original_image)])
        total_frames = len(list(ImageSequence.Iterator(original_image)))
        frame_counter = 0

    else:
        show_no_gif_message()

def show_no_gif_message():
    # Show a message if no valid GIF is selected
    label_no_gif = ttk.Label(app, text="No valid GIF selected!")
    label_no_gif.pack(pady=10)

# Tkinter setup
app = tk.Tk()
app.title("Vaani App")

# Set the initial window size (width x height)
app.geometry("720x720")  # Adjust the dimensions as needed

# Material Design Colors
primary_color = "#2196F3"  # Material Blue
secondary_color = "#FFC107"  # Material Yellow
background_color = "#FFFFFF"  # Material White
text_color = "#212121"  # Material Dark

# Configure Style
style = ttk.Style()
style.theme_use('clam')  # Change to 'clam' theme
style.configure('TLabel', background=background_color, foreground=text_color)
style.configure('TButton', background=primary_color, foreground=text_color)
style.map('TButton', background=[('active', secondary_color)])

# Title "Vaani" with colorful, big, italic font
title_frame = ttk.Frame(app)
title_frame.pack(pady=20)
title_label = ttk.Label(title_frame, text="Vaani", font=("Helvetica", 70, "bold"), foreground="#212121",background=app.cget("bg"))
title_label.pack()
underline = ttk.Separator(app, orient="horizontal")
underline.pack(fill="x")

# Create and place widgets
label = ttk.Label(app, text="Enter prompt:",font=("Helvetica", 20, "bold"),background=app.cget("bg"))
label.pack(pady=10)

entry = ttk.Entry(app)
entry.pack(pady=10)

# Submit Button
def submit_data():
    input_value = entry.get()
    process_input(input_value)

button_submit = ttk.Button(app, text="Submit", command=submit_data)
button_submit.pack(pady=10)

# Browse Button
button_browse = ttk.Button(app, text="Browse GIF", command=browse_gif)
button_browse.pack(pady=10)



# Declare label_gif, gif_running, and gif_frames outside the if block
label_gif = ttk.Label(app)
gif_running = False  # Initialize gif_running
gif_frames = iter([tk.PhotoImage()])  # Initialize with placeholder
total_frames = 0
frame_counter = 0
original_image = None

# Play/Pause Button
button_play_pause = ttk.Button(app, text="Play/Pause", command=toggle_animation)
button_play_pause.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()






