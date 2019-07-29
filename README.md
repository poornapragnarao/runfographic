# runfographic

## Introduction:
Runfographic creates visualisations of your Runs(Any GPX activity with tracks).
The visualizations are of the path and colored based on the pace. The colormap can be chosen from any of the available colormaps in matplotlib. Refer - https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html

Similar visualisations can be done in Runtastic and Nike Run App. In Runfographic, 1. your GPS co-ordinates are not stored so your location data is not exposed and 2. Any colormap of your choice can be used for the track.


## Requirements:

1. gpxpy
2. matplotlib
3. numpy

## Usage:

python runfographic.py -f 'filepath to gpx file' -c 'colormap as string'

## Sample path:
The below path was created using 'viridis' colormap - 

![Sample_Path](https://github.com/sigma--/runfographic/blob/master/sample-path.png)
