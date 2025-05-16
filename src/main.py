from sprite_converter import SpriteConverter
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Define paths
    sprite_path = project_root / "assets" / "wizard_fireball_12frames.png"
    output_path = project_root / "assets" / "output.gif"
    
    # Initialize the converter with your sprite sheet
    converter = SpriteConverter(str(sprite_path))
    
    # Convert to GIF
    success = converter.convert_to_gif(
        output_path=str(output_path),
        frame_width=255,     # 1020/4 = 255 pixels
        frame_height=340,    # 1020/3 = 340 pixels
        num_cols=4,          # 4 colonnes
        num_rows=3,          # 3 lignes
        duration=100,        # 100ms par frame
        loop=0,             # 0 means infinite loop
        optimize=True
    )
    
    if success:
        print(f"GIF created successfully at: {output_path}")
    else:
        print("Failed to create GIF")

if __name__ == "__main__":
    main() 