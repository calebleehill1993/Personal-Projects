from PIL import Image, ImageFont, ImageDraw
import random

text = 'hello people of Earth! I have come to declare victory over you and your puny little world. It is so so tiny and I am the biggest and most incredible person born!!!'
ratio = (7, 9) # Standard is portrait 7x9
horizontal = False
image_width = 667 # Standard is 667
margin = 0.05 # Standard is 0.05
font_size = 20 # Standard is 100
spacing = 4 # Standard is 4
font_url = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf" # Standard is "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

def contrasting_color1(color):
    return tuple([255 - c for c in color])

def contrasting_color2(color):
    return tuple([(c + 128) % 256 for c in color])

# size = width x height
output_image = Image.new(mode='RGB', size=(2, 1))
output_map = output_image.load()

primary_color = tuple([random.randint(0, 255) for i in range(3)])

output_map[0, 0] = primary_color
output_map[1, 0] = contrasting_color1(primary_color)

output_image.save('test.png')


img = Image.new('RGB', (1000, 1000), color = 'black')
font = ImageFont.truetype(font_url, font_size)
draw = ImageDraw.Draw(img)
fill00 = (0, 0, 0)
text00 = (255, 255, 255)
draw.rectangle(((0, 0), (100, 100)), fill=fill00)
draw.text((50, 50), 'Text Here', fill=text00, anchor='mm', font=font)
fill10 = (255, 255, 255)
text10 = (0, 0, 0)
draw.rectangle(((100, 0), (200, 100)), fill=fill10)
draw.text((150, 50), 'Text Here', fill=text10, anchor='mm', font=font)
fill01 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
text01 = contrasting_color1(fill01)
draw.rectangle(((0, 100), (100, 200)), fill=fill01)
draw.text((50, 150), 'Text Here', fill=text01, anchor='mm', font=font)
fill11 = fill01
text11 = contrasting_color2(fill11)
draw.rectangle(((100, 100), (200, 200)), fill=fill11)
draw.text((150, 150), 'Text Here', fill=text11, anchor='mm', font=font)


img.save('test_color.png')