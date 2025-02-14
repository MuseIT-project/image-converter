#!/usr/bin/env python3
#
from utils import (
    merge_mean_color,
    _weight_mean_color,
    closest_predefined_color,
    predefined_colors,
    make_black_transparent
)
from skimage import data, io, segmentation, color, util, img_as_ubyte
from skimage import graph
from io import BytesIO
import numpy as np
from PIL import Image
import cv2
import trimesh
import tempfile
from scipy.spatial import Delaunay

def convert_color_merge(img, compactness, n_segments, thresh):
    labels = segmentation.slic(
        img,
        compactness=compactness,
        n_segments=n_segments,
        start_label=1
    )
    g = graph.rag_mean_color(img, labels)
    labels2 = graph.merge_hierarchical(
        labels,
        g,
        thresh=thresh,
        rag_copy=False,
        in_place_merge=True,
        merge_func=merge_mean_color,
        weight_func=_weight_mean_color
    )
    out_original_colors = color.label2rgb(labels2, img, kind='avg', bg_label=0)
    buf = BytesIO()
    io.imsave(buf, out_original_colors, format='png')
    buf.seek(0)
    return buf

def convert_forced_color_merge(img, compactness, n_segments, thresh, colors=predefined_colors):
    labels = segmentation.slic(
        img,
        compactness=compactness,
        n_segments=n_segments,
        start_label=1
    )
    g = graph.rag_mean_color(img, labels)
    labels2 = graph.merge_hierarchical(
        labels,
        g,
        thresh=thresh,
        rag_copy=False,
        in_place_merge=True,
        merge_func=merge_mean_color,
        weight_func=_weight_mean_color
    )
    output_image = np.zeros_like(img, dtype=np.uint8)
    for region in np.unique(labels2):
        mask = labels2 == region
        mean_color = img[mask].mean(axis=0)
        closest_color = closest_predefined_color(mean_color, colors)
        output_image[mask] = closest_color
    buf = BytesIO()
    io.imsave(buf, output_image, format='png')
    buf.seek(0)
    return buf

def contour_merger(contours, image):
    edge = Image.open(contours).convert('RGBA')
    core = Image.open(image).convert('RGBA')
    edge_data = np.array(edge)
    edge_data = make_black_transparent(edge_data)
    edge_image_transparent = Image.fromarray(edge_data)
    combined_image = Image.alpha_composite(core, edge_image_transparent)
    buf = BytesIO()
    combined_image.save(buf, format='PNG')
    buf.seek(0)
    return buf

def convert_to_3d(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    colors = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0

    heightmap = gray_image / 255.0

    heightmap = heightmap * 0.1

    rows, cols = heightmap.shape
    x = np.linspace(0, 1, cols)
    y = np.linspace(0, 1, rows)
    x, y = np.meshgrid(x, y)
    z = heightmap

    resized_image = cv2.resize(image_rgb, (cols, rows), interpolation=cv2.INTER_LINEAR)
    colors = resized_image.reshape(-1, 3)
    tri = Delaunay(np.c_[x.ravel(), y.ravel()])
    faces = tri.simplices
    points = np.c_[x.ravel(), y.ravel(), z.ravel()]
    mesh = trimesh.Trimesh(vertices=points, faces=faces)
    colors = colors.reshape(-1, 3)
    # mesh.visual.vertex_colors = colors
    mesh.visual.vertex_colors = (colors * 255).astype(np.uint8)
    mesh = trimesh.smoothing.filter_taubin(mesh, iterations=15)

    mesh.apply_transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


    with tempfile.NamedTemporaryFile(suffix=".glb", delete=False) as temp_file:
        temp_filename = temp_file.name
        mesh.export(temp_filename)
    print("file rendered, returning!")
    return temp_filename

def iterfile(filename):
    with open(filename, "rb") as f:
        while chunk := f.read(1024):
            yield chunk
