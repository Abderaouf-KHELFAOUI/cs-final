
import marimo as mr

app = mr.App()

# If your generator.py is in the same folder
from wallpaper_gen import HexWallpaperGenerator


@mr.widget
def generate_wallpaper(
    input_file: str = "input.png",   # Input image file
    hex_radius: int = 20,            # Hexagon size
    output_file: str = "output.svg"  # Output SVG file
):
    """
    Interactive widget to generate hexagonal wallpaper.
    """
    gen = HexWallpaperGenerator(input_file, hex_radius)
    gen.generate_svg(output_file)
    return f"SVG generated: {output_file}"


generate_wallpaper()
