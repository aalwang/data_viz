## This script is used to create scatter plots with color contoured data points (if desired)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
import scipy.stats

## Function to automatically assign levels to data (used to assign x and y ticks)
def find_levels(x,y,n):
    if y is not None:
        low = min([np.nanmin(x), np.nanmin(y)])
        high = max([np.nanmax(x), np.nanmax(y)])
    elif y is None:
        low = math.floor(np.nanmin(x))
        high = math.ceil(np.nanmax(x))
    levels = np.linspace(low, high, n+1)
    levels = np.round(levels).astype(int)
    return levels

## axes: Axis for plotting (ax object)
## dataA: data for x-axis (numpy array)
## dataB: data for y-axis (numpy array) ** dataA and dataB should be same length and aligned
## cont_field: Field to contour on scatter ("None" if no contour is desired)
## labA: label for x-axis (string)
## labB: label for  y-axis (string)
## lab_cont: label for contour field (string)
## n: number of desired levels for x and y axis (int)
## levels: levels for contour field (list)
## title: plot title (string)
## save_as: save file name, include format (string; e.g. the_name.png)
## same_var: True when comparing the same variable from two different datasets (boolean)
## stats: if True stats are calculated and displayed on plot (boolean)
## bootstrap: if True bootstrap statistics are calculated (boolean)
## boot_shade: if True the bootstrapped 95% confidence interval of the linear regression is plotted 


