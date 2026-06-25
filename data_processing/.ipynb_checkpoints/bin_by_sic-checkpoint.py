#### Bins sea ice concentration (SIC) into specified bins and returns bin means as well as the 95% confidence interval for each bin

import numpy as np
from scipy import stats

#### Parameters ####
## var_bins: variable that is used to define bins (e.g. SIC) (numpy array)
## var_binned: variable that is binned based on var_bins (numpy array) 
## ** var_bins and var_binned must be aligned (ideally both should be in the same dataframe)
## bin_n: number of bins (int)
## sample_exception: True for no restriction on sample size (boolean)

#### Returns ####
## bin_means: mean from each bin in the form of an array
## ci_l: lower bound confidenc eintervalfrom each bin in the form of an array
## ci_h: upper bound confidenc eintervalfrom each bin in the form of an array

def bin_by_sic(var_bins,var_binned,bin_n,sample_exception):
    
    valid = np.isfinite(var_bins) & np.isfinite(var_binned)
    var_bins   = var_bins[valid]
    var_binned = var_binned[valid]

    ## define bin edges
    edges = np.linspace(0, 100, bin_n + 1)
    print(edges)

    bin_means = []
    ci_l = []
    ci_h = []

    ## loop through bins and calculate means and confidence intervals
    for i in range(bin_n):

        b = (var_bins >= edges[i]) & (var_bins < edges[i+1])

        n = np.sum(b)

        if n < 5 and not sample_exception:
            bin_means.append(np.nan)
            ci_l.append(np.nan)
            ci_h.append(np.nan)
            continue

        mean = np.nanmean(var_binned[b])

        sem = stats.sem(var_binned[b], nan_policy='omit')
        if n > 1:
            ci_low, ci_high = stats.t.interval(0.95, n-1, loc=mean, scale=sem)
        else:
            ci_low, ci_high = np.nan, np.nan

        bin_means.append(mean)
        ci_l.append(ci_low)
        ci_h.append(ci_high)

    return np.array(bin_means), np.array(ci_l), np.array(ci_h)

