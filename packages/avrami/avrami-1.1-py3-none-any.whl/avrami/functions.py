import numpy as np
from scipy.optimize import curve_fit 


def DH(t_data, DHinf, k, tzero, n):
    return DHinf * (1 - np.exp(-k * np.abs(t_data - tzero)**n))


def DH_fitting(df, initial_guess):

    t_data = np.array(df['time'])
    a_data = np.array(df['Area'])
    
    params, covariance = curve_fit(DH, t_data, a_data, p0=initial_guess)

    DHinf_fit, k_fit, tzero_fit, n_fit = params

    return DHinf_fit, k_fit, tzero_fit, n_fit, covariance



def fitted_DH(t_data, DHinf_fit, k_fit, tzero_fit, n_fit):
    return DH(t_data, DHinf_fit, k_fit, tzero_fit, n_fit)

