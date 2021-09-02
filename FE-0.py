# Import  the Libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from finta import TA
from datetime import timedelta
import datetime as dt
#import talib
# https://blog.quantinsti.com/install-ta-lib-python/


#Data Extraction
x_in='Close'
quot = pd.read_csv('GHNI.csv')
timestamp=quot.iloc[:,0]
open=quot.iloc[:,1]
high=quot.iloc[:,2]
low=quot.iloc[:,3]
close=quot.iloc[:,4]
volume=quot.iloc[:,5]




###############################################Time Engineering
timestamp=pd.to_datetime(timestamp)
time_year=pd.DataFrame({'Year': timestamp.dt.year})
time_quarter=pd.DataFrame({'Quarter': timestamp.dt.quarter})
time_month=pd.DataFrame({'Month': timestamp.dt.month})
time_week=pd.DataFrame({'Week': timestamp.dt.isocalendar().week})
time_date=pd.DataFrame({'Date': timestamp.dt.day})
time_day=pd.DataFrame({'Day': timestamp.dt.weekday})

###############################################Signal Processing
close_return=pd.DataFrame({'C-ROC': close.pct_change()})
volume_return=pd.DataFrame({'V-ROC': volume.pct_change()})

#print('COMON', time_week)





##############################################Technical Indicators
#Simple Moving Averages
hl_span=volume
MA_2=TA.SMA(quot, 2)
MA_3=TA.SMA(quot, 3)
MA_5=TA.SMA(quot, 5)
MA_8=TA.SMA(quot, 8)
MA_13=TA.SMA(quot, 13)
MA_21=TA.SMA(quot, 21)
MA_34=TA.SMA(quot, 34)
MA_55=TA.SMA(quot, 55)
MA_89=TA.SMA(quot, 89)
MA_144=TA.SMA(quot, 144)
MA_233=TA.SMA(quot, 233)
MA_377=TA.SMA(quot, 377)
MA_610=TA.SMA(quot, 610)
SMA_FIB=pd.concat([MA_2, MA_3, MA_5, MA_8, MA_13, MA_21, MA_34, MA_55, MA_89, MA_144, MA_233, MA_377, MA_610 ], axis=1)

# Bollinger Band
BB=TA.BBANDS(quot,20,2)

#BB_U=BB['BB_UPPER']
#Strength
TRUE_SEN=TA.TSI(quot,25,13,13)

#Oscillators
MACD=TA.MACD(quot,12,26,9)
STOCH_RSI=TA.STOCHRSI(quot,14,14)
RSI=TA.RSI(quot,14)
MFI=TA.MFI(quot,14)
ULT_OSC=TA.UO(quot)
VORTEX_IND=TA.VORTEX(quot,14)
AWE_OSC=TA.AO(quot)
Fish_14=TA.FISH(quot, 50)
Fish_9=TA.FISH(quot,500)
RMI=RSI-MFI
print(RMI)
#Time Chart
fig, axs = plt.subplots(6)
fig.suptitle('Feature Engineering')
axs[0].plot(close)
axs[0].plot(BB)
axs[1].plot(close_return)
axs[2].plot(volume_return)
axs[3].plot(SMA_FIB)
axs[4].plot(RSI)
axs[4].plot(MFI)
axs[5].plot(RMI)

plt.show()


                    # Prepare FE File
#feng=pd.concat([close,volume, hl_span, TA.FISH(quot, 14),TA.EMA(quot, 2)],axis=1)
feng=pd.concat([time_year,time_quarter,time_month,time_week,time_date, time_day, close,close_return,volume_return,BB,RSI,MFI,RMI,MACD,AWE_OSC,STOCH_RSI,VORTEX_IND,ULT_OSC,TRUE_SEN,SMA_FIB],axis=1)
feng=feng.fillna(0)
#print(feng)

                    # Correlation Engine
# Plotting Correlation Heat Map
#ax = sns.heatmap(feng.corr().sort_values('Close'), vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(50, 220, n=200), square=False)
#ax.set_xticklabels(ax.get_xticklabels(), rotation=45,horizontalalignment='right');
#plt.show()
# Plotting Correlation BAR MAP
feng_corr=feng.corr()
feng_corr['Close'].plot(kind='bar')
plt.show()





















##Save Engine
featured_file = pd.ExcelWriter('FEATURED.xlsx', engine='openpyxl')
feng.to_excel(featured_file, '1', index=False, startcol=0)
#ybox.to_excel(testfile, 'Y-TRAIN', index=False, startcol=0)
featured_file.save()
featured_file.close()
print('Saving Done')




#Junkyard
#plt.figure(figsize=(16,8))
#plt.title(x_in)
#plt.plot(hl_span)
#plt.figure(figsize=(16,8))
#plt.plot(close)
#plt.xlabel('Date', fontsize=18)
#plt.ylabel('Price', fontsize=18)
