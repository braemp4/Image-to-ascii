from PIL import Image 
from numpy import array
import curses

donut = Image.open("test-donut.png")
pixels = array(donut)

print(donut.size)

def get_largest_dim(image):
    return max(image.size)

scaling_dimension = get_largest_dim(donut)
def get_scaling_factor(scaling_dimension) -> int:
    if scaling_dimension < 300:
        return 6
    elif scaling_dimension >= 300 and scaling_dimension < 400:
        return 10
    elif scaling_dimension >= 400:
        return 15
    else:
        return 30
scale = get_scaling_factor(scaling_dimension)

def get_luminance(p):
    return p[0] * 0.299 + p[1]* 0.587 + p[2] * 0.144

def lum_to_shade(lum):
    if lum < 60:
        return "black"
    elif 60 <= lum < 110:
        return "dark-grey"
    elif 110 <= lum < 160:
        return "grey"
    elif 160 <= lum < 210:
        return "light-grey"
    elif lum >= 210:
        return "white"

def shade_array(pixels):

    shades = []
    for i in range(len(pixels)):
        nested = []
        for y in range(len(pixels[i])):
            luminance = get_luminance(pixels[i][y])
            shade = lum_to_shade(luminance)
            nested.append(shade)
        shades.append(nested)
    return array(shades)

pixel_to_char = {"black": "@", "dark-grey": "#", "grey": "+", "light-grey": "-", "white": "."}

def main():
    screen = curses.initscr()

    shades = shade_array(pixels)
    for i in range(len(shades)):
        for y in range(len(shades[i])):
            color = shades[i][y]
            screen.addstr( i//scale, y//scale, pixel_to_char[color])

            screen.refresh()
    screen.getch()
main()
