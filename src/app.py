import streamlit as st
from sprite_converter import SpriteConverter
from pathlib import Path
import tempfile
import os
import base64

def get_gif_download_link(gif_path: str, file_name: str) -> str:
    """Crée un lien de téléchargement pour le GIF."""
    with open(gif_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:image/gif;base64,{b64}" download="{file_name}">Download GIF</a>'

# Configuration de la page
st.set_page_config(
    page_title="Sprite to GIF Converter",
    page_icon="🖼️",
    layout="centered"
)

# Style personnalisé
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stImage {
        max-width: 250px;
        margin: 0 auto;
    }
    .preview-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
    }
    /* Réduire la largeur des number inputs */
    .stNumberInput {
        max-width: 120px;
    }
    /* Réduire la largeur des multiselect */
    .stMultiSelect {
        max-width: 100%;
    }
    /* Réduire la largeur des checkboxes */
    .stCheckbox {
        max-width: 120px;
    }
    /* Supprimer les marges inutiles */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    /* Ajuster l'espacement des colonnes */
    .row-widget.stButton {
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🖼️ Sprite to GIF Converter")

# Section d'upload
uploaded_file = st.file_uploader("Upload your sprite sheet", type=['png'])

if uploaded_file is not None:
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        sprite_path = tmp_file.name

    # Aperçu et paramètres côte à côte
    col_params, col_preview = st.columns([2, 1])
    
    with col_preview:
        st.markdown('<div class="preview-section">', unsafe_allow_html=True)
        st.image(uploaded_file, caption="Preview", width=200)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_params:
        st.markdown("### Parameters")
        
        # Frame dimensions
        col_width, col_height,col_duration = st.columns(3)
        with col_width:
            frame_width = st.number_input("Frame width (px)", min_value=1, value=256)
        with col_height:
            frame_height = st.number_input("Frame height (px)", min_value=1, value=256)
        with col_duration:
            duration = st.number_input("Frame duration (ms)", min_value=1, value=100)
            
        # Frames per row and number of rows
        col_frames, col_rows, col_optimize = st.columns(3)
        with col_frames:
            frames_per_row = st.number_input("Frames per row", min_value=1, value=4)
        with col_rows:
            number_of_rows = st.number_input("Number of rows", min_value=1, value=3)
        with col_optimize:
            optimize = st.checkbox("Optimize GIF", value=True)

        # Row selection (full width)
        selected_rows = st.multiselect(
            "Select rows",
            options=list(range(1, number_of_rows + 1)),
            default=list(range(1, number_of_rows + 1))
        )

    # Bouton de conversion centré
    st.markdown("<div style='text-align: center; margin-top: 0.5rem;'>", unsafe_allow_html=True)
    if st.button("Convert to GIF", use_container_width=True):
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
                num_cols=frames_per_row,
                num_rows=number_of_rows,
                duration=duration,
                loop=0,  # Always infinite loop
                optimize=optimize,
                selected_rows=selected_rows
            )

            if success:
                st.success("GIF created successfully!")
                
                # Alternative display method: Base64 embed
                try:
                    with open(output_path, "rb") as f:
                        gif_bytes_for_embed = f.read()
                    b64_gif = base64.b64encode(gif_bytes_for_embed).decode()
                    
                    st.markdown(
                        f'<img src="data:image/gif;base64,{b64_gif}" alt="Generated GIF" width="200">',
                        unsafe_allow_html=True
                    )
                    st.caption("Result (via Markdown)")
                except Exception as e:
                    st.error(f"Error embedding GIF with Markdown: {e}")

                # Keep your st.download_button logic
                with open(output_path, "rb") as file_bytes_for_download:
                    st.download_button(
                        label="Download GIF",
                        data=file_bytes_for_download,
                        file_name=f"{Path(uploaded_file.name).stem}.gif",
                        mime="image/gif",
                        key="download_button_markdown_attempt",
                        use_container_width=True
                    )
                
                os.unlink(sprite_path)
                os.unlink(output_path)
            else:
                st.error("Failed to create GIF")
    st.markdown("</div>", unsafe_allow_html=True) 