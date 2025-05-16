from typing import List, Tuple
from pathlib import Path
import logging
from PIL import Image

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpriteConverter:
    """Class for converting sprites to animated GIF."""
    
    def __init__(self, input_path: str):
        """
        Initializes the sprite converter.
        
        Args:
            input_path (str): Path to the directory containing the sprites
        """
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(f"The directory {input_path} does not exist")
        
        logger.info(f"Converter initialized with directory: {input_path}")
    
    def resize_sprite_sheet(self, target_size: int = 1020) -> Image.Image:
        """
        Resize the sprite sheet to a size divisible by both 3 and 4.
        
        Args:
            target_size (int): Target size for width and height (default: 1020)
            
        Returns:
            Image.Image: Resized sprite sheet
        """
        try:
            with Image.open(self.input_path) as img:
                # Calculate new dimensions maintaining aspect ratio
                width, height = img.size
                ratio = min(target_size/width, target_size/height)
                new_size = (int(width * ratio), int(height * ratio))
                
                # Resize image
                resized = img.resize(new_size, Image.Resampling.LANCZOS)
                logger.info(f"Resized sprite sheet from {img.size} to {new_size}")
                return resized
                
        except Exception as e:
            logger.error(f"Error resizing sprite sheet: {str(e)}")
            raise
    
    def extract_frames(
        self,
        frame_width: int,
        frame_height: int,
        num_cols: int,
        num_rows: int,
        selected_rows: List[int] = None
    ) -> List[Image.Image]:
        """
        Extract frames from a sprite sheet.
        
        Args:
            frame_width (int): Width of each frame in pixels
            frame_height (int): Height of each frame in pixels
            num_cols (int): Number of columns in the sprite sheet
            num_rows (int): Number of rows in the sprite sheet
            selected_rows (List[int]): List of row indices to extract (1-based)
            
        Returns:
            List[Image.Image]: List of extracted frames
        """
        try:
            # Resize the sprite sheet first
            sprite_sheet = self.resize_sprite_sheet()
            frames = []
            
            # If no rows are selected, use all rows
            if selected_rows is None:
                selected_rows = list(range(1, num_rows + 1))
            
            # Convert to 0-based indices
            selected_rows = [row - 1 for row in selected_rows]
            
            # Read frames left to right, then top to bottom
            for row in range(num_rows):
                if row not in selected_rows:
                    continue
                for col in range(num_cols):
                    left = col * frame_width
                    top = row * frame_height
                    right = (col + 1) * frame_width
                    bottom = (row + 1) * frame_height
                    
                    frame = sprite_sheet.crop((left, top, right, bottom))
                    frames.append(frame)
            
            logger.info(f"Extracted {len(frames)} frames from sprite sheet")
            return frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            raise
    
    def convert_to_gif(
        self,
        output_path: str,
        frame_width: int,
        frame_height: int,
        num_cols: int,
        num_rows: int,
        duration: int = 100,
        loop: int = 0,
        optimize: bool = True,
        selected_rows: List[int] = None
    ) -> bool:
        """
        Convert sprite sheet to animated GIF.
        
        Args:
            output_path (str): Output path for the GIF
            frame_width (int): Width of each frame in pixels
            frame_height (int): Height of each frame in pixels
            num_cols (int): Number of columns in the sprite sheet
            num_rows (int): Number of rows in the sprite sheet
            duration (int): Duration of each frame in milliseconds
            loop (int): Number of loops (0 for infinite)
            optimize (bool): Whether to optimize the GIF
            selected_rows (List[int]): List of row indices to include (1-based)
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        try:
            frames = self.extract_frames(
                frame_width, 
                frame_height, 
                num_cols, 
                num_rows,
                selected_rows
            )
            
            if not frames:
                logger.error("No frames were extracted")
                return False
            
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=loop,
                optimize=optimize
            )
            
            logger.info(f"GIF saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting to GIF: {str(e)}")
            return False 