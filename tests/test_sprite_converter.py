import pytest
from pathlib import Path
from PIL import Image
from src.sprite_converter import SpriteConverter

def create_test_sprite_sheet(tmp_path: Path, width: int, height: int, cols: int, rows: int) -> Path:
    """Create a test sprite sheet image."""
    # Create a blank image
    sheet = Image.new('RGBA', (width * cols, height * rows), (0, 0, 0, 0))
    
    # Save it
    output_path = tmp_path / "test_sprite_sheet.png"
    sheet.save(output_path)
    return output_path

def test_sprite_converter_initialization(tmp_path):
    """Test converter initialization."""
    # Create a test sprite sheet
    sheet_path = create_test_sprite_sheet(tmp_path, 64, 64, 4, 3)
    
    # Test initialization
    converter = SpriteConverter(str(sheet_path))
    assert converter.input_path == sheet_path

def test_sprite_converter_invalid_path():
    """Test initialization with invalid path."""
    with pytest.raises(FileNotFoundError):
        SpriteConverter("invalid/path.png")

def test_extract_frames(tmp_path):
    """Test frame extraction from sprite sheet."""
    # Create a test sprite sheet
    sheet_path = create_test_sprite_sheet(tmp_path, 64, 64, 4, 3)
    
    converter = SpriteConverter(str(sheet_path))
    frames = converter.extract_frames(64, 64, 4, 3)
    
    assert len(frames) == 12  # 4 columns * 3 rows
    assert all(isinstance(frame, Image.Image) for frame in frames)
    assert all(frame.size == (64, 64) for frame in frames)

def test_extract_frames_with_row_selection(tmp_path):
    """Test frame extraction with specific row selection."""
    # Create a test sprite sheet
    sheet_path = create_test_sprite_sheet(tmp_path, 64, 64, 4, 3)
    
    converter = SpriteConverter(str(sheet_path))
    
    # Test selecting only the first row
    frames = converter.extract_frames(64, 64, 4, 3, selected_rows=[1])
    assert len(frames) == 4  # Only first row (4 columns)
    
    # Test selecting multiple rows
    frames = converter.extract_frames(64, 64, 4, 3, selected_rows=[1, 3])
    assert len(frames) == 8  # First and last rows (4 columns each)
    
    # Test with no rows selected
    frames = converter.extract_frames(64, 64, 4, 3, selected_rows=[])
    assert len(frames) == 0

def test_convert_to_gif(tmp_path):
    """Test GIF conversion."""
    # Create a test sprite sheet
    sheet_path = create_test_sprite_sheet(tmp_path, 64, 64, 4, 3)
    output_path = tmp_path / "output.gif"
    
    converter = SpriteConverter(str(sheet_path))
    success = converter.convert_to_gif(
        str(output_path),
        frame_width=64,
        frame_height=64,
        num_cols=4,
        num_rows=3
    )
    
    assert success
    assert output_path.exists()

def test_convert_to_gif_with_row_selection(tmp_path):
    """Test GIF conversion with row selection."""
    # Create a test sprite sheet
    sheet_path = create_test_sprite_sheet(tmp_path, 64, 64, 4, 3)
    output_path = tmp_path / "output.gif"
    
    converter = SpriteConverter(str(sheet_path))
    
    # Test converting only the first row
    success = converter.convert_to_gif(
        str(output_path),
        frame_width=64,
        frame_height=64,
        num_cols=4,
        num_rows=3,
        selected_rows=[1]
    )
    
    assert success
    assert output_path.exists()
    
    # Test converting multiple rows
    success = converter.convert_to_gif(
        str(output_path),
        frame_width=64,
        frame_height=64,
        num_cols=4,
        num_rows=3,
        selected_rows=[1, 3]
    )
    
    assert success
    assert output_path.exists()
    
    # Test with no rows selected
    success = converter.convert_to_gif(
        str(output_path),
        frame_width=64,
        frame_height=64,
        num_cols=4,
        num_rows=3,
        selected_rows=[]
    )
    
    assert not success  # Should fail when no rows are selected 