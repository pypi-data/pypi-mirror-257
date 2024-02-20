#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Sun Feb  18 02:37:00 2024

@author: leahghartman

Description : A file containing functions capable of analyzing a full dataset of images.
"""
# import random needed packages that should already be installed
import numpy as np
from PIL import Image

# import from other modules in the package
from single import single_image_proj, single_image_line

#########################
### START OF FUNCTIONS
#########################

def full_set(imglist, xmargins, ymargins, pixelsize=3.45, xpixel=0, ypixel=0):
    """ Returns a list of FWHM values (in microns) for both x- and y-axes as well as a list of images cropped by the analysis function for troubleshooting and/or 
    making movies/animations/GIFs.

        Parameters
        ----------
        imglist : array
            Array of images (this needs to be a set of SORTED image paths (so, 1.tiff, 2.tiff, etc.).
        xmargins : integer
            How many pixels on each side of the beam (in the x-direction; located at the centroid of the image) you'd like as a buffer for cropping.
        ymargins : integer
            How many pixels on each side of the beam (in the y-direction; located at the centroid of the image) you'd like as a buffer for cropping.
        pixelsize : integer
            This function returns FWHM values in microns, which depends on the pixel size of your camera. The default for the CU-PWFA lab is 3.45 microns.
        lineout : boolean
            The user can choose whether they want to use lineouts or projections for full dataset analysis by specifying this variable to be what they want.
    """
    # create empty lists for FWHM in x- and y-directions as well as an empty list for all of the cropped images
    xlist = []
    ylist = []
    croppedimgs = []

    if xpixel == 0 & ypixel == 0:
        # for loop that cycles through all of the images and finds the FWHM along each axis (using PROJECTIONS)
        for i in imglist:
            # find the FWHM in both transverse dimensions as well as the cropped images used for processing
            xFWHM, yFWHM, croppedimg = single_image_proj(xmargins, ymargins, imgar=np.array(Image.open(i)))

            # append everything to their respective empty lists
            croppedimgs.append(croppedimg)
            xlist.append(xFWHM * pixelsize);
            ylist.append(yFWHM * pixelsize);

    else:
         # for loop that cycles through all of the images and finds the FWHM along each axis (using LINEOUTS)
        for i in imglist:
            # find the FWHM in both transverse dimensions as well as the cropped images used for processing
            xFWHM, yFWHM, croppedimg = single_image_line(xmargins, ymargins, xpixel=xpixel, ypixel=ypixel, imgar=np.array(Image.open(i)));

            # append everything to their respective empty lists
            croppedimgs.append(croppedimg)
            xlist.append(xFWHM * pixelsize);
            ylist.append(yFWHM * pixelsize);

    # return everything we want
    return(xlist, ylist, croppedimgs)