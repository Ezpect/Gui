import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Scale, HORIZONTAL
import cv2
from PIL import Image, ImageTk
import numpy as np
import subprocess

# Function to load an image or start video streaming
def load_image_or_stream():
    global cap, stream_button
    if cap is None:
        cap = cv2.VideoCapture(0)  # Use webcam, change to file path for video file
        stream_button.config(text="Stop Streaming")
        process_video_stream()
    else:
        cap.release()
        cap = None
        stream_button.config(text="Start Streaming")
        # Clear labels when streaming is stopped
        img_label.config(image="")
        sobel_label.config(image="")
        canny_label.config(image="")
        threshold_label.config(image="")
        adaptive_label.config(image="")

# Function to process video stream
def process_video_stream():
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            display_image(frame, img_label)
            apply_sobel(frame)
            apply_canny(frame)
            apply_global_threshold(frame)
            apply_adaptive_threshold(frame)
            # Repeat the process for the next frame
            img_label.after(10, process_video_stream)

def display_image(image, label):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for display
    image = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image)
    label.config(image=image_tk)
    label.image = image_tk

# Function to load an image
def load_image():
    global original_image, img_label
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB) # Convert to RGB for display
        display_image(original_image, img_label)

# Function to apply the Sobel operator
def apply_sobel(frame):
    global original_image, sobel_label
    if original_image is None:
        messagebox.showerror("Error", "Please load an image first")
        return
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = cv2.magnitude(sobelx, sobely)
    sobel_combined = np.uint8(sobel_combined)
    display_image(sobel_combined, sobel_label)

# Function to apply the Canny edge detector
def apply_canny(frame):
    global original_image, canny_label
    if original_image is None:
        messagebox.showerror("Error", "Please load an image first")
        return
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    threshold1 = threshold1_slider.get()
    threshold2 = threshold2_slider.get()
    edges = cv2.Canny(gray_image, threshold1, threshold2)
    display_image(edges, canny_label)

# Function to apply global thresholding
def apply_global_threshold(frame):
    global original_image, threshold_label
    if original_image is None:
        messagebox.showerror("Error", "Please load an image first")
        return
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    threshold_value = threshold_slider.get()
    _, thresholded = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    display_image(thresholded, threshold_label)

# Function to apply adaptive thresholding
def apply_adaptive_threshold(frame):
    global original_image, adaptive_label
    if original_image is None:
        messagebox.showerror("Error", "Please load an image first")
        return
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)
    block_size = block_size_slider.get()
    C_value = C_slider.get()
    adaptive_thresholded = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C_value)
    display_image(adaptive_thresholded, adaptive_label)

# Function to execute git commands
def execute_git_commands():
    try:
        subprocess.check_call(["git", "remote", "add", "origin", "https://github.com/Ezpect/Gui.git"])
        subprocess.check_call(["git", "branch", "-M", "main"])
        subprocess.check_call(["git", "push", "-u", "origin", "main"])
        messagebox.showinfo("Success", "Git commands executed successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while executing git commands: {e}")

# Create the main window
root = tk.Tk()
root.title("Image Processing Techniques")
root.geometry("1200x800")

# Create a frame for the original image
frame_original = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_original.pack(side=tk.LEFT, padx=10, pady=10)
Label(frame_original, text="Original Image").pack()
img_label = Label(frame_original)
img_label.pack()

# Create frames for displaying the results of different techniques
frame_sobel = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_sobel.pack(side=tk.LEFT, padx=10, pady=10)
Label(frame_sobel, text="Sobel Edge Detection").pack()
sobel_label = Label(frame_sobel)
sobel_label.pack()

frame_canny = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_canny.pack(side=tk.LEFT, padx=10, pady=10)
Label(frame_canny, text="Canny Edge Detection").pack()
canny_label = Label(frame_canny)
canny_label.pack()

frame_threshold = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_threshold.pack(side=tk.LEFT, padx=10, pady=10)
Label(frame_threshold, text="Global Thresholding").pack()
threshold_label = Label(frame_threshold)
threshold_label.pack()

frame_adaptive = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame_adaptive.pack(side=tk.LEFT, padx=10, pady=10)
Label(frame_adaptive, text="Adaptive Thresholding").pack()
adaptive_label = Label(frame_adaptive)
adaptive_label.pack()

# Create a button to start/stop video streaming
stream_button = Button(root, text="Webcam", command=load_image_or_stream)
stream_button.pack(side=tk.TOP, pady=10)

# Create a button to load an image
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(side=tk.TOP, pady=10)

# Create sliders for Canny edge detection parameters
threshold1_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Threshold1")
threshold1_slider.set(100)
threshold1_slider.pack(side=tk.TOP, pady=10)

threshold2_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Threshold2")
threshold2_slider.set(200)
threshold2_slider.pack(side=tk.TOP, pady=10)

# Create a button to apply Sobel edge detection
sobel_button = Button(root, text="Apply Sobel", command=apply_sobel)
sobel_button.pack(side=tk.TOP, pady=10)

# Create a slider for global thresholding
threshold_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Global Threshold")
threshold_slider.set(128)
threshold_slider.pack(side=tk.TOP, pady=10)

# Create a button to apply global thresholding
global_button = Button(root, text="Apply Global Threshold", command=apply_global_threshold)
global_button.pack(side=tk.TOP, pady=10)

# Create sliders for adaptive thresholding parameters
block_size_slider = Scale(root, from_=3, to=25, orient=HORIZONTAL, label="Block Size (Odd only)")
block_size_slider.set(11)
block_size_slider.pack(side=tk.TOP, pady=10)

C_slider = Scale(root, from_=-10, to=10, orient=HORIZONTAL, label="C Value")
C_slider.set(2)
C_slider.pack(side=tk.TOP, pady=10)

# Create a button to apply adaptive thresholding
adaptive_button = Button(root, text="Apply Adaptive Threshold", command=apply_adaptive_threshold)
adaptive_button.pack(side=tk.TOP, pady=10)

# Create a button to execute git commands
git_button = Button(root, text="Execute Git Commands", command=execute_git_commands)
git_button.pack(side=tk.TOP, pady=10)

# Initialize the original image variable
original_image = None

# Initialize the video capture variable
cap = None

# Run the application
root.mainloop()
