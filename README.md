## Webcam timing
![ubuntu22_ps3eye](https://github.com/arthurkehrwald/webcam-timing/assets/50906979/add2221c-12eb-41a4-b14e-82d86c105d26)

### Usage
1. Connect a webcam to your computer
2. Create a virtual environment with a Python 3.10 interpreter
3. Run `pip install -r requirements.txt` to install dependencies
4. Run `measure.py`
- Plots of existing csv files can be shown by running `plot.py` with the path to the file as argument
- Stats of existing csv files can be shown by running `analyze.py` with the path to the file as argument

### Operation
- Uses OpenCV to read specified number of frames from the webcam
- Measures time between frames
- Saves frame times in .csv file
- Logs statistics (e.g. frames per second, mean deviation) to console
- Shows plot
