## Takes data from bin_by_sic script and plots a single line with 95% confidence interval bars
## To create the plots in the manuscipt simply loop through this function for different sea ice estimates and variables
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

## ax: Axis for plotting (ax object)
## x: x-axis data (should be 10 bins from 0-100 if using output from bin_by_sic script) (list/array)
## y_mean: mean data from bin_by_sic (numpy array)
## x_offset: offset on x-axis so CI bars don't overlap (int/float)
## y_ci_high: high CI data from bin_by_sic (numpy array)
## y_ci_low: low CI data from bin_by_sic (numpy array)
## x_label: SIC estimate (String)
## color: color of line (String)

def binned_dep(ax, x, y_mean, x_offset, y_ci_high, y_ci_low, x_label, color):
                         
    ax.errorbar(x+x_offset, y_mean, yerr=np.vstack([y_mean - y_ci_low, y_ci_high - y_mean]),
            label=x_label, fmt='-s',alpha=0.7,c='blue', capsize=5,linewidth=2)

