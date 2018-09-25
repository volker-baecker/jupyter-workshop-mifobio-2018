# coding: utf-8
"""
@author:    CEDRIC HASSEN-KHODJA @ MRI @ MONTPELLIER

@descript:  This is the 'batch' version of the tutorial pipeline solutions for
            the MIFOBIO 2018 workshop.
            It was exported from the jupyter notebook and then modified so it
            can be used for batch processing.
"""

# SETUP AND IMPORTS
from __future__ import division
import numpy as np
import scipy.ndimage as ndi

#------------------------------------------------------------------------------

# PIPELINE FUNCTION

def run_pipeline(filename_1, filename_2, filename_3):

    # Report
    print '\nWORKING ON IMAGES:', filename_1, '/', filename_2, '/', filename_3

    #--------------------------------------------------------------------------

    # # Importing & Handling Image Data
    
    # (i) Specify the filename
    # (ii) Load the images
    # Import the function 'imread' from the module 'skimage.io'
    from skimage.io import imread
    
    # Load 'FITC.jpeg' and store it in a variable.
    # Suggested name for the variable: fitc
    fitc = imread(filename_1)
    
    # Load 'Hoechst.jpeg' and store it in a variable.
    # Suggested name for the variable: hoechst
    hoechst = imread(filename_2)
    
    # Load 'Tritc.jpeg' and store it in a variable.
    # Suggested name for the variable: tritc
    tritc = imread(filename_3)
    
    # (iii) Check the data represention of the images
    # Check that 'fitc', 'hoechst', 'tritc' is a variable of type 'ndarray' - use Python's built-in function 'type'.
    print("Fitc is of type:"),type(fitc)
    print("Hoechst is of type:"),type(hoechst)
    print("Tritc is of type:"),type(tritc)
    
    # Print the shape of the array using the numpy-function 'shape'. 
    print("Fitc has shape:"),fitc.shape
    print("Hoechst has shape:"),hoechst.shape
    print("Tritc has shape:"),tritc.shape
    
    # Check the datatype of the individual numbers in the array. You can use the array attribute 'dtype' to do so.
    print("Fitc values are of type:"),fitc.dtype
    print("Hoechst values are of type:"),fitc.dtype
    print("Tritc values are of type:"),tritc.dtype
    
    #(iv) Normalize images
    info = np.iinfo(hoechst.dtype)
    hoechst = hoechst.astype(np.float64) / info.max
    info = np.iinfo(fitc.dtype)
    fitc = fitc.astype(np.float64) / info.max
    info = np.iinfo(tritc.dtype)
    tritc = tritc.astype(np.float64) / info.max
    
    # (v) Look at the images to check that all is OK.
    
    # (v) Create a composite image.
    from skimage.color import gray2rgb
    
    fitc_rgb = gray2rgb(fitc)
    hoechst_rgb = gray2rgb(hoechst)
    tritc_rgb = gray2rgb(tritc)
    
    tritc_green = tritc_rgb * [0,1,0]
    hoechst_blue = hoechst_rgb * [0,0,1]
    fitc_red = fitc_rgb * [1,0,0]
    
    composite = tritc_green + hoechst_blue + fitc_red
    
    # # Computing nuclei mask
    
    # ## Preprocessing
    
    # ### Median filtering
    
    # (i) Create a variable for the size of smoothing filter. 
    size = 5
    
    # (ii) Perform the smoothing on the image
    hoechst_smooth = ndi.filters.median_filter(hoechst,size)
    
    # (iii) Visualize the result using plt.imshow and plt.show
    
    # ### Global Thresholding
    
    #(i) Threshold the median-smoothed original image using the otsu method to obtain the nuclei mask.
    from skimage.filters import threshold_otsu
    
    nmask = np.zeros(hoechst_smooth.shape, dtype = bool)
    nmask[hoechst_smooth > threshold_otsu(hoechst_smooth)] = 1
    
    # (ii) Visualize the result using plt.imshow and plt.show
    
    # ### Improving Masks with Binary Morphology
    
    # (i) Create a diamond-shaped structuring element and asign it to a new variable.
    from skimage.morphology import diamond
    se = diamond(1)
    
    # (ii) Try morphological operations to further improve the membrane mask
    from skimage.morphology import closing
    from skimage.morphology import opening
    
    nmask = opening(closing(nmask, se),se)
    nmask = ndi.binary_fill_holes(nmask)
    
    # (iii) Visualize the result using plt.imshow and plt.show
    
    # # Computing cell mask
    
    # (i) Adjust Brightness and Contrast
    ntritc = tritc * 2.82 - 0.17
    nfitc = fitc * 5.03 - 0.35
    nhoechst = hoechst * 2.99 - 0.15
    
    #(ii) Visualize the result after create a mix image using plt.imshow and plt.show
    mix = nfitc+ntritc+nhoechst
    
    #(iii) Do you improve the light of the image by playing with the gamma.
    mix_2 = (nfitc**2+ntritc**2+nhoechst**2)**0.5
    
    #(iv) Visualize the result
    
    # ### 2d convolution filter
    
    # (i) Create a cross-shaped structuring element and asign it to a new variable.
    se = np.matrix([[0,1,0],[1,2,1],[0,1,0]], dtype='float')/6
    
    # (ii) import signal from scipy to get the convolve2d function for execute the 2d convolution filter on the image. 
    from scipy import signal
    
    cmask = signal.convolve2d(mix_2, se, boundary="wrap", mode="same") >= 0.12
    
    #(iii) display the result
    # (iii) Create a diamond-shaped structuring element and asign it to a new variable.
    se = diamond(1)
    
    # (iv) Use morphology operation like closing to improve image
    cmask = closing(cmask, se)
    
    # # segmenting nuclei using watershed
    # (i) Distance transform on thresholded membranes
    dist_transf = ndi.distance_transform_edt(nmask)
    
    # (ii) Visualize the output and understand what you are seeing.
    # (iii) Dilate the distance threshold
    i = 10
    struct = (np.mgrid[:i,:i][0] - np.floor(i/2))**2 + (np.mgrid[:i,:i][1] - np.floor(i/2))**2 <= np.floor(i/2)**2
    dist_trans_dil = ndi.filters.maximum_filter(dist_transf, footprint=struct) 
    
    # (iv) Retrieve the local maxima (the 'peaks') in the distance transform
    from skimage.feature import peak_local_max
    seeds = peak_local_max(dist_trans_dil, indices=False, min_distance=10)
    
    # (v) Visualize the output
    # (vi) Label the seeds
    seeds_labeled = ndi.label(seeds)[0]
    
    # (vii) Perform watershed
    from skimage.morphology import watershed
    ws = watershed(hoechst_smooth,seeds_labeled)
    
    # (viii) Show the result as transparent overlay over the smoothed input image
    
    # # segmenting cells using Voronoi tesselation
    
    # (i) The label function from skimage.measure module finds every 
    #connected set of pixels other than the background, 
    from skimage.measure import label
    markers_nuc = label(nmask, connectivity=2, return_num=True)
    
    # (ii) We apply a sobel filter from skimage.filters to detect edges from cell body and serve as input 
    # for the voronoi tesselation algorithm. 
    from skimage.filters import sobel
    
    fsobel = np.empty_like(mix_2)
    fsobel = sobel(mix_2)
    
    # (iii) Visualize the output
    # (iv) This algo is implemented in centrosome package, an open source image processing library.
    from centrosome.propagate import propagate
    cell_seg,_ = propagate(image=fsobel, labels=markers_nuc[0], mask=cmask, weight=1)
    
    # (v) Visualize the output. Focus on boundaries between labeled 
    # regions highlighted thanks to mark_boundaries from skimage.segmentation and draw contour lines 
    # for nuclei thanks to contour from matplotlib.pyplot.
    
    
    # # Quantification of cell features
    
    # (i) Create a dictionary that contains a key-value pairing for each measurement
    results = {"cell_id":[],
               "cell_tubulin_mean":[],
               "cell_actin_mean":[],
               "cell_area":[]}
    
    # (ii) Record the measurements for each cell
    # Iterate over cell IDs
    for cell_id in np.unique(cell_seg)[1:]:
    
        # Mask the current cell
        cell_mask = cell_seg==cell_id
        
        # Get the measurements
        results["cell_id"].append(cell_id.item())
        results["cell_area"].append(np.sum(cell_mask).item())
        results["cell_tubulin_mean"].append(np.mean(tritc[cell_mask]).item())
        results["cell_actin_mean"].append(np.mean(fitc[cell_mask]).item())

# (iii) Print the results and check that they make sense
#for key in results.keys(): print key, '\n', results[key], '\n'

#--------------------------------------------------------------------------

    # RETURN OUTPUT

    return cell_seg, results

#------------------------------------------------------------------------------