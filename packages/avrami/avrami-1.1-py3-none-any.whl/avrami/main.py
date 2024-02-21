#!/usr/bin/env python
# coding: utf-8

#python main.py\Users\20224751\Downloads\SN_TEST.csv 6.0 0.05 1 1 -l --log
from avrami.file_load import data_import 
from avrami.functions import DH_fitting
from avrami.plots import scatter_plot, scatter_plot_fit
from avrami.log_functions import logDH, logDH_fit

import argparse

parser = argparse.ArgumentParser(
                    prog='Avrami Fit',
                    description='Fitting program for nucleation data',
                    epilog='Text at the bottom for help')

parser.add_argument('filename')  
parser.add_argument('file_path')
parser.add_argument('DHinf') 
parser.add_argument('k') 
parser.add_argument('tzero') 
parser.add_argument('n') 
parser.add_argument('-l', '--log',
                    action='store_true')  


def avrami_data_process(file_path, intial_guess):

    df = data_import(file_path)

    scatter_plot(df)

    DHinf_fit, k_fit, tzero_fit, n_fit, covariance = DH_fitting(df, intial_guess)
    print("Fitted DHinf:", DHinf_fit)
    print("Fitted k:", k_fit)
    print("Fitted tzero:", tzero_fit)
    print("Fitted n:", n_fit)
    print("Covariance matrix:\n", covariance)
    
    scatter_plot_fit(df, DHinf_fit, k_fit, tzero_fit, n_fit)

    x, y = logDH(df, tzero_fit, DHinf_fit)
    k_lin, n_lin = logDH_fit(x, y)
    print("k slope:", k_lin)
    print("reaction order:", n_lin)







if __name__ == '__main__':

    args = parser.parse_args()
    initial_guess = (args.DHinf, args.k, args.tzero, args.n) 
    avrami_data_process(args.file_path, initial_guess)
