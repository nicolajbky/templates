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
    # loading template frame
    frame_ =  imageio.imread('face.tiff')

    # Since the data are only b/w, only one value per cell is relevant
    # the following code transforms the tiff data accordingly
    h, w, _ = frame_.shape
    frame = np.zeros((h,w))
    for y in range(h):
        for x in range(w):
            frame[y][x] = frame_[y][x][0]

    # for the sake of testing, 10 runs of the same calculations are performed
    runs=10
    tic = time.time()
    for _ in range(runs):
        x, y, error = find_best_correlation(frame, frame, 5, 5, 0)
    toc = time.time()

    print('Average {3:.3f}s \t{4:.2f}Hz'.format(int(x),
                                                      int(y),
                                                      int(error),
                                                      (toc-tic)/runs,
                                                      runs/(toc-tic)))

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

    height, width = frame1.shape
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
    for x in range(-x_range, x_range+1):
        for y in range(-y_range, y_range+1):
            # select shifted position of data in frame 2
            buffer = frame2[y_range+y:height-y_range+y,
                              x_range+x:width-x_range+x]

            # derive difference between frame1 and buffer (shifted frame2)
            difference= np.abs(frame1-buffer)

            # integrate absolute error
            error = np.sum(difference)
            #error = difference.sum()
            shift_matrix[index,:] = [x, y, error]

            index+=1

    # find minimal abs error:
    min_error_pos = np.argmin(shift_matrix[:,2])

    # get pixel shift
    x = shift_matrix[min_error_pos,0]
    y = shift_matrix[min_error_pos,1]
    min_error = shift_matrix[min_error_pos,2]

    return x, y, min_error




if __name__ == '__main__':
    main()
