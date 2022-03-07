import pvlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import daytime  
import seaborn as sns
from scipy import stats
from sklearn.metrics import mean_squared_error




'''
Common plots set-up function.
'''
def plot_specs(title, ylabel, xlabel, rot, ylim_min, 
    ylim_max, xlim_min, xlim_max, loc):
    plt.rc('font', family='Helvetica')
    plt.rcParams['axes.axisbelow'] = True;
    
    plt.title(title, fontname="Helvetica", fontsize=15);
    plt.ylabel(ylabel, fontname="Helvetica", fontsize=13);
    plt.xlabel(xlabel, fontname="Helvetica", fontsize=13);
    
    plt.tick_params(direction='out', length=5, width=0.75, grid_alpha=0.3)
    plt.xticks(rotation=rot)
    plt.ylim(ylim_min, ylim_max)
    plt.xlim(xlim_min, xlim_max)
    plt.grid(True);
    plt.legend(loc=loc, fontsize=9);
    plt.tight_layout;

'''
Statistic Metrics
'''
def median_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.median(np.abs((y_true - y_pred) / y_true)) * 100

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def metrics(r2, measured, modeled, store):
    print('R2: ', r2.round(4))

    metrics_df = pd.DataFrame({'measured': measured, 
                               'modeled': modeled})

    y_true = metrics_df.measured
    y_pred = metrics_df.modeled

    rmse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)
    rmse = (rmse/np.max(y_true))*100
    print('RMSE: ', np.round(rmse, 2))

    '''
    MAPE requires to filter the data when y_true=0 --> (y_true - y_pred)/y_true
    '''
    metrics_df = metrics_df.loc[(metrics_df.index.hour >= 7) & (metrics_df.index.hour <= 17) & (metrics_df.measured != 0)]

    y_true = metrics_df.measured
    y_pred = metrics_df.modeled

    mape = median_absolute_percentage_error(y_true=y_true, y_pred=y_pred)
    print('MAPE: ', np.round(mape, 2))
    
    if store == True:
        list_r2.append(r_value)
        list_rmse.append(rmse)
        list_mape.append(mape)