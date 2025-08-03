from PIL import Image
import curses
from curses.textpad import Textbox, rectangle
from time import sleep
from numpy import array

def get_largest_dim(img):
    return max(img.size)

def get_scaling_factor(scaling_dimension) -> int:
    
    if scaling_dimension < 300:
        return 6
    elif scaling_dimension >= 300 and scaling_dimension < 350:
        return 10
    elif scaling_dimension >= 400:
        return 15
    else:
        return 30

def get_scaling_factor_new(scaling_dimension, window) -> int:
    window_size = max(window.getmaxyx())

    return window_size // scaling_dimension

def get_luminance(p):
    return p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.144

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
pixel_to_char = {"black": "@", "dark-grey": "#", "grey": "+", "light-grey": "-", "white": " "}

def convert_img(window, pixels, scale):
    shades = shade_array(pixels)
    for i in range(len(shades)):
        for j in range(len(shades[i])):
            color = shades[i][j]
            window.addstr(i//scale, j//scale, pixel_to_char[color])
            
            #window.refresh()
    window.refresh() #if we want to render image all at once

def main():
    screen = curses.initscr()
    curses.noecho()
    y,x = screen.getmaxyx()
    
    #Title and prompt
    screen.addstr(0, 0, "Image ==> Ascii Converter:", curses.A_BOLD)
    screen.addstr(2,0, "Image URL:")
    screen.refresh()
        
    #Displaying errors
    error_win = curses.newwin(5,25, 0, 45)
    screen.refresh()

    #Textbox
    text_win = curses.newwin(0, 20, 2,12)
    text_box = Textbox(text_win)
    #rectangle(screen, 2, 12, 2, 2)
           
    #screen.refresh()
    while True:
        screen.refresh()
        text_box.edit()
        #screen.refresh() #idk if we need this
 
        url = text_box.gather().strip().replace("\n", "")
        #url = "placeholder"
        try:
            img = Image.open(url)
            break
        except:
            img = None
            text_win.clear()
            screen.refresh()

            error_win.addstr("Empty or invalid URL")
            error_win.refresh()
            sleep(0.5)
            error_win.clear()
            error_win.refresh()
    if img:
        screen.clear() #placeholder - > render will have its own screen

        pixels = array(img)
        scaling_dimension = get_largest_dim(img)
        scale = get_scaling_factor(scaling_dimension)
        #scale = get_scaling_factor_new(scaling_dimension, screen)
        convert_img(screen,pixels, scale)

    #else:
    #    return

main()


