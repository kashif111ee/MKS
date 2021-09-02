import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from finta import TA
from datetime import timedelta
import datetime as dt
import numpy as np


#Data Extraction
x_in='Close'
quot = pd.read_csv('GHNI.csv')
timestamp=quot.iloc[:,0]
open=quot.iloc[:,1]
high=quot.iloc[:,2]
low=quot.iloc[:,3]
close=quot.iloc[:,4]
volume=quot.iloc[:,5]
#Time Engineering
timestamp=pd.to_datetime(timestamp)
time_year=pd.DataFrame({'Year': timestamp.dt.year})
time_quarter=pd.DataFrame({'Quarter': timestamp.dt.quarter})
time_month=pd.DataFrame({'Month': timestamp.dt.month})
time_week=pd.DataFrame({'Week': timestamp.dt.isocalendar().week})
time_date=pd.DataFrame({'Date': timestamp.dt.day})
time_day=pd.DataFrame({'Day': timestamp.dt.weekday})
#Signal Processing
close_return=pd.DataFrame({'C-ROC': close.pct_change()})
volume_return=pd.DataFrame({'V-ROC': volume.pct_change()})

#Rolling Data
result = quot.asfreq('D').rolling(window=52*7, min_periods=1).max()



#Digital Checks
C_SIGNAL= pd.DataFrame()
V_SIGNAL= pd.DataFrame()
CEQUALO=pd.DataFrame()
HEQUALL=pd.DataFrame()
CEQUALL=pd.DataFrame()
CEQUALH=pd.DataFrame()
C_SIGNAL['C_SIGNAL'] = close_return['C-ROC'].apply(lambda x: 1 if x >= 0 else (0 if x <0 else '_'))
V_SIGNAL['V_SIGNAL'] = volume_return['V-ROC'].apply(lambda x: 1 if x >= 0 else (0 if x <0 else '_'))
CEQUALO['C=O']=np.where(close == open, 1, 0)
HEQUALL['H=L']=np.where(high == low, 1, 0)
CEQUALL['C=L']=np.where(close == low, 1, 0)
CEQUALH['C=H']=np.where(close == high, 1, 0)
#close['Close'].apply(lambda x: 1 if x >=  else (0 if x <0 else '_'))











feng=pd.concat([time_year,time_quarter,time_month,time_week,time_date, time_day, result,high,low,open,close,close_return,volume_return,C_SIGNAL,V_SIGNAL,CEQUALO,HEQUALL,CEQUALL,CEQUALH],axis=1)
feng=feng.fillna(0)
##Save Engine
featured_file = pd.ExcelWriter('FE1AOut.xlsx', engine='openpyxl')
feng.to_excel(featured_file, '1', index=False, startcol=0)
#ybox.to_excel(testfile, 'Y-TRAIN', index=False, startcol=0)
featured_file.save()
featured_file.close()
print('Saving Done')