# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 15:59:59 2018

@author: Nicolaj


Plaese install package
    tifffile
if opening tiff files


"""
import time
import numpy as np
from scipy import ndimage
import imageio





def main():
    frame =  imageio.imread('face.tiff')
    print(frame.shape)

    for _ in range(10):
        x, y, error = find_best_correlation(frame, frame, 5, 5, 3)

    print('minimal error with shift x={}px and y={}px with error {}'.format(int(x),int(y), error))



def find_best_correlation(frame1, frame2, x_range, y_range, blur):
    """
    find_best_correlation(frame1, frame2, x_range, y_range, blur)

    Derives the difference between frame1 and frame 2 based on shifting
    frame2 in +/- x_range and +/- in y_range relative to frame1
    blur defines the sigma for gaussian blur. If blur = 0 no blurring will be
    calculated.

    returns x, y and error value for the shift with the minimal error
    """
    start_time = time.time()
    height, width, depth = frame1.shape
    if frame1.shape != frame2.shape:
        print('Frames have different solution!')
        return

    if x_range <=0 or y_range<=0 or type(x_range)!=int or type(y_range)!=int:
        print('x_range and y_range must be positive integer')
        return

    # blurring of frame1 and frame 2
    if blur > 0:
        frame1 = ndimage.gaussian_filter(frame1, sigma=blur)
        frame2 = ndimage.gaussian_filter(frame2, sigma=blur)

    # frame 1 is cropped to size for comparisson
    x_start = x_range
    x_end = width-x_range
    y_start = y_range
    y_end = height-y_range
    frame1 = frame1[y_start:y_end, x_start:x_end]

    # list of pixel shift in x and y direction and error
    shift_matrix = np.zeros(((x_range*2+1)*(y_range*2+1),3))
    index = 0
    buffer = np.zeros((height+2*y_range, width+2*x_range, depth))
    buffer_height, buffer_width, buffer_debth = buffer.shape
    for x in range(-x_range, x_range+1):
        # derive the shifted position   for x
        x_start = x_range + x
        x_end = buffer_width-x_range+x
        for y in range(-y_range, y_range+1):
            buffer = np.zeros((height+2*y_range, width+2*x_range, depth))

            # derive the shifted position   for y
            y_start = y_range+y
            y_end = buffer_height-y_range+y

            # populate the buffer with the shifted frame content
            buffer[y_start:y_end, x_start:x_end]=frame2

            # crop frame to only populated cells
            buffer = buffer[2*y_range:buffer_height-2*y_range,
                            2*x_range:buffer_width-2*x_range]

            # derive difference between frame1 and buffer (shifted frame2)
            difference= np.abs(frame1-buffer)

            # integrate absolute error
            error = np.sum(difference)
            shift_matrix[index,:] = [x, y, error]

            index+=1

    # find minimal abs error:
    min_error_pos = np.argmin(shift_matrix[:,2])

    # get pixel shift
    x = shift_matrix[min_error_pos,0]
    y = shift_matrix[min_error_pos,1]

    end_time = time.time()

    print('x={0}px \ty={1}px \te={2} \t{3:.2f}s \t{4:.2f}Hz'.format(int(x),
                                                      int(y),
                                                      int(error),
                                                      end_time-start_time,
                                                      1/(end_time-start_time)))


    return x, y, error




if __name__ == '__main__':
    main()
