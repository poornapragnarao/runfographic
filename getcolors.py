
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
def getcolorscmap(basemap, color_ends, pace):
    colormap = cm.get_cmap(basemap, 50)
    reducedmap = ListedColormap(colormap(np.linspace(color_ends[0], color_ends[1], 25)))

    # # Normalize the pace
    N = 25
    all_pace_mean = np.convolve(pace, np.ones((N,))/N)[(N-1):]
    min_pace = min(all_pace_mean)
    max_pace = max(all_pace_mean)
    mean_pace = np.average(pace)
    #norm_paces = [sigmoid(sp, 1, 0.5) for sp in all_data['all_pace']]
    #norm_paces = [(sp-min_pace)*(25 - 1)/(max_pace-min_pace) for sp in all_pace_mean]
    norm_paces = np.tanh(all_pace_mean)
    norm_paces = norm_paces + abs(min(norm_paces))
    max_norm_pace = max(norm_paces)
    min_norm_pace = min(norm_paces)

    return norm_paces, reducedmap