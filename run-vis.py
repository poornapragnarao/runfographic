import gpxpy
import gpxpy.gpx
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def to_xy(point, r, cos_phi_0):
    lam = point[0]
    phi = point[1]
    return (r * math.radians(phi), r * math.radians(lam) * cos_phi_0)

filepath = 'D:/dev/gpx-parse/activities/Auroville.gpx'
color_gradient = ['#0CE500', '#24E601', '#3CE702', '#54E803', '#6CEA04', '#85EB05', '#9DEC06', '#B6EE07', '#CEEF08', '#E7F009', '#F2E40B', '#F3CE0C', '#F4B80D', '#F6A20E', '#F78C0F', '#F87611', '#FA6012', '#FB4A13', '#FC3414', '#FE1D15']
num_colors = len(color_gradient)
r = 6371000 # meters

gpx_file = open(filepath, 'r')
filename = str.split(filepath, '/')
filename = filename[len(filename)-1]
filename = str.split(filename,'.')
gpx = gpxpy.parse(gpx_file)
def_origin = 1
all_points_x = []
all_points_y = []
all_speeds = []
all_pace = []
all_elev = []
# Get all x,y points and speed
for track in gpx.tracks:
    for segment in track.segments:
        for point_no, point in enumerate(segment.points):           
            pointxy = to_xy((point.latitude, point.longitude), r, math.sin(math.radians(point.longitude)))
            if def_origin:
                origin = pointxy
                def_origin = 0
            else:
                all_points_x.append(pointxy[0] - origin[0])
                all_points_y.append(pointxy[1] - origin[1])
                curr_speed = point.speed_between(segment.points[point_no - 1])
                all_speeds.append(curr_speed)
                if curr_speed > 0:
                    all_pace.append(1/(point.speed_between(segment.points[point_no - 1])))
                else:
                    all_pace.append(0)
            all_elev.append(point.elevation)

# Print details of gpx file
print('date - '+str(gpx.time.day)+' '+str(gpx.time.month)+' '+str(gpx.time.year))

# Normalize the speeds
N = 40
all_pace_mean = np.convolve(all_pace, np.ones((N,))/N)[(N-1):-N]
all_speeds_mean = np.convolve(all_speeds, np.ones((N,))/N)[(N-1):-N]
plt.plot(all_speeds_mean)
plt.show()
min_speed = min(all_speeds_mean)
max_speed = max(all_speeds_mean)
norm_speeds = [(sp-min_speed)*(num_colors - 1)/(max_speed-min_speed) for sp in all_speeds_mean]

# Normalize and make points positive
minx = min(all_points_x)
miny = min(all_points_y)
allmin = abs(min([minx, miny]))
allx = [x+allmin for x in all_points_x]
ally = [y+allmin for y in all_points_y]

# Get color list according to speeds
color_list = [color_gradient[int(c)] for c in norm_speeds]

# Start plotting
plt.figure()
plt.subplot(211)
print('Plotting...')
plt.axis('off')
plt.scatter(allx,ally, color=color_list, s=10)#, markersize=4)


# Debug
num_points = len(all_points_x)
plt.subplot(212)
plt.axis('off')
plt.plot(all_elev[0:num_points])
plt.ylim(ymax = max(all_elev[0:num_points]), ymin = min(all_elev[0:num_points]))
x=list(np.linspace(0,num_points,num_points))
plt.bar(x=x,height=all_elev[0:num_points], color=color_list[0:num_points], linewidth=0, width = 1.0)

plt.savefig(filename[0]+'.png', facecolor='black',edgecolor='white',dpi=400)
print('Saved to '+filename[0]+'.png')
plt.show()
