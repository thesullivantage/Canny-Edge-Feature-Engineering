import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np

import argparse
import sys
import os


def load_and_recolor_image(image_path, new_cmap='hot'):
    
    
    '''Canny Edge Detection:
    - [The comparision of gradients between borders of pixels] decides which are all edges are really edges and which are not. 
    - For this, we need two threshold values, minVal and maxVal. [hysterisis-based inclusion]
    - Any edges with intensity gradient more than maxVal are sure to be edges and those below minVal are sure to be non-edges, so discarded. 
    - Those who lie between these two thresholds are classified edges or non-edges based on their connectivity. 
        - If they are connected to "sure-edge" pixels, they are considered to be part of edges. 
        - Otherwise, they are also discarded.
    '''
    ### hand tune edge thresholds for individual use case
    edge_threshold1 = 500
    edge_threshold2 = 1250
    
    # Load original image (read in grayscale)
    img_original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Normalize image to 0-1 range (float)
    img_norm = img_original.astype(float) / 255
 
    try:
        # generate colormap
        cmap = plt.get_cmap(new_cmap)
    except Exception:
        # if invalid colormap name entered for mpl, throw:
        print('please enter a valid colormap name.')
        sys.exit(1) 
        ### (see also docs for alternatives mentioned in README.md)   

    ### map grayscale image to colormap
    colored_image = cmap(img_norm)

    ### to 32-bit float
    colored_image = colored_image.astype(np.float32)

    ### convert from rgba to rgb
    colored_image_rgb = cv2.cvtColor(colored_image, cv2.COLOR_RGBA2RGB)
    
    ### convert to 0-255 pixel values for color
    colored_image_rgb = (colored_image_rgb * 255).astype(np.uint8)
    
    ### detect edges in the converted grayscale image using hysteresis; ADJUST THRESHOLDS DEPENDING ON DESIRED RESOLUTION

    edges = cv2.Canny(img_original, edge_threshold1, edge_threshold2)
    
    ### apply dilation filter to blur high contrast edges (steep edge gradients); replace anchor pixel (center, by default) of sliding kernel with largest pixel value in (view of the) current kernel position
    ### NOTE: not necessarily suitable for tasks where features need to remain precisely intact. 
        ### Included here for smoothing of spectrograms for visualization purposes.
    dilated_edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))

    ### make 3-channel RGB mask (length-3 array, each of same dimension as image) to apply on the rgb image
    edge_mask_rgb = np.stack([dilated_edges]*3, axis=-1)

    ### [OPTIONAL] 
    ### edge mask applies near sharp edges, there: restore the original grayscale color in the colored image.
    ### Effect: keep sharp black and white outlines in the current configuration. 
    img_original_rgb = cv2.cvtColor(img_original, cv2.COLOR_GRAY2RGB)

    ### Apply selected pixels from the last step to the already recolored image to effectively retrace solid outlines of image features in B&W
    colored_image_rgb[edge_mask_rgb > 0] = img_original_rgb[edge_mask_rgb > 0]

    ### (Recolor) Floor white and black colors to those corresponding pixel values. 
    colored_image_rgb[img_original == 0] = 0
    colored_image_rgb[img_original == 255] = 255

    return colored_image_rgb

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image-path", type=str, required=True,  help="image path to recolor (relative to current directory).")
    parser.add_argument("--cmap-name", type=str, required=True, help="From Matplotlib: sequential colormap to recolor image to (throws error if not a valid type).")
    parser.add_argument("--output-dir", type=str, default='.', help="path to output directory.")
    parser.add_argument("--test", type=bool, default='.', help="create sample outputs of each perceptually uniform sequential colormap type in the original image directory.")

    if opts.cmap_name is not None and opts.test:
        print('Error: --cmap-name and --test both passed. In --test configuration, all available colormaps from: \
              ['viridis', 'plasma', 'inferno', 'magma', 'cividis'] \
              are output to --output-dir. Try again without passing --cmap-name. 
        )
    
    opts = parser.parse_args()
    
    ### TODO: More extensive I/O testing for image path reading for this util.
    image_path = os.path.join(opts.image_path)

    ### Perceptually Uniform Sequential colormap list (matplotlib)
    cmap_list = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

    if opts.output_dir == '.':
        opts.output_dir = os.getcwd()
        
    imgName = '.'.join(image_path.split('.')[:-1])

    if test == False:
        new_cmap = opts.cmap_name
        ### Conduct recoloring/edge tracing

        colored_image = load_and_recolor_image(image_path, new_cmap)
        outFile = f'{imgName}_recolored_{new_cmap}.png'
        outPath = os.path.join(opts.output_dir, outFile)
        cv2.imwrite(outPath, cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR))
    else: 
        '''
        if we want to see samples of all colormaps that we could use from the above list on our image data,
        use --test True in the command line! Outputs all to the same directory as the input image (FIXME).
        '''
        for c in cmap_list:
            ### Conduct recoloring/edge tracing
            colored_image = load_and_recolor_image(image_path, c)
            outFile = f'{imgName}_recolored_{c}.png'
            outPath = os.path.join(opts.output_dir, outFile)
            # Display the recolored image:
            
            cv2.imwrite(outPath, cv2.cvtColor(colored_image, cv2.COLOR_RGB2BGR))
