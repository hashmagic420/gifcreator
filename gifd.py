import streamlit as st
from PIL import Image, ImageDraw
import imageio
from streamlit_drawable_canvas import st_canvas

# Create a canvas for drawing, now with a dynamic key and text support
def draw_frame(width, height, stroke_color, bg_color, frame_num, text=None):
    st.write(f"Draw on the canvas (this will be frame {frame_num + 1}):")
    canvas_result = st_canvas(
        stroke_width=3,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=height,
        width=width,
        drawing_mode="freedraw",
        key=f"canvas_frame_{frame_num}"  # Ensure each frame has a unique key
    )

    img = None
    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype('uint8'))
        
        # Apply text if provided
        if text:
            d = ImageDraw.Draw(img)
            d.text((10, 10), text, fill=stroke_color)
    
    return img

# Function to create GIF from user-generated frames
def create_gif_from_frames(frames, duration=200):
    gif_filename = 'output.gif'
    frames[0].save(gif_filename, save_all=True, append_images=frames[1:], duration=duration, loop=0)
    return gif_filename

# Streamlit app structure
st.title("Interactive Frame-by-Frame GIF Creator")

# Settings for the canvas
frame_width = st.number_input("Frame Width:", value=200)
frame_height = st.number_input("Frame Height:", value=100)
primary_color = st.color_picker("Pick a background color for frames:", "#496D89")
stroke_color = st.color_picker("Pick a stroke color for drawing/text:", "#FFFF00")

# Number of frames to generate
total_frames = st.slider("Total number of frames to create:", 1, 20, 5)

# Initialize list to hold frames
user_frames = []
copied_frame = None  # Store the copied frame

# Loop to allow user to create multiple frames
for i in range(total_frames):
    st.write(f"Create Frame {i + 1}")
    
    # Option to apply text to the frame
    text_to_apply = st.text_input(f"Optional: Enter text for Frame {i + 1}", key=f"text_input_{i}")
    
    # Option to copy the previous frame
    copy_previous_frame = st.checkbox(f"Copy previous frame for Frame {i + 1}", key=f"copy_frame_{i}")
    
    # If copying, use the copied frame as a base
    if copy_previous_frame and copied_frame is not None:
        img = copied_frame.copy()  # Copy the previously saved frame
        st.image(img, caption=f"Frame {i + 1} (Copied)", width=200)  # Show copied frame
    else:
        # Draw each frame with a unique key and optional text
        img = draw_frame(frame_width, frame_height, stroke_color, primary_color, i, text=text_to_apply)
    
    if img is not None:
        user_frames.append(img)
        copied_frame = img  # Set the current frame as the copied frame for future use
    
        st.image(img, caption=f"Frame {i + 1}", width=200)  # Show the frame for feedback
    
    if st.button(f"Save Frame {i + 1}", key=f"save_{i}"):
        st.write(f"Frame {i + 1} saved!")

# Once all frames are created, allow the user to generate the GIF
if len(user_frames) == total_frames:
    if st.button("Create GIF"):
        gif_path = create_gif_from_frames(user_frames)
        st.image(gif_path, caption="Generated GIF")

        # Provide a download link for the GIF
        with open(gif_path, "rb") as file:
            st.download_button(
                label="Download GIF",
                data=file,
                file_name="output.gif",
                mime="image/gif"
            )
