#!/usr/bin/env python3

from wand.image import Image
from wand.display import display
from wand.color import Color
from wand.drawing import Drawing

import imageio
import visvis

import click

import numpy as np
import math

import sys

STD_THRESH = 10

NUM_COLORS_THRESHOLD = 100


MAX_COLOR_DIFF = 0.4

DRAW_CIRCLES = True


#def too_many_colors(img, x, y, w, h):
#    colors = set()
#    num_colors = 0
#    for row in img[x : x + w,
#                   y : y + h]:
#        for color in row:
#            if color not in colors:
#                colors.add(color)
#            if len(colors) > NUM_COLORS_THRESHOLD:
#                return True
#    return False


def too_many_colors(img, avg_color, x, y, w, h):
    if w <= 2:
        return False
    img = img[y:y+h,x:x+w]
    red = img[:,:,0]
    green = img[:,:,1]
    blue = img[:,:,2]
    red_std = np.std(red)
    if red_std > STD_THRESH:
        return True
    green_std = np.std(green)
    if green_std > STD_THRESH:
        return True
    blue_std = np.std(blue)
    if blue_std > STD_THRESH:
        return True
    return False

# This was the one I was using
#def too_many_colors(img, avg_color, x, y, w, h):
#    #import pdb ;pdb.set_trace()
#    if w <= 2:
#        return False
#    subimg = img[x:x+w,y:y+h]
#    subimg.resize(1,1)
#    avg_color = subimg[0,0]
#    if avg_color == img[x,y]:
#        return False
#    min_red = 1
#    max_red = 0
#    min_green = 1
#    max_green = 0
#    min_blue = 1
#    max_blue = 0
#    subimg = img[x:x+w,y:y+h]
#    for color in subimg.histogram:
#        min_red = min(min_red, color.red)
#        max_red = max(max_red, color.red)
#        if max_red - min_red > MAX_COLOR_DIFF:
#            return True
#        min_green = min(min_green, color.green)
#        max_green = max(max_green, color.green)
#        if max_green - min_green > MAX_COLOR_DIFF:
#            return True
#        min_blue = min(min_blue, color.blue)
#        max_blue = max(max_blue, color.blue)
#        if max_blue - min_blue > MAX_COLOR_DIFF: 
#            return True
#    return False


#def too_many_colors(img, avg_color, x, y, w, h,
#                    min_red = 1, max_red = 0,
#                    min_green = 1, max_green = 0,
#                    min_blue = 1, max_blue = 0):
#    if w <= 2:
#        return False
#    subimg = img[x:x+w,y:y+h]
#    subimg.resize(1,1)
#    avg_color = subimg[0,0]
#    if avg_color == img[x,y]:
#        return False
#    min_red = min(img[x,y].red, img[x+w-1,y].red,
#                  img[x,y+h-1].red, img[x+w-1,y+h-1].red,
#                  min_red)
#    max_red = max(img[x,y].red, img[x+w-1,y].red,
#                  img[x,y+h-1].red, img[x+w-1,y+h-1].red,
#                  max_red)
#    if max_red - min_red > MAX_COLOR_DIFF:
#        return True
#    min_green = min(img[x,y].green, img[x+w-1,y].green,
#                    img[x,y+h-1].green, img[x+w-1,y+h-1].green,
#                    min_green)
#    max_green = max(img[x,y].green, img[x+w-1,y].green,
#                    img[x,y+h-1].green, img[x+w-1,y+h-1].green,
#                    max_green)
#    if max_green - min_green > MAX_COLOR_DIFF:
#        return True
#    min_blue = min(img[x,y].blue, img[x+w-1,y].blue,
#                   img[x,y+h-1].blue, img[x+w-1,y+h-1].blue,
#                   min_blue)
#    max_blue = max(img[x,y].blue, img[x+w-1,y].blue,
#                   img[x,y+h-1].blue, img[x+w-1,y+h-1].blue,
#                   max_blue)
#    if max_blue - min_blue > MAX_COLOR_DIFF: 
#        return True
#    if too_many_colors(img, avg_color, x, y, int(w * 0.5), int(h * 0.5),
#                       min_red = min_red, max_red = max_red,
#                       min_green = min_green, max_green = max_green,
#                       min_blue = min_blue, max_blue = max_blue):
#        return True
#    if too_many_colors(img, avg_color, x + int(w*0.5), y, int(w * 0.5), int(h * 0.5),
#                       min_red = min_red, max_red = max_red,
#                       min_green = min_green, max_green = max_green,
#                       min_blue = min_blue, max_blue = max_blue):
#        return True
#    if too_many_colors(img, avg_color, x, y + int(h*0.5), int(w * 0.5), int(h * 0.5),
#                       min_red = min_red, max_red = max_red,
#                       min_green = min_green, max_green = max_green,
#                       min_blue = min_blue, max_blue = max_blue):
#        return True
#    if too_many_colors(img, avg_color, x + int(w*0.5), y + int(h*0.5), int(w * 0.5), int(h * 0.5),
#                       min_red = min_red, max_red = max_red,
#                       min_green = min_green, max_green = max_green,
#                       min_blue = min_blue, max_blue = max_blue):
#        return True
#    return False

