import gpxpy
import gpxpy.gpx
import math

DIST_BETWEEN_PACE = 100 #metres
r = 6371000 # meters
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60
M_IN_KM = 1000
SPLIT_DIST_M = 1000 #metres
def to_xy(point, r, cos_phi_0):
    lam = point[0]
    phi = point[1]
    return (r * math.radians(phi), r * math.radians(lam) * cos_phi_0)

def get_time_diff(prev_point, point, unit):
    if prev_point.time.hour > point.time.hour:
        diff_hour = prev_point.time.hour - 24
    else:
        diff_hour = prev_point.time.hour
    time_diff_hour = (point.time.hour-diff_hour)
    time_diff_min  = (point.time.minute-prev_point.time.minute)
    if prev_point.time.second < point.time.second:
        time_diff_s = point.time.second - prev_point.time.second
    else:
        time_diff_s = (SECONDS_IN_MINUTE - prev_point.time.second) + point.time.second
        time_diff_min = time_diff_min - 1
    if unit == 'min':
        return time_diff_hour*MINUTES_IN_HOUR + time_diff_min + time_diff_s/SECONDS_IN_MINUTE
    elif unit == 's':
        return time_diff_hour*MINUTES_IN_HOUR*SECONDS_IN_MINUTE + time_diff_min*SECONDS_IN_MINUTE + time_diff_s
    else:
        return 'ERROR'

def mydiv(d1,d2):
    if d2 == 0:
        return 0
    else:
        return d1/d2

def getalldata(filepath):
    gpx_file = open(filepath, 'r')
    gpx = gpxpy.parse(gpx_file)
    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx.get_moving_data()
    dist_pace_calc = 0
    dist_split_calc = 0
    split_distance = 0
    split_pace = []
    split_dist = []
    graph_distance = 0
    graph_speed = []
    graph_dist = []
    all_pace = []
    all_elev = []
    all_points_x = []
    all_points_y = []
    dist_bw_pts = []
    all_hr = []
    def_origin = 1
    # Get all x,y points and speed
    for track in gpx.tracks:
        for segment in track.segments:
            for point_no, point in enumerate(segment.points):        
                pointxy = to_xy((point.latitude, point.longitude), r, math.sin(math.radians(point.longitude)))
                if def_origin:
                    origin = pointxy
                    origin_latlong = point
                    prev_point_graph = origin_latlong
                    prev_point_split = origin_latlong
                    start_point = point
                    def_origin = 0
                else:
                    end_point = point
                    dist_from_prev = gpxpy.geo.distance(segment.points[point_no-1].latitude,segment.points[point_no-1].longitude, segment.points[point_no-1].elevation, 
                                        point.latitude, point.longitude, point.elevation, haversine=True)
                    dist_bw_pts.append(dist_from_prev)
                    dist_pace_calc = dist_pace_calc + dist_from_prev
                    dist_split_calc = dist_split_calc + dist_from_prev
                    time_diff = get_time_diff(segment.points[point_no-1], point,'s')
                    all_pace.append(mydiv(time_diff, dist_from_prev))
                    all_elev.append(point.elevation)
                    all_points_x.append(pointxy[0] - origin[0])
                    all_points_y.append(pointxy[1] - origin[1])
                    if dist_pace_calc > DIST_BETWEEN_PACE:
                        graph_distance = graph_distance + dist_pace_calc
                        time_diff = get_time_diff(prev_point_graph, point,'s')
                        m_per_s = mydiv(dist_pace_calc, time_diff)
                        graph_speed.append(m_per_s)
                        graph_dist.append(graph_distance)
                        dist_pace_calc = 0
                        prev_point_graph = point
                    if dist_split_calc > SPLIT_DIST_M:
                        split_distance = split_distance + dist_split_calc
                        time_diff = get_time_diff(prev_point_split, point, 'min')
                        min_per_selected_split = mydiv(time_diff, (dist_split_calc/M_IN_KM))
                        split_pace.append(min_per_selected_split)
                        split_dist.append(split_distance)
                        dist_split_calc = 0
                        prev_point_split = point
                    for ext in point.extensions:
                        for child in ext:
                            if 'hr' in child.tag:
                                all_hr.append(int(child.text))

    total_time = (moving_time+stopped_time)/SECONDS_IN_MINUTE#get_time_diff(start_point, end_point, 'min')
    ret_dict = {'all_pace':all_pace,'all_elev':all_elev,'all_hr':all_hr, 'all_dist':dist_bw_pts,
            'graph_speed':graph_speed, 'graph_dist':graph_dist,
            'split_pace':split_pace,'split_dist':split_dist, 'all_x':all_points_x,'all_y':all_points_y,'total_time':total_time,
            'moving_dist':moving_distance, 'moving_time':moving_time}
    return ret_dict


