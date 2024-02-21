import numpy as np


def logDH(df, tzero_fit, DHinf_fit):
    t_data = np.array(df['time'])
    a_data = np.array(df['Area'])
    x = np.abs(t_data - tzero_fit)

    new_a_data = a_data[a_data < DHinf_fit]

    
    # Filter the corresponding elements in x
    filter_x = x[a_data < DHinf_fit]

    y = np.log(1 - new_a_data / DHinf_fit)

    return filter_x, y 



def logDH_fit(x, y):
    k_lin, n_lin = np.polyfit(x,y,1)
    return k_lin, n_lin
