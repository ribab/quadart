#!/usr/bin/env python3

from wand.image import Image
from wand.display import display
from wand.color import Color
from wand.drawing import Drawing
import imageio
import click
import numpy as np
import time


def loading_bar(recurse_depth):
    global load_progress
    global start_time
    load_depth=3
    try:
        load_progress
        start_time
    except:
        load_progress = 0
        start_time = time.time()
        print('[' + ' '*(4**load_depth) + ']\r', end='')
    if recurse_depth <= load_depth:
        load_progress += 4**(load_depth - recurse_depth)
        cur_time = time.time()
        time_left = 4**load_depth*(cur_time - start_time)/load_progress \
                  - cur_time + start_time
        print('[' + '='*load_progress \
                  + ' '*(4**load_depth - load_progress) \
                  + '] ' \
                  + 'time left: {} secs'.format(int(time_left)).ljust(19) \
                  + '\r', end='')



class QuadArt:
    def __init__(self, std_thresh=10, draw_type='circle', max_recurse=None):
        self.img = None
        self.canvas = None
        self.draw = None
        self.std_thresh = std_thresh
        self.draw_type = draw_type
        self.recurse_depth = 0
        self.max_recurse_depth = max_recurse

    def recursive_draw(self, x, y, w, h):
        '''Draw the QuadArt recursively
        '''

        if (self.max_recurse_depth == 0 or self.recurse_depth < self.max_recurse_depth) \
        and self.too_many_colors(int(x), int(y), int(w), int(h)):
            self.recurse_depth += 1

            self.recursive_draw(x,         y,         w/2.0, h/2.0)
            self.recursive_draw(x + w/2.0, y,         w/2.0, h/2.0)
            self.recursive_draw(x,         y + h/2.0, w/2.0, h/2.0)
            self.recursive_draw(x + w/2.0, y + h/2.0, w/2.0, h/2.0)

            self.recurse_depth -= 1

            if self.recurse_depth == 3:
                loading_bar(self.recurse_depth)
        else:
            self.draw_avg(x, y, w, h)

            if self.recurse_depth < 3:
                loading_bar(self.recurse_depth)

    def too_many_colors(self, x, y, w, h):
        if w * self.output_scale <= 2 or w <= 2:
            return False
        img = self.img[y:y+h,x:x+w]
        red = img[:,:,0]
        green = img[:,:,1]
        blue = img[:,:,2]

        red_avg = np.average(red)
        green_avg = np.average(green)
        blue_avg = np.average(blue)

        if red_avg >= 254 and green_avg >= 254 and blue_avg >= 254:
            return False

        if 255 - red_avg < self.std_thresh and 255 - green_avg < self.std_thresh \
                                           and 255 - blue_avg < self.std_thresh:
            return True

        red_std = np.std(red)
        if red_std > self.std_thresh:
            return True

        green_std = np.std(green)
        if green_std > self.std_thresh:
            return True

        blue_std = np.std(blue)
        if blue_std > self.std_thresh:
            return True

        return False

    def draw_avg(self, x, y, w, h):
        avg_color = self.get_color(int(x), int(y), int(w), int(h))
        self.draw_in_box(avg_color, x, y, w, h)
        return avg_color

    def get_color(self, x, y, w, h):
        img = self.img[y : y + h,
                       x : x + w]
        red = np.average(img[:,:,0])
        green = np.average(img[:,:,1])
        blue = np.average(img[:,:,2])
        color = Color('rgb(%s,%s,%s)' % (red, green, blue))
        return color

    def draw_in_box(self, color, x, y, w, h):
        if self.draw_type == 'circle':
            self.draw_circle_in_box(color, x, y, w, h)
        else:
            self.draw_square_in_box(color, x, y, w, h)

    def draw_circle_in_box(self, color, x, y, w, h):
        x *= self.output_scale
        y *= self.output_scale
        w *= self.output_scale
        h *= self.output_scale

        self.draw.fill_color = color
        self.draw.circle((int(x + w/2.0), int(y + h/2.0)),
                         (int(x + w/2.0), int(y)))

    def draw_square_in_box(self, color, x, y, w, h):
        x *= self.output_scale
        y *= self.output_scale
        w *= self.output_scale
        h *= self.output_scale

        self.draw.fill_color = color
        self.draw.rectangle(x, y, x + w, y + h)

    def width(self):
        return self.img.shape[1]

    def scale_width(self):
        return self.width() * self.output_scale

    def height(self):
        return self.img.shape[0]

    def scale_height(self):
        return self.height() * self.output_scale

    def generate(self, filename,
                 left=None, right=None, up=None, down=None,
                 output_size=512):
        self.img = imageio.imread(filename)
        left  = 0             if left  is None else int(self.width()  * float(left))
        right = self.width()  if right is None else int(self.width()  * float(right))
        up    = 0             if up    is None else int(self.height() * float(up))
        down  = self.height() if down  is None else int(self.height() * float(down))
        self.img = self.img[up:down,left:right]
        if self.width() < self.height():
            difference = self.height() - self.width()
            subtract_top = int(difference/2)
            subtract_bot = difference - subtract_top
            self.img = self.img[subtract_top:-subtract_bot,:]
        elif self.height() < self.width():
            difference = self.width() - self.height()
            subtract_left = int(difference/2)
            subtract_right = difference - subtract_left
            self.img = self.img[:,subtract_left:-subtract_right]

        self.output_scale = float(output_size) / self.width()

        self.canvas = Image(width = output_size,
                            height = output_size,
                            background = Color('white'))
        self.canvas.format = 'png'
        self.draw = Drawing()
        self.recursive_draw(0, 0, self.width(), self.height())
        self.draw(self.canvas)

    def display(self):
        display(self.canvas)

    def save(self, filename):
        self.canvas.save(filename=filename)


@click.command()
@click.argument('filename')
@click.option('-l', '--left', default=None, help='left pixel of image')
@click.option('-r', '--right', default=None, help='right pixel of image')
@click.option('-u', '--up', default=None, help='top pixel of image')
@click.option('-d', '--down', default=None, help='bottom pixel of image')
@click.option('-o', '--output', default=None, help='name of file to save result to')
@click.option('-s', '--size', default=512, help='Output size')
@click.option('-t', '--type', 'draw_type', default='circle', help='Draw type')
@click.option('--thresh', default=10, help='Standard deviation threshold for color difference')
@click.option('-m', '--max-recurse', 'max_recurse', default=0, help='Maximum allowed recursion depth. Default is infinity.')
def main(filename, left, right, up, down, output, size, draw_type, thresh, max_recurse):
    quadart = QuadArt(std_thresh=thresh, draw_type=draw_type, max_recurse=max_recurse)
    quadart.generate(filename, left=left, right=right,
                               up=up, down=down,
                               output_size=size)
    if output is None:
        quadart.display()
    else:
        quadart.save(output)

if __name__ == '__main__':
    main()