def get_color(img, x, y, w, h):
    img = img[y : y + h,
              x : x + w]
    red = np.average(img[:,:,0])
    green = np.average(img[:,:,1])
    blue = np.average(img[:,:,2])
    color = Color('rgb(%s,%s,%s)' % (red, green, blue))
    return color

def draw_square_in_box(draw, color,
                       x, y, w, h):
    global OUTPUT_SCALE
    x *= OUTPUT_SCALE
    y *= OUTPUT_SCALE
    w *= OUTPUT_SCALE
    h *= OUTPUT_SCALE
    draw.fill_color = color
    draw.rectangle(x, y, x + w, y + h)

def draw_circle_in_box(draw, color,
                       x, y, w, h):
    global OUTPUT_SCALE

    if not DRAW_CIRCLES:
        draw_square_in_box(draw, color, x, y, w, h)
    else:
        x *= OUTPUT_SCALE
        y *= OUTPUT_SCALE
        w *= OUTPUT_SCALE
        h *= OUTPUT_SCALE

        draw.fill_color = color
        draw.circle((int(x + w/2.0), int(y + h/2.0)),
                    (int(x + w/2.0), int(y)))


def draw_avg_circle(img, canvas, draw, x, y, w, h):
    x_int = int(x)
    y_int = int(y)
    w_int = int(w)
    h_int = int(h)
    if w == 0:
        w = 1
    if h == 0:
        h = 1
    if x == img.shape[1] - 1:
        x = img.shape[1] - 2
    if y == img.shape[0] - 1:
        y = img.shape[0] - 2
    avg_color = get_color(img, x_int, y_int, w_int, h_int)
    draw_circle_in_box(draw, avg_color, x, y, w, h)
    return avg_color


def recursive_draw(img, canvas, draw, x, y, w, h):
    global level
    global count
    try:
        level += 1
    except:
        level = 1
        print('\r[{}]'.format(' '*64), end='')
    if level == 4:
        try:
            count += 1
        except:
            count = 1
        print('\r[{}{}]'.format('='*count, ' '*(64-count)), end='')
    x_int = int(x)
    y_int = int(y)
    w_int = int(w)
    h_int = int(h)
    if w == 0:
        w = 1
    if h == 0:
        h = 1
    if x == img.shape[1] - 1:
        x = img.shape[1] - 2
    if y == img.shape[0] - 1:
        y = img.shape[0] - 2
#    relhistsize = histsize/(subimg.width*subimg.height)
    if too_many_colors(img, None,
                       x_int, y_int, w_int, h_int):
        recursive_draw(img, canvas, draw, x,         y,         w/2.0, h/2.0)
        recursive_draw(img, canvas, draw, x + w/2.0, y,         w/2.0, h/2.0)
        recursive_draw(img, canvas, draw, x,         y + h/2.0, w/2.0, h/2.0)
        recursive_draw(img, canvas, draw, x + w/2.0, y + h/2.0, w/2.0, h/2.0)
    else:
        draw_avg_circle(img, canvas, draw, x, y, w, h)
        if level == 3:
            try:
                count += 4
            except:
                count = 4
            print('\r[{}{}]'.format('='*count, ' '*(64-count)))
        if level == 2:
            try:
                count += 16
            except:
                count = 16
            print('\r[{}{}]'.format('='*count, ' '*(64-count)))
    level -= 1


@click.command()
@click.argument('filename')
@click.option('-l', '--left', default=None, help='left pixel of image')
@click.option('-r', '--right', default=None, help='right pixel of image')
@click.option('-u', '--up', default=None, help='top pixel of image')
@click.option('-d', '--down', default=None, help='bottom pixel of image')
def main(filename, left, right, up, down):
    global OUTPUT_SCALE

    img = imageio.imread(filename)
    width = img.shape[1]
    height = img.shape[0]

    if left is None:
        left = 0
    else:
        left = int(width * float(left))

    if right is None:
        right = width
    else:
        right = int(width * float(right))

    if up is None:
        up = 0
    else:
        up = int(height * float(up))

    if down is None:
        down = height
    else:
        down = int(height * float(down))
    
    img = img[left:right, up:down]
    width = img.shape[1]
    height = img.shape[0]
    
    if width != height:
        print('Image must be a square.')
        sys.exit(1)

    OUTPUT_SCALE = 1
    while (OUTPUT_SCALE + 1) * width <= 1000:
        OUTPUT_SCALE += 1
    
    with Image(width = int(width * OUTPUT_SCALE),
               height = int(height * OUTPUT_SCALE),
               background = Color('white')) as canvas:
        canvas.format = 'png'
        with Drawing() as draw:

            recursive_draw(img, canvas, draw, 0, 0, width, height)
            draw(canvas)
            display(canvas)

if __name__ == '__main__':
    main()
