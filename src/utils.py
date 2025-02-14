from skimage import data, io, segmentation, color, util, img_as_ubyte
from skimage import graph
import numpy as np
import cv2 as cv
import os
from scipy.spatial import KDTree
from io import BytesIO

predefined_colors = [
    [208, 72, 154],
    [236, 24, 121],
    [236, 28, 35],
    [250, 164, 23],
    [241, 235, 32],
    [154, 201, 59],
    [113, 193, 82],
    [111, 197, 164],
    [59, 184, 235],
    [67, 111, 182],
    [90, 80, 162],
    [134, 80, 160],
    [214, 111, 171],
    [237, 95, 141],
    [240, 90, 65],
    [251, 181, 75],
    [244, 235, 98],
    [173, 211, 96],
    [141, 199, 116],
    [136, 209, 181],
    [109, 192, 236],
    [101, 133, 193],
    [117, 105, 174],
    [154, 108, 177],
    [223, 144, 189],
    [243, 135, 166],
    [243, 134, 99],
    [254, 197, 119],
    [248, 239, 139],
    [191, 222, 135],
    [170, 213, 150],
    [171, 219, 196],
    [149, 207, 242],
    [134, 153, 205],
    [143, 134, 190],
    [171, 137, 190],
    [230, 179, 209],
    [247, 174, 193],
    [248, 168, 141],
    [255, 215, 161],
    [249, 244, 176],
    [212, 228, 174],
    [196, 225, 181],
    [196, 228, 213],
    [183, 221, 244],
    [169, 182, 220],
    [175, 167, 210],
    [196, 171, 211],
    [241, 214, 232],
    [250, 213, 221],
    [253, 210, 191],
    [254, 234, 204],
    [252, 249, 215],
    [231, 241, 212],
    [225, 239, 216],
    [226, 240, 232],
    [220, 236, 250],
    [209, 214, 236],
    [209, 206, 233],
    [222, 210, 229]
]


circle_of_fifths = [
    [1,0,254],
    [102,1,205],
    [102, 0, 153],
    [153,1,103],
    [254,0,1],
    [255,102,0],
    [254,254,0],
    [204,204,0],
    [0,171,1],
    [0,254,152],
    [0,254,152],
    [0,102,255]
]

rgba_colors = [
    (251,214,221,255), (240,213,230,255), (222,210,230,255), (210,206,233,255),
    (208,215,234,255), (222,235,252,255), (227,240,233,255), (224,238,212,255),
    (231,242,210,255), (252,249,216,255), (255,234,205,255), (250,212,191,255),
    (247,174,193,255), (230,179,210,255), (196,171,211,255), (176,167,210,255),
    (170,182,220,255), (183,221,244,255), (196,228,213,255), (196,225,181,255),
    (212,229,175,255), (249,244,176,255), (255,216,161,255), (249,168,141,255),
    (240,137,166,255), (223,144,191,255), (171,138,191,255), (144,135,192,255),
    (134,154,207,255), (149,208,242,255), (171,219,197,255), (172,212,150,255),
    (190,223,136,255), (249,240,139,255), (255,196,115,255), (247,132,103,255),
    (237,95,143,255), (212,112,172,255), (154,109,176,255), (117,106,172,255),
    (99,133,194,255), (112,193,236,255), (142,208,180,255), (141,200,116,255),
    (174,211,95,255), (244,238,92,255), (252,180,78,255), (239,91,65,255),
    (236,24,126,255), (212,70,154,255), (135,80,161,255), (90,81,162,255),
    (67,111,182,255), (65,182,235,255), (113,198,165,255), (113,192,83,255),
    (154,201,59,255), (243,235,30,255), (247,166,25,255), (236,29,35,255)
]

# Extract RGB values, ignoring the alpha channel
rgb_fifths = [[r, g, b] for r, g, b, a in rgba_colors]


def get_contours(image, t_lower, t_upper, cont_thickness, contour_colors=(0, 0, 0)):

    cont_color = contour_colors  # BGR color for contour lines, red in this case

    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(image, (3, 3), 0)
    # Applying the Canny Edge filter
    edge = cv.Canny(blur, t_lower, t_upper)
    contours, hierarchy = cv.findContours(edge, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Create a new black image of the same size as the original
    white_image = np.ones_like(image) * 255

    # Drawing the contours on the black image
    cv.drawContours(white_image, contours, -1, cont_color, cont_thickness)
    buf = BytesIO()

    # Ensure the output directory exists
    #output_dir = 'output_images'
    #if not os.path.exists(output_dir):
    #    os.makedirs(output_dir)

    # Saving the image with contours on black background
    #image_name = os.path.splitext(os.path.basename(image))[0]
    #full_save_path = os.path.join(output_dir, image_name + ' -- contours.png')
    success, output = cv.imencode('.png', white_image)
    buf = BytesIO(output)
    buf.seek(0)
    return buf

    # Displaying the image for verification
    # cv.imshow('Contours', black_image)
    # print("Press any key to close the image window.")
    # cv.waitKey(0)  # Waits indefinitely for a key press
    # cv.destroyAllWindows()  # Closes all the OpenCV windows

def make_black_transparent(image_data, threshold=50):
    # Extract the RGB channels
    r, g, b, a = np.rollaxis(image_data, axis=-1)
    # Create a mask for nearly black pixels
    mask = (r < threshold) & (g < threshold) & (b < threshold)
    # Set the alpha channel to 0 for nearly black pixels
    image_data[mask, 3] = 0
    return image_data

def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}

def closest_predefined_color(mean_color, colors=predefined_colors):
    tree = KDTree(colors)
    _, idx = tree.query(mean_color)
    return colors[idx]

def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])