def scatter_contour_plot(axes,dataA,dataB,cont_field,labA,labB,lab_cont,n,levels,title, color, save_as, same_var, stats, bootstrap, boot_shade):

    norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=256)
    if cont_field is None:
        scat = axes.scatter(dataA,dataB,c=color,s=80, alpha=0.5)
    else:
        scat = axes.scatter(dataA,dataB,c=cont_field,norm=norm,s=80)
    
    if same_var == True:
        axes.set_xticks(find_levels(dataA,dataB,n))
        axes.set_yticks(find_levels(dataA,dataB,n))
        axes.plot(find_levels(dataA,dataB,n),find_levels(dataA,dataB,n), c='k',lw=4)
    elif same_var == False:
        axes.set_xticks(find_levels(dataA,None,n))
        axes.set_yticks(find_levels(dataB,None,n))
    axes.grid(True, linestyle='--', alpha=0.8)
    axes.tick_params(axis='both', labelsize=28)
    axes.tick_params(axis='both', which='major', length=5, width=2)
    axes.set_xlabel(labA,fontsize=36)
    axes.set_ylabel(labB,fontsize=36)
    #axes[0].plot(np.arange(-40,320,5),np.arange(-40,320,5),c='k')

    ## Add best fit line
    ## mask nans
    mask = np.isfinite(dataA) & np.isfinite(dataB)
    
    ## make sure data is long enough and realistic
    if len(dataA[mask]) > 2 and np.std(dataA[mask]) > 0:
        z = np.polyfit(dataA[mask], np.array(dataB)[mask],1 )
        p = np.poly1d(z)

        x_fit = np.linspace(np.min(dataA[mask]), np.max(dataA[mask]), 200)
        axes.plot(dataA[mask], p(dataA[mask]), c='red', lw=4)

        if stats==True and bootstrap==False:
            axes.text( 0.02, 0.90, f"y={z[0]:.2f}x+{z[1]:.2f}",transform=axes.transAxes, fontsize=28, verticalalignment='top', zorder=10)

    ## Add bootstrap method (Helped along by AI)
    ## This section resamples the data 1000 times and calculates the median slope as well as the 95% confidence interval of slopes.
    if bootstrap==True and len(dataA[mask])>5:
        slopes = []
        intercepts = []
        mbes = []

        for _ in range(1000):
            ## resampler
            idx = np.random.choice(len(dataA[mask]), len(dataA[mask]), replace=True)
            ## apply resampler to data
            a_boot = dataA[mask][idx]
            b_boot = dataB[mask][idx]

            ## make sure data is realistic
            if np.std(a_boot) > 0:
                ## get best fit line for the resampled data
                zb = np.polyfit(a_boot, b_boot, 1)
                ## add slope, intercept, and mbe to lists
                slopes.append(zb[0])
                intercepts.append(zb[1])
                mbes.append(np.mean(b_boot - a_boot))

        if len(slopes) > 10:
            ## convert list to array
            slopes = np.array(slopes)
            intercepts = np.array(intercepts)

            ## calculate the 95% confidence interval of the slopes
            slope_ci = np.percentile(slopes, [2.5, 97.5])
            slope_med = np.median(slopes)
            intercept_med = np.median(intercepts)

            ## Calculate the 95% confidence interval of mbe 
            mbe_ci = np.percentile(mbes, [2.5, 97.5])
            mbe_med = np.median(mbes)
            if boot_shade==True:
                ## Bootstrap fit line
                y_boot = slope_med * x_fit + intercept_med
                axes.plot(x_fit, y_boot, "r", lw=5)

                ## shade in bootstrap confidence interval
                y_low = slope_ci[0] * x_fit + intercept_med
                y_high = slope_ci[1] * x_fit + intercept_med
                axes.fill_between(x_fit, y_low, y_high, alpha=0.2)
                
            ## if we want to display stats then print the actual slope with the bootstrap 95% confidence interval
            if stats==True:
                axes.text(0.02, 0.9,f"Slope: {z[0]:.2f} [{slope_ci[0]:.2f},{slope_ci[1]:.2f}]",transform=axes.transAxes,fontsize=28, verticalalignment='top')
    
    ## Calculate and add RMSE when plot is depicting the same variable in different data
    rmse = np.sqrt(np.mean((dataA[mask] - np.array(dataB)[mask]) ** 2))
    if same_var==True & stats==True:
        axes.text(0.02, 0.83, f"RMSE: {rmse:.2f}",transform=axes.transAxes, fontsize=28, verticalalignment='top', zorder=10)

        
    ## calculate mean bias
    bias = np.mean(dataB[mask] - dataA[mask])

    ## if we dont bootstrap just print the MBE
    if stats==True and bootstrap == False:
        axes.text(0.02, 0.97, f"MBE: {bias:.2f}",transform=axes.transAxes, fontsize=28, verticalalignment='top', zorder=10)
        
    ## if bootstrapped then print MBE of data with 95% BS CI
    if stats==True and bootstrap==True:
        ## print bootstrap mean bias error
        axes.text(0.02, 0.97,f"MBE: {bias:.2f} [{mbe_ci[0]:.2f},{mbe_ci[1]:.2f}]",transform=axes.transAxes,fontsize=28,verticalalignment='top')

    ## calculate coefficient of determination (R^2)
    r_value = scipy.stats.linregress(dataA[mask], dataB[mask])[2]
    print(r_value)
    r_2 = r_value**2
    if stats==True:
        axes.text(0.02, 0.76, f"R$^2$: {r_2:.2f}",transform=axes.transAxes, fontsize=28, verticalalignment='top', zorder=10)
    
    ## Find cc for contoured field
    if cont_field is not None:
        mask_cfield = np.isfinite(dataA) & np.isfinite(cont_field)
        cc_dataA_cfield = np.corrcoef(dataA[mask], cont_field[mask_cfield])[0, 1]
        cb = axes.figure.colorbar(scat, ax=axes, orientation="vertical", fraction=0.05, pad=0.05) 
        cb.ax.tick_params(labelsize=28)
        cb.set_label(lab_cont, fontsize=28)

        if same_var==True:
            axes.text(np.nanmin(find_levels(dataA,dataB,n))+ np.nanmax(find_levels(dataA,dataB,n))/n,np.nanmin(find_levels(dataA,dataB,n))
            ,f"cc({labA},shaded  field): {cc_dataA_cfield:.2f}",fontsize=28, c='r')
            

    axes.set_title(title,fontsize=45)

    plt.savefig(save_as)
    return axes