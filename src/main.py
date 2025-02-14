from skimage import data, io, segmentation, color, util, img_as_ubyte
from skimage import graph
import numpy as np
from typing import Tuple
import cv2 as cv
import os
from io import BytesIO
from scipy.spatial import KDTree
from PIL import Image

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from schema.input import Input, FormatType, ColorType
from utils import (
    predefined_colors,
    circle_of_fifths,
    rgb_fifths,
    closest_predefined_color,
    get_contours,
    make_black_transparent,
    _weight_mean_color,
    merge_mean_color,
)
from converter import (
    convert_color_merge,
    convert_forced_color_merge,
    contour_merger,
    convert_to_3d,
    iterfile
)
from version import get_version

app = FastAPI()


@app.get("/version")
async def info():
    result = get_version()
    return {"version": result}


@app.post("/convert")
def convert_image(
        output_format: FormatType,
        color_format: ColorType,
        file: UploadFile,
        compactness: int = Form(5),
        n_segments: int = Form(2000),
        thresh: int = Form(50),
        contour_color: str = Form("255,0,0"),
        t_lower: int = Form(50),
        t_upper: int = Form(130),
        cont_thickness: int = Form(1),
):
    img = io.imread(file.file)
    if output_format is FormatType.colormerge:
        buf = convert_color_merge(
            img=img,
            compactness=compactness,
            n_segments=n_segments,
            thresh=thresh
        )
    if output_format is FormatType.colormerge_forced:
        if color_format is ColorType.fifths:
            colors = circle_of_fifths
        if color_format is ColorType.fifthsv2:
            colors = rgb_fifths
        else:
            colors = predefined_colors
        buf = convert_forced_color_merge(
            img=img,
            compactness=compactness,
            n_segments=n_segments,
            thresh=thresh,
            colors=colors
        )
    if output_format is FormatType.contours:
        buf = get_contours(image=img, t_lower=t_lower, t_upper=t_upper, cont_thickness=cont_thickness)
    if output_format is FormatType.combined:
        contours = get_contours(image=img, t_lower=t_lower, t_upper=t_upper, cont_thickness=cont_thickness)
        normal = convert_color_merge(
            img=img,
            compactness=compactness,
            n_segments=n_segments,
            thresh=thresh
        )
        buf = contour_merger(
            contours=contours,
            image=normal
        )
    if output_format is FormatType.combined_forced:
        contours = get_contours(image=img, t_lower=t_lower, t_upper=t_upper, cont_thickness=cont_thickness)
        if color_format is ColorType.fifths:
            colors = circle_of_fifths
        if color_format is ColorType.fifthsv2:
            colors = rgb_fifths
        else:
            colors = predefined_colors
        normal = convert_forced_color_merge(
            img=img,
            compactness=compactness,
            n_segments=n_segments,
            thresh=thresh,
            colors=colors
        )
        buf = contour_merger(
            contours=contours,
            image=normal
        )
    if output_format is FormatType.mesh:
        tempfilename = convert_to_3d(image=img)
        return StreamingResponse(
            iterfile(tempfilename),
            media_type='model/obj',
            headers={"Content-Disposition": "attachment; filename=3d_model.glb"}
        )
    return StreamingResponse(buf, media_type="image/png")
