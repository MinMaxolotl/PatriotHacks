import numpy as np
import skimage as ski
from scipy.interpolate import interp1d
# from HSL import rgb_to_hsl
from skimage.color import rgb2hsv
from PIL import Image

# Import an image of jpg, png, bmp, jpec, hvic through skimage
# Input is something like 'tree.png'
# Temporary images become .png files
# By default color photos are pulled as RGB, and have values [0, 255] as floats
def input_photo(input_name):
    image = np.array(ski.io.imread(input_name))
    # display = Image.fromarray(image)
    # display.show()
    # print(image)
    return image

# Test input_photo
# image = input_photo('max.jpg')

# image_grey = ski.color.rgb2gray(image)
# image_grey = ski.feature.canny(image_grey, 1)
# display = Image.fromarray(image_grey)
# display.show()

# Function for number of pixels in image
# def num_pixels(image):
#     width = len(image[0,:])
#     height = len(image[:,0])
#     return width*height

# Test num_pixels
# print(num_pixels(image))

# Pull average RGB Values out of image
# Returns list of average values in format [RED, GREEN, BLUE]
def RGB_avg(image):
    red_avg = image[:,:,0].mean()
    green_avg = image[:,:,1].mean()
    blue_avg = image[:,:,2].mean() 

    return [red_avg, green_avg, blue_avg]

#print(RGB_avg(image))
    
# Gathers HSV averages
# Returns list of average values in format [HUE, SATURATION, VALUE]
def HSV_avg(image):
    hsv_img = rgb2hsv(image)
    hue_avg = hsv_img[:,:,0].mean() * 255
    saturation_avg = hsv_img[:,:,1].mean() * 255
    value_avg = hsv_img[:,:,2].mean() * 255

    return [hue_avg, saturation_avg, value_avg]

# Gathers HSL averages
# Returns list of average values in format [HUE, LIGHT, SATURATION]
# Significantly slower than HSV. Not primarily used
# def HSL_avg(image):
#     hsl_img = np.zeros_like(image)
#     num_rows = image.shape[0]
#     num_cols = image.shape[1]
    
#     for row in range(num_rows):
#         for col in range(num_cols):
#             ONE_255 = 1.0 / 255.0
#             h, s, l = rgb_to_hsl(image[row, col, 0] * ONE_255, image[row, col, 1] * ONE_255, image[row, col, 2] * ONE_255)
#             hsl_img[row, col, 0] = (h / ONE_255)
#             hsl_img[row, col, 1] = (s / ONE_255)
#             hsl_img[row, col, 2] = (l / ONE_255)

#     hue_avg = hsl_img[:,:,0].mean()
#     saturation_avg = hsl_img[:,:,1].mean()
#     light_avg = hsl_img[:,:,2].mean()

#     return [hue_avg, saturation_avg, light_avg]

#print(HSV_avg(image))

# Function to convert average values to spotify values
# Returns feature values
def photo2features(image):
    img = input_photo(image)
    r, g, b = RGB_avg(img)
    h, s, v = HSV_avg(img)

    color_features = np.array([r,g,b,h,s,v])
    
    remap =             interp1d([0,765],[0,1])
    acoustincess =      float(remap(max(0.000001, g + b - r)))
    remap =             interp1d([0,510],[0,1])
    danceability =      float(remap(max(0.000001, v + s)))
    remap =             interp1d([0, 870],[0,1])
    energy =            float(remap(max(0.000001, r + v - h)))
    remap =             interp1d([0, 1020],[0,1])
    instrumentalness =  float(remap(max(0.000001, v - s + g -r)))
    remap =             interp1d([0, 510],[0,1])
    valence =           float(remap(max(0.000001, v - b)))

    return np.array([acoustincess, danceability, energy, instrumentalness, valence]), color_features

# Test photo2features
# print(photo2features(image))
