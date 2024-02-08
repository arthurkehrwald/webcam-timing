## Webcam timing
![ubuntu22_ps3eye](https://github.com/arthurkehrwald/webcam-timing/assets/50906979/add2221c-12eb-41a4-b14e-82d86c105d26)

Measure, analyze, and plot webcam frame timings.

### Features
- Supports most USB webcams and Luxonis Oak cameras
- Measures time between frames
- Saves frame times in .csv file
- Logs statistics (e.g. frames per second, mean deviation) to console
- Shows plot

### Setup
1. Create a virtual environment with a Python 3.10 interpreter
2. Run `pip install -r requirements.txt` to install dependencies
3. Configure the program for your camera by editing `create_camera.py`. Use the `OpenCvCamera` class for standard UVC webcams (e.g. Logitech C270) and the `OakCamera` class for Luxonis Oak cameras. If your camera is not supported, you can add support yourself by implementing the abstract base class `CameraBase`. Pull requests welcome!

### Usage
- Run `measure.py` to create a .csv file containing the delays between frames
- Plots of existing csv files can be shown by running `plot.py` with the path to the file as argument
- Stats of existing csv files can be shown by running `analyze.py` with the path to the file as argument
- Run `display.py` to see the video stream of the camera. This is useful for troublehooting

