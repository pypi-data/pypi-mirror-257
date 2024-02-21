import matplotlib.pyplot as plt
import numpy as np 
from avrami.functions import fitted_DH
from avrami.log_functions import logDH_fit


def scatter_plot(df):
    df.plot(x='time', y='Area', marker='o', linestyle='-')
    plt.xlabel('Time (min)')
    plt.ylabel('DH (J/g)')
    plt.title('Enthalpy vs Time')
    plt.show()



def scatter_plot_fit(df, DHinf_fit, k_fit, tzero_fit, n_fit):
    t_data = np.array(df['time'])
    a_data = np.array(df['Area'])
    plt.scatter(t_data, a_data, label='Data')
    plt.plot(t_data, fitted_DH(t_data, DHinf_fit, k_fit, tzero_fit, n_fit), label='Fitted DH Function', color='red')
    plt.xlabel('Time (min)')
    plt.ylabel('DH (J/g)')
    plt.title('Enthalpy vs Time Fit')
    plt.legend()
    plt.show()


