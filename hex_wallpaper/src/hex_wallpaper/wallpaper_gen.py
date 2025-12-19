from PIL import Image
import numpy as np
import math

class HexWallpaperGenerator:
    
    #Generates a hexagonal SVG wallpaper from a low-resolution image.
    

    def __init__(self, input_file, hex_radius=20):
        self.input_file = input_file
        self.hex_radius = hex_radius

        self.img = Image.open(input_file) #loading image
        self.width, self.height = self.img.size
        self.pixels = self.img.load()
        
    # Hexagon geometry

    def hexagon_points(self, xc, yc):
        
        #Returns the 6 corner points of a hexagon centered at (xc, yc)
        r = self.hex_radius
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = xc + r * math.cos(angle)
            y = yc + r * math.sin(angle)
            points.append((x, y))
        return points

    @staticmethod
    def points_to_svg(points):
        """
        Converts a list of points into SVG string format
        """
        return " ".join([f"{x},{y}" for x, y in points])


    # color sampling
    def average_color(self, xc, yc):
        
        #Samples pixels inside a circular approximation of a hexagon
        #& returns the average color as an (R, G, B) tuple
        
        r = self.hex_radius
        colors = []
        x_start = max(0, int(xc - r))
        x_end = min(self.width, int(xc + r))
        y_start = max(0, int(yc - r))
        y_end = min(self.height, int(yc + r))

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if (x - xc) ** 2 + (y - yc) ** 2 <= r ** 2:
                    # Fixed: PIL pixels are accessed as [x, y] where x is horizontal
                    pixel = self.pixels[x, y]
                    # Handle both RGB and RGBA images
                    if isinstance(pixel, int):  # Grayscale
                        colors.append((pixel, pixel, pixel))
                    elif len(pixel) >= 3:  # RGB or RGBA
                        colors.append(pixel[:3])  # Take only RGB values
                    else:
                        colors.append(pixel)

        if colors:
            avg = tuple(np.mean(colors, axis=0).astype(int))
            return avg
        else:
            return (255, 255, 255)


    # combine fcts & svg generation
    def generate_svg(self, output_file):
        
        #Generates an SVG file with hexagons colored according to the input image
        
        hex_width = 2 * self.hex_radius
        hex_height = math.sqrt(3) * self.hex_radius

        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">\n'

        rows = int(self.height / (hex_height * 0.75)) + 2  # Added +2 for coverage
        cols = int(self.width / hex_width) + 2

        for row in range(rows):
            for col in range(cols):
                xc = col * hex_width + (hex_width / 2 if row % 2 else 0)
                yc = row * hex_height * 0.75

                # Skip hexagons completely outside the image bounds
                if xc < -self.hex_radius or xc > self.width + self.hex_radius:
                    continue
                if yc < -self.hex_radius or yc > self.height + self.hex_radius:
                    continue

                color = self.average_color(xc, yc)
                points = self.hexagon_points(xc, yc)
                points_str = self.points_to_svg(points)
                # Fixed: removed extra space in rgb format
                svg_content += f'<polygon points="{points_str}" fill="rgb({color[0]},{color[1]},{color[2]})" stroke="none"/>\n'

        svg_content += "</svg>"

        with open(output_file, "w") as f:
            f.write(svg_content)

        print(f"SVG saved to {output_file}")




def main():
    gen = HexWallpaperGenerator(
        "src/hex_wallpaper/input.png",
        20
    )
    gen.generate_svg("src/hex_wallpaper/output.svg")
    print("SVG generated: src/hex_wallpaper/output.svg")

if __name__ == "__main__":
    main()


