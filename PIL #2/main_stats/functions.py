from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import random
from fontTools.ttLib import TTCollection

OPACITY = 200
LEFT_TEXT = 1160
RIGHT_TEXT = 1880
RIGHT_Y_POSITION = 75
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"

def draw_text(im, text, color, position, font_size, index, anchor):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size, index=index)
    draw.text(position, str(text), font=font, fill=color,anchor=anchor)

def text_bold(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 10, anchor=anchor)

def text(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 0, anchor=anchor)

def text_narrow(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 7, anchor=anchor)

def get_random_background():
    folder_path = "PIL #2/backgrounds"
    png_files = [file for file in os.listdir(folder_path)]

    image = random.choice(png_files)

    image_path = os.path.join(folder_path, image)
    im = Image.open(image_path)
    im = im.filter(ImageFilter.GaussianBlur(radius=5.0))

    return im

def create_right_background(im):
    shape = [(1120, 0), (1920, 1080)]
    size = shape[1][0] - shape[0][0], shape[1][1] - shape[0][1]
    print(size)
    
    # Create rectangle in 'RGBA' mode for transparency support
    rectangle = Image.new('RGBA', size, (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(rectangle)
    
    draw.rectangle([(0, 0), (800, 1080)], fill=(0, 0, 0, OPACITY))
    
    # Paste the rectangle onto the image with transparency
    im.paste(rectangle, (shape[0][0], shape[0][1]), rectangle)

def create_rounded_rectangle(image, size, corner_radius, color, position, scale_factor=3):
    width, height = size
    scaled_size = (width * scale_factor, height * scale_factor)
    scaled_radius = corner_radius * scale_factor

    # centre on position, rather than top left
    position = int(position[0] - width/2), int(position[1] - height/2)
    
    # Create a scaled-up image
    rectangle = Image.new('RGBA', scaled_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)
    
    # Draw the rounded rectangle on the scaled image
    draw.rounded_rectangle(
        [(0, 0), scaled_size],
        radius=scaled_radius,
        fill=color
    )
    
    # Downscale the image to the target size to apply anti-aliasing
    rounded_rectangle = rectangle.resize(size, Image.LANCZOS)
    image.paste(rounded_rectangle, position, rounded_rectangle)