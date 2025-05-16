import pytest
import streamlit as st
from pathlib import Path
import tempfile
from src.app import get_gif_download_link

def test_get_gif_download_link(tmp_path):
    """Test the GIF download link generation."""
    # Create a temporary GIF file
    gif_path = tmp_path / "test.gif"
    with open(gif_path, "wb") as f:
        f.write(b"fake gif content")
    
    # Test link generation
    link = get_gif_download_link(str(gif_path), "test.gif")
    assert "data:image/gif;base64" in link
    assert "download=\"test.gif\"" in link

def test_app_ui_elements():
    """Test the presence of main UI elements."""
    # Note: This is a basic test that checks if the main UI elements are present
    # More complex UI testing would require mocking Streamlit's session state
    # and other components
    
    # The following assertions would need to be implemented with proper Streamlit testing
    # framework or mocking
    pass

def test_app_file_upload():
    """Test file upload functionality."""
    # Note: This would require mocking Streamlit's file uploader
    # and testing the file processing logic
    pass

def test_app_parameters():
    """Test parameter handling."""
    # Note: This would require mocking Streamlit's input widgets
    # and testing the parameter processing logic
    pass

def test_app_conversion():
    """Test the conversion process."""
    # Note: This would require mocking the SpriteConverter
    # and testing the conversion workflow
    pass 