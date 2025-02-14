from fastapi.testclient import TestClient
from main import app, iterfile

client = TestClient(app)

def test_convert_image_colormerge():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            data={
                "compactness": "5",
                "n_segments": "2000",
                "thresh": "50",
                "contour_color": "255,0,0",
                "t_lower": "50",
                "t_upper": "130",
                "cont_thickness": "1"
            },
            params={"color_format": "default", "output_format": "colormerge"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_convert_image_colormerge_forced():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            data={
                "compactness": 5,
                "n_segments": 2000,
                "thresh": 50
            },
            params={"color_format": "fifths", "output_format": "colormerge_forced"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_convert_image_contours():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            data={
                "t_lower": 50,
                "t_upper": 130,
                "cont_thickness": 1
            },
            params={"output_format": "contours", "color_format": "default"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_convert_image_combined():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            data={
                "compactness": 5,
                "n_segments": 2000,
                "thresh": 50,
                "contour_color": "255,0,0",
                "t_lower": 50,
                "t_upper": 130,
                "cont_thickness": 1
            },
            params={"color_format": "default", "output_format": "combined"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_convert_image_combined_forced():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            data={
                "compactness": 5,
                "n_segments": 2000,
                "thresh": 50,
                "contour_color": "255,0,0",
                "t_lower": 50,
                "t_upper": 130,
                "cont_thickness": 1
            },
            params={"color_format": "fifthsv2", "output_format": "combined_forced"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_convert_image_mesh():
    with open("/root/src/tests/test_image.jpg", "rb") as img_file:
        response = client.post(
            "/convert",
            files={"file": ("test_image.jpg", img_file, "image/jpeg")},
            params={"output_format": "mesh", "color_format": "default"}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "model/obj"

def test_iterfile():
    with open("/root/src/tests/test_file.txt", "w") as f:
        f.write("This is a test file.")
    with open("/root/src/tests/test_file.txt", "rb") as f:
        iterator = iterfile(f.name)
        content = b"".join(iterator)
        assert content == b"This is a test file."