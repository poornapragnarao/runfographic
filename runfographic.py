import gpxdata
import getcolors
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import accumulate

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", help='filepath of the GPX file', type=str)
parser.add_argument("-c", help='color map entered as string. See matplotlib colormaps for options.', default='hsv', type=str)
args = parser.parse_args()
color_map = args.c

filepath = args.f
print('path is - ' + filepath)
filename = str.split(filepath, '/')
filename = filename[len(filename)-1]
filename = str.split(filename,'.')

if filename[1] != 'gpx':
    print('Not GPX file!')
    exit()

NUM_COLORS = 25
M_TO_KM = 1000

all_data = gpxdata.getalldata(filepath)
cumulative_dist = list(accumulate(all_data['all_dist']))
cumulative_dist = [x/M_TO_KM for x in cumulative_dist]
all_data['graph_dist'] = [x/M_TO_KM for x in all_data['graph_dist']]
all_data['split_dist'] = [x/M_TO_KM for x in all_data['split_dist']]
full_dist = all_data['moving_dist']/M_TO_KM
average_pace = all_data['total_time']/full_dist
average_pace_min = int(average_pace)
average_pace_s = int((average_pace - average_pace_min)*60)
hr_available = len(all_data['all_hr']) > 0
# Make points positive
minx = min(all_data['all_x'])
miny = min(all_data['all_y'])
allmin = abs(min([minx, miny]))
allx = [x+allmin for x in all_data['all_x']]
ally = [y+allmin for y in all_data['all_y']]


# Get colors
norm_paces, norm_cmap = getcolors.getcolorscmap(color_map, [1.0, 0.0], all_data['all_pace'])


# Create visualisations
### Track Plot ###
track_plt, ax = plt.subplots()#(1, 1, 1, facecolor='b') # nrows, ncols, index
plt.axis('off')

# Draw all GPS points
#norm = mpl.colors.Normalize(vmin=min(norm_paces), vmax=max(norm_paces))
sc_plot = plt.scatter(allx,ally,s=5,c=norm_paces,cmap=norm_cmap)#, norm=norm)#, 

# Draw start and end points
plt.scatter(allx[0],ally[0], s=25,c='white')
plt.scatter(allx[0],ally[0], s=12,c=norm_cmap.colors[0])
plt.scatter(allx[-1],ally[-1], s=25,c='white')
plt.scatter(allx[-1],ally[-1], s=12,c=norm_cmap.colors[-1])
ax.set_aspect('equal')
ax.set_facecolor('grey')

# Stats display at bottom
string1 = str(average_pace_min)+":"+ "%0*d" % (2,average_pace_s) + 'min/km'
dist = cumulative_dist[-1]
string2 = '        '+"%0.2f" % dist + 'km'
if hr_available:
    string3 = '        '+str(int(np.mean(all_data['all_hr'])))+'bpm'
else:
    string3 = ''

s = string1+string2+string3
text_xy = (0.5,0)
font = {'fontname':'Monospace'}
ax.text(0.5, 0, s, fontsize=12,c='white',bbox=dict(facecolor='grey', alpha=0.5,boxstyle='round,pad=0.5'),
        transform=ax.transAxes, ha="center", va="top", **font)

# Save the figure
track_plt.savefig(filename[0]+'.png', facecolor='xkcd:dark grey',edgecolor='white',dpi=400)
print('Saved to ' + filename[0] + '.png')


### Graphs ###

graph_plt = plt.figure()

#plt.axis('off')

# Elevation
plt.subplot(221)
plt.title('Elevation')
plt.xlabel('Distance')
plt.ylabel('Metres')
plt.ylim(ymax = max(all_data['all_elev']), ymin = min(all_data['all_elev']))
plt.plot(cumulative_dist,all_data['all_elev'])
num_points = len(all_data['all_elev'])
min_pace = min(norm_paces)
max_pace = max(norm_paces)
num_colors = len(norm_cmap.colors)
new_norm_paces = [(sp-min_pace)*(num_colors - 1)/(max_pace-min_pace) for sp in norm_paces]
new_colors = [norm_cmap.colors[int(x)] for x in new_norm_paces]
#plt.bar(x=cumulative_dist,height=all_data['all_elev'], color=new_colors, linewidth=0, width = 0.01)

# Heart rate
plt.subplot(222)
plt.title('HR')
plt.xlabel('Distance')
plt.ylabel('Beats per minute')
if hr_available:
    plt.plot(cumulative_dist,all_data['all_hr'])
else:
    plt.text(0.35,0.5, 'No HR Data')

# Speed
plt.subplot(223)
plt.title('Speed')
plt.xlabel('Distance')
plt.ylabel('km/hr')
all_data['graph_speed'] = [x*3.6 for x in all_data['graph_speed']]
plt.plot(all_data['graph_dist'], all_data['graph_speed'])

# Splits
plt.subplot(224)
plt.title('Splits pace')
plt.xlabel('Distance')
plt.ylabel('min/km')
plt.bar(x=all_data['split_dist'],height=all_data['split_pace'],width=0.5)

plt.tight_layout()

# Save the figure
plt.savefig(filename[0]+'_graphs.png',edgecolor='white',dpi=400)
print('Saved to ' + filename[0]+'_graphs.png')

# Show the figures
graph_plt.show()
track_plt.show()

# Wait for user input
input()