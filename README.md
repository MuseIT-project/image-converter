# Image Converter

## Project Overview

This project focuses on converting images to multimodal representations. It provides functionalities to convert image colors to different, predefined, adjacent colors (see transformations section below). It was based on previous work performed on behalf of the University of Boras, by  Andreas Holmstedt.

## Tech stack

- FastAPI
- Sklearn
- Scipy
- Docker (for packaging/containerization)
- Poetry (for dependency management)

## Setting Up

1. Clone the repository:
  ```sh
  git clone https://github.com/yourusername/image-converter.git
  cd image-converter
  ```

2. Run the make commands:
  ```sh
  make build
  make start
  ```

## Makefile Commands

- `make build`: Build and start the project.
- `make start`: Start the project running in a non-detached mode.
- `make startbg`: Start the project running in detached mode (background).
- `make stop`: Stop the running project.
- `make test`: Run unit tests.
- `make copy-poetry-files`: Copy poetry files inside the container.
- `make export-poetry-files`: Export poetry files from inside the container.
- `make update-requirements`: Update poetry requirements and export the lock file.
- `make add-poetry-package package_name=<package_name>`: Add a poetry package using the backend container to resolve.
- `make remove-poetry-package package_name=<package_name>`: Remove a poetry package.
- `make shell`: Enter the system shell in the backend container.
- `make python-shell-be`: Enter into IPython shell in the backend container.
- `make version`: Export version.

## Docker Compose File

The `docker-compose.yml` file defines the services for the application. It includes:

- `image-converter`: The main service that runs the image conversion application. It uses the Dockerfile to build the image and exposes necessary ports.

## Usage

1. Start the container
2. Go either to `https://localhost:8855/docs/` to access the web Swagger docs or use an endpoint directly.
3. Submit images for transformations.

## Transformations available

A number of transformations are available, with varying options. While the API offers some documentation, details are more useful on why these transformations are chosen.

Using the `convert` endpoint, allows you to submit a number of params, with the following effects:

### Parameters

- `output_format`: Specifies the type of transformation to apply. Options include:
  - `colormerge`: Merges colors in the image based on hierarchical clustering.
  - `colormerge_forced`: Similar to `colormerge`, but forces the colors to predefined sets.
  - `contours`: Extracts and draws contours on the image.
  - `combined`: Combines the `colormerge` transformation with contours.
  - `combined_forced`: Combines the `colormerge_forced` transformation with contours.
  - `mesh`: Converts the image to a 3D mesh model.

- `color_format`: Specifies the color set to use when `output_format` is `colormerge_forced` or `combined_forced`. Options include:
  - `fifths`: Uses the `circle_of_fifths` color set.
  - `fifthsv2`: Uses the `rgb_fifths` color set.
  - `predefined`: Uses the `predefined_colors` set.

- `file`: The image file to be transformed.

- `compactness`: Controls the balance between color proximity and space proximity for the SLIC algorithm. Default is 5.

- `n_segments`: Specifies the number of segments for the SLIC algorithm. Default is 2000.

- `thresh`: Threshold value for hierarchical merging of segments. Default is 50.

- `contour_color`: Specifies the color of the contours in BGR format. Default is "255,0,0" (red).

- `t_lower`: Lower threshold for the Canny edge detector. Default is 50.

- `t_upper`: Upper threshold for the Canny edge detector. Default is 130.

- `cont_thickness`: Thickness of the contour lines. Default is 1.




