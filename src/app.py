import streamlit as st
from sprite_converter import SpriteConverter
from pathlib import Path
import tempfile
import os

st.set_page_config(
    page_title="Sprite to GIF Converter",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 Sprite to GIF Converter")

# File uploader
uploaded_file = st.file_uploader("Choose your sprite sheet PNG file", type=['png'])

if uploaded_file is not None:
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        sprite_path = tmp_file.name

    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        frame_width = st.number_input("Frame width (pixels)", min_value=1, value=255)
        num_cols = st.number_input("Number of frames per row", min_value=1, value=4)
        duration = st.number_input("Duration per frame (ms)", min_value=1, value=100)
    
    with col2:
        frame_height = st.number_input("Frame height (pixels)", min_value=1, value=340)
        num_rows = st.number_input("Number of frames per column", min_value=1, value=3)
        optimize = st.checkbox("Optimize GIF", value=True)

    if st.button("Convert to GIF"):
        with st.spinner("Converting..."):
            # Create a temporary file for the output GIF
            with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as output_file:
                output_path = output_file.name

            # Convert to GIF
            converter = SpriteConverter(sprite_path)
            success = converter.convert_to_gif(
                output_path=output_path,
                frame_width=frame_width,
                frame_height=frame_height,
                num_cols=num_cols,
                num_rows=num_rows,
                duration=duration,
                loop=0,
                optimize=optimize
            )

            if success:
                st.success("GIF created successfully!")
                
                # Display the GIF
                st.image(output_path, caption="Resulting GIF")
                
                # Download button
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download GIF",
                        data=file,
                        file_name=f"{Path(uploaded_file.name).stem}.gif",
                        mime="image/gif",
                        key="download_button"
                    )
                
                # Clean up temporary files
                os.unlink(sprite_path)
                os.unlink(output_path)
            else:
                st.error("Failed to create GIF") 