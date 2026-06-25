## script to plot multiple variables on a single time series

import matplotlib.pyplot as plt
import numpy as np
import math

## For aligning y-axis at 0
def align_zero(ax1, ax2):
    y1_min, y1_max = ax1.get_ylim()
    y2_min, y2_max = ax2.get_ylim()

    ## Relative location of zero on first axis
    zero_rel = (0 - y1_min) / (y1_max - y1_min)

    # get range and keep it for axis 2
    range2 = y2_max - y2_min

    new_y2_min = -zero_rel * range2
    new_y2_max = new_y2_min + range2

    ax2.set_ylim(new_y2_min, new_y2_max)

## ax = Ax object to plot on (ax)
## time = Time used for time series (must be compatable with variables) (xarray)
## var_1,var_2,var_3 and var_4 = Variables to plot (xarray)
## v_name_1,v_name_2,v_name_3 and v_name_4 = The varibale names (string)
## step = The step interval of first y-axis (float)
## step2 = The step interval of the second y-axis (only if twinx==True) (float)
## x_label = x axis label (string)
## y_label = y axis label (string)
## y_label_ax2 = y axis label for second y axis (only if twinx==True) (string)
## title = Title to display on top of graph (string)
## linestyles = Line style of 4 lines, list of style symbols (string list)
## c_list = Color of 4 lines, list of colors (string list)
## twinx = If true create a second y-axis (boolean)
## align = If true align two y axes at zero (boolean)
## same_cc = If true calculate cc between vars 1 and 2 and 3 and 4 (boolean)


def ts_multivar(ax, time, var_1, var_2, var_3, var_4, v_name_1, v_name_2, v_name_3, v_name_4, step, step2, x_label, y_label,y_label_ax2, title, linestyles, c_list, twinx, align,same_cc):
                
    fig = ax.figure
                
    ax.set_xlabel(x_label,fontsize=36)
    ax.set_ylabel(y_label,fontsize=36)
    ax.plot(time,var_1, label=v_name_1, c=c_list[0],lw=3, linestyle=linestyles[0])
    ax.plot(time,var_2, label=v_name_2, c=c_list[1],lw=3, linestyle=linestyles[1])
    
    max_l=[np.nanmax(var_1),np.nanmax(var_2)]
    min_l=[np.nanmin(var_1),np.nanmin(var_2)]
    
    if var_3 is not None and twinx==False:
        ax.plot(time,var_3, label=v_name_3, c=c_list[2],zorder=2,lw=3, linestyle=linestyles[2])
        max_l.append(np.nanmax(var_3))
        min_l.append(np.nanmin(var_3))
        if var_4 is not None:
            ax.plot(time,var_4, label=v_name_4, c=c_list[3],zorder=2,lw=3, linestyle=linestyles[3])
        
    if var_3 is not None and twinx==True:
        ax2 = ax.twinx()
        ax2.plot(time,var_3, label=v_name_3, c=c_list[2],zorder=2,lw=3, linestyle=linestyles[2])
        #ax2.set_yticks(np.arange(math.floor(np.nanmin(var_3) / 10) * 10,(math.ceil(np.nanmax(var_3) / 10) * 10)+step2*4,step2))
        ax2.set_yticks(np.arange(math.floor(np.nanmin(var_3) / step2) * step2,(math.ceil(np.nanmax(var_3) / step2) * step2)+step2*4,step2))
        if var_4 is not None:
            ax2.plot(time,var_4, label=v_name_4, c=c_list[3],zorder=2,lw=3,linestyle=linestyles[3])
            #ax2.set_yticks(np.arange(math.floor(np.nanmin(var_3) / 10) * 10,(math.ceil(np.nanmax(var_3) / 10) * 10)+step2*4,step2))
            ax2.set_yticks(np.arange(math.floor(np.nanmin(var_3) / step2) * step2,(math.ceil(np.nanmax(var_3) / step2) * step2)+step2*4,step2))
            
    if var_3 is None and twinx==True:
        ax2 = ax.twinx()
        ax2.plot(time,var_2, label=v_name_2, c=c_list[2],zorder=2,lw=3, linestyle=linestyles[1]) 
        ax2.set_yticks(np.arange(math.floor(np.nanmin(var_2) / 10) * 10,(math.ceil(np.nanmax(var_2) / 10) * 10)+step2*4,step2))

        
    ## The following code determines the y range and ticks of the plot
    ax.set_yticks(np.arange(math.floor(min(min_l) / 10) * 10,(math.ceil(max(max_l) / 10) * 10)+step*3,step))
    
    ax.tick_params(axis='both', labelsize=28)
    ax.tick_params(axis='both', which='major', length=5, width=2)

    if twinx==True:
        ax2.tick_params(axis='both', labelsize=28)
        ax2.tick_params(axis='both', which='major', length=5, width=2)
        ax2.set_ylabel(y_label_ax2,fontsize=36)

        if align==True:
            align_zero(ax, ax2)
        
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        legend = ax.legend(lines + lines2, labels + labels2, loc='upper right',fontsize=28)
        ## make sure legend is on top
        legend.set_zorder(10)
    if twinx == False:
        legend = ax.legend(loc='upper right',fontsize=28)
        legend.set_zorder(10)
    if var_3 is not None and same_cc==False:
            ## make sure vars are numpy 
            var_1_np = np.array(var_1)
            var_3_np = np.array(var_3)
            ## make mask for nans
            mask_2 = ~np.isnan(var_1_np) & ~np.isnan(var_3_np)
            ## calulate cc
            cc_2= np.corrcoef(var_1_np[mask_2], var_3_np[mask_2])[0, 1]
            ax.text( 0.02, 0.95, f"r({v_name_1}, {v_name_3}) = {cc_2:.2f}",transform=ax.transAxes,
            fontsize=28, verticalalignment='top', zorder=10)
    if var_3 is not None and same_cc==True:
            ## make sure vars are numpy 
            var_3_np = np.array(var_3)
            var_4_np = np.array(var_4)
            ## make mask for nans
            mask_2 = ~np.isnan(var_3_np) & ~np.isnan(var_4_np)
            ## calulate cc
            cc_2= np.corrcoef(var_3_np[mask_2], var_4_np[mask_2])[0, 1]
            ax.text( 0.02, 0.95, f"r({v_name_3}, {v_name_4}) = {cc_2:.2f}",transform=ax.transAxes,
            fontsize=28, verticalalignment='top', zorder=10)
    ## make sure vars are numpy 
    var_1_np = np.array(var_1)
    var_2_np = np.array(var_2)
    ## make mask for nans
    mask = ~np.isnan(var_1_np) & ~np.isnan(var_2_np)
    ## calulate cc
    cc= np.corrcoef(var_1_np[mask], var_2_np[mask])[0, 1]
    ax.text(0.02, 0.88, f"r({v_name_1}, {v_name_2}) = {cc:.2f}",transform=ax.transAxes,
    fontsize=28,verticalalignment='top',zorder=10)

    
    ax.set_title(title, fontsize=36)
    if twinx == False:
        return ax
    elif twinx ==True:
        return ax,ax2
