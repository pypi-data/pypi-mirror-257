# main.py
import os
import pandas as pd
import progressbar
from time import sleep
import datetime as dt
from datetime import date
from datetime import timedelta
import yfinance as yf
import pytz
import numpy as np
from stockstats import StockDataFrame as Sdf
NY = "America/New_York"

class Load_n_Preprocess:
    def __init__(self, tickers_list, start_date, end_date, feature_lookback = 0, drl_lookback = 0, path_daily_data = None, path_intraday_data=None):
        self.tickers_list = tickers_list
        self.removed_tickers_list = []
        self.start_date = pd.to_datetime(start_date)
        self.feature_lookback = feature_lookback
        self.drl_lookback = drl_lookback
        self.end_date = pd.to_datetime(end_date)
        self.path_daily_data = path_daily_data
        self.path_intraday_data = path_intraday_data

        self.market_open = pd.Timestamp('09:30:00').time()              # Regular market open time
        self.market_close = pd.Timestamp('15:30:00').time()             # Regular market close time

    def load_daily_data(self):
        file_ext = os.path.splitext(self.path_daily_data)[-1]
        if file_ext == '.csv':
            df_tics_daily = pd.read_csv(self.path_daily_data)
        elif file_ext == '.h5':
            df_tics_daily = pd.read_hdf(self.path_daily_data, "df",mode = 'r')

        ######## this part is written for temproary  ###########################
        # df_tics['tic'] = TICKERS_LIST[0]
        # df_tics = df_tics[['Date','tic','Open','High','Low','Close']]
        # df_tics = df_tics.rename(columns = {'Date':'date','Open':'open','High':'high','Low':'low','Close':'close'})
        # df_tics['tic'] = TICKERS_LIST[0]
        # df_tics = df_tics[['time','tic','open','high','low','close']]
        # df_tics = df_tics.rename(columns = {'time':'date'})
        ########################################################################
        if len(self.tickers_list) == 0:
            self.tickers_list = list(df_tics_daily['tic'].unique())
        else:
            df_tics_daily = df_tics_daily.loc[df_tics_daily['tic'].isin(self.tickers_list)]
        
        df_tics_daily['date'] = pd.to_datetime(df_tics_daily['date']).dt.date               #,utc=True)              # convert date column to datetime
        df_tics_daily['date'] = pd.to_datetime(df_tics_daily['date'])
        df_tics_daily = df_tics_daily.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics_daily.index = df_tics_daily['date'].factorize()[0]

        start_date_idx = df_tics_daily[(df_tics_daily['date'] >= self.start_date)].index[0] - (self.drl_lookback + self.feature_lookback)
        end_date_idx = df_tics_daily[(df_tics_daily['date'] <= self.end_date)].index[-1] 
        df_tics_daily = df_tics_daily.loc[start_date_idx:end_date_idx]
        df_tics_daily = df_tics_daily.reset_index(drop=True)
        df_tics_daily.index = df_tics_daily['date'].factorize()[0]

        return df_tics_daily


    def mean_cov_return(self, df_tics_daily):
        df_tics_close = df_tics_daily.pivot(index = 'date',values = 'close',columns='tic')
        df_tics_close = df_tics_close.ffill().bfill()
        df_mean_returns = pd.DataFrame(df_tics_close.pct_change().mean(),columns=['mean_return']).reset_index()
        cov_matrix = np.asarray(df_tics_close.pct_change().cov())
        corr_matrix = np.asarray(df_tics_close.pct_change().corr())

        return df_mean_returns, cov_matrix, corr_matrix

    def load_intraday_data(self):
        file_ext = os.path.splitext(self.path_intraday_data)[-1]
        if file_ext == '.csv':
            df_tics_intraday = pd.read_csv(self.path_intraday_data)
        elif file_ext == '.h5':
            df_tics_intraday = pd.read_hdf(self.path_intraday_data, "df",mode = 'r') 

        df_tics_intraday = df_tics_intraday[df_tics_intraday['tic'].isin(self.tickers_list)]

        df_tics_intraday = df_tics_intraday[['datetime','tic','open','high','low','close','volume']]
        df_tics_intraday = df_tics_intraday.rename(columns = {'datetime':'date'})
        
        df_tics_intraday[['open','high','low','close']] = df_tics_intraday[['open','high','low','close']].astype(float)
        df_tics_intraday = df_tics_intraday.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics_intraday.index = df_tics_intraday['date'].factorize()[0]

        return df_tics_intraday
    
    def clean_intraday_data(self, df_tics_daily, df_tics_intraday):
        intraday_start_date = self.start_date - timedelta(days = 10)
        intraday_end_date = self.end_date + timedelta(days = 1)

        if self.path_intraday_data.split('_')[-1].split('.')[0] == '30min':
            freq = '30T'

        elif self.path_intraday_data.split('_')[-1].split('.')[0] == '1hour':
            freq = '1h'

        df_timestamps = pd.date_range(start=intraday_start_date, end=intraday_end_date, freq = freq)
        df_timestamps = pd.DataFrame(df_timestamps[(df_timestamps.time >= self.market_open) & (df_timestamps.time <= self.market_close)],columns=['datetime'])
        df_timestamps['date'] = df_timestamps['datetime'].dt.date

        df_timestamps = df_timestamps[pd.to_datetime(df_timestamps['date']).isin(df_tics_daily['date'].unique())]
        df_timestamps = df_timestamps.drop('date',axis=1)
        df_timestamps = df_timestamps.rename(columns = {'datetime':'date'})


        df_tics_intraday_list = []
        for tic in self.tickers_list:
            df_tic_intraday = df_tics_intraday[df_tics_intraday['tic'] == tic]
            df_tic_intraday = df_tic_intraday[(df_tic_intraday['date'].dt.time >= self.market_open) & (df_tic_intraday['date'].dt.time <= self.market_close)]
            
            df_tic_intraday = df_timestamps.merge(df_tic_intraday,on='date', how='left')
            df_tic_intraday = df_tic_intraday.sort_values(by=['date'],ignore_index=True)
            print("No. of missing values before imputation for %5s = %5d"%(tic,df_tic_intraday['close'].isna().sum()))
            # df_tic_intraday = df_tic_intraday.fillna(method='ffill').fillna(method='bfill')
            df_tic_intraday = df_tic_intraday.ffill().bfill()
            # df_tic_intraday['intraday_return'] = df_tic_intraday['open'].pct_change().fillna(0)    # this line add pct_change feature
            df_tics_intraday_list.append(df_tic_intraday)

        df_tics_intraday = pd.concat(df_tics_intraday_list)
        df_tics_intraday = df_tics_intraday.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics_intraday.index = df_tics_intraday['date'].factorize()[0]

        return df_tics_intraday
    
    def clean_daily_data_old(self, df_tics_daily):
        # df_tics = df_tics[(df_tics['date'] >= self.start_date) & (df_tics['date'] <= self.end_date)]  # formation date not included
        uniqueDates = df_tics_daily['date'].unique()
        # print(f"Number of Unique dates in between {df_tics['date'].iloc[0].date()} and {df_tics['date'].iloc[-1].date()} is {len(uniqueDates)}")
        df_dates = pd.DataFrame(uniqueDates, columns=['date'])

        df_tics_daily_list = []
        for tic in self.tickers_list:
            df_tic = df_tics_daily[df_tics_daily['tic'] == tic]
            df_tic = df_dates.merge(df_tic, on='date', how='left')
            df_tic['tic'] = tic
            print("No. of missing values before imputation for %5s = %5d"%(tic,df_tic['close'].isna().sum()))
            df_tic = df_tic.fillna(method='ffill').fillna(method='bfill')
            df_tics_daily_list.append(df_tic)

        df_tics_daily = pd.concat(df_tics_daily_list)
        df_tics_daily = df_tics_daily.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics_daily.index = df_tics_daily['date'].factorize()[0]

        # index_start_date = df_tics[(df_tics['date'] >= self.start_date)].index[0] - (self.drl_lookback + self.feature_lookback - 2)
        # index_end_date = df_tics[(df_tics['date'] <= self.end_date)].index[-1] 
        # df_tics = df_tics.loc[index_start_date:index_end_date]

        start_date_idx = df_tics_daily[(df_tics_daily['date'] >= self.start_date)].index[0] - (self.drl_lookback + self.feature_lookback)
        end_date_idx = df_tics_daily[(df_tics_daily['date'] <= self.end_date)].index[-1] 
        df_tics_daily = df_tics_daily.loc[start_date_idx:end_date_idx]
        df_tics_daily = df_tics_daily.reset_index(drop=True)
        df_tics_daily.index = df_tics_daily['date'].factorize()[0]

        # print(f'Start date index: {start_date_idx}\nEnd date index: {end_date_idx}')
        print("Data cleaned.")
        return df_tics_daily

    def filter_tickers_old(self, df, missing_values_allowed = 0.01):
        uniqueDates = df['date'].unique()
        # if len(self.tickers_list) == 0:
        #     self.tickers_list = df['tic'].unique()
        # print("===================================================")
        # print(f'Number of Unique dates in between {self.start_date.date()} and {self.end_date.date()} is {len(uniqueDates)}')
        # print("===================================================")
        df_dates = pd.DataFrame(uniqueDates, columns=['date'])

        df_tics_list = []
        updated_tickers_list = []
        for i, tic in enumerate(self.tickers_list):
            df_tic = df[df['tic'] == tic]
            df_tic = df_dates.merge(df_tic, on='date', how='left')
            df_tic['tic'] = tic
            # print('No. of missing values for', tic, ' =',df_tic['close'].isna().sum())
            # print("No. of missing values for %5s = %5d"%(tic,df_tic['close'].isna().sum()))
            
            
            if df_tic['close'].isna().sum() <= missing_values_allowed * len(df_dates): 
                df_tic = df_tic.fillna(method='ffill').fillna(method='bfill')   # can be commented.
                df_tics_list.append(df_tic)
                updated_tickers_list.append(tic)
            else:
                # print(tic,' is removed based on missing values')
                self.removed_tickers_list.append(tic)

        self.tickers_list = updated_tickers_list
        df_tics = pd.concat(df_tics_list)
        df_tics = df_tics.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics.index = df_tics.date.factorize()[0]
        print(f"{self.removed_tickers_list} are removed due to missing data.")
        return df_tics

    def clean_daily_data(self, df, missing_values_allowed = 0.01):
        uniqueDates = df['date'].unique()
        # if len(self.tickers_list) == 0:
        #     self.tickers_list = df['tic'].unique()
        # print("===================================================")
        # print(f'Number of Unique dates in between {self.start_date.date()} and {self.end_date.date()} is {len(uniqueDates)}')
        # print("===================================================")
        df_dates = pd.DataFrame(uniqueDates, columns=['date'])

        df_tics_daily_list = []
        updated_tickers_list = []
        for i, tic in enumerate(self.tickers_list):
            df_tic = df[df['tic'] == tic]
            df_tic = df_dates.merge(df_tic, on='date', how='left')
            df_tic['tic'] = tic
            # print('No. of missing values for', tic, ' =',df_tic['close'].isna().sum())
            # print("No. of missing values for %5s = %5d"%(tic,df_tic['close'].isna().sum()))
            # print("No. of missing values before imputation for %5s = %5d"%(tic,df_tic['close'].isna().sum()))
            if df_tic['close'].isna().sum() <= missing_values_allowed * len(df_dates): 
                # df_tic = df_tic.fillna(method='ffill').fillna(method='bfill')   # can be commented.
                df_tic = df_tic.ffill().bfill()   
                df_tics_daily_list.append(df_tic)
                updated_tickers_list.append(tic)
            else:
                # print(tic,' is removed based on missing values')
                self.removed_tickers_list.append(tic)

        self.tickers_list = updated_tickers_list
        df_tics_daily = pd.concat(df_tics_daily_list)
        df_tics_daily = df_tics_daily.sort_values(by=['date', 'tic'],ignore_index=True)
        df_tics_daily.index = df_tics_daily.date.factorize()[0]
        print(f"{self.removed_tickers_list} are removed due to missing data.")\
        
        start_date_idx = df_tics_daily[(df_tics_daily['date'] >= self.start_date)].index[0]
        end_date_idx = df_tics_daily[(df_tics_daily['date'] <= self.end_date)].index[-1] 
        df_tics_daily = df_tics_daily.reset_index(drop=True)
        df_tics_daily.index = df_tics_daily['date'].factorize()[0]

        return df_tics_daily

    def convert_daily(self,df_daily,timeframe ='W'):
        df_daily = df_daily.set_index('date')
        df_daily['date'] = df_daily.index
        dfw_tics_list = []
        for tic in self.tickers_list:
            df_tic = df_daily[df_daily['tic'] == tic]
            df_tic.sort_index(ascending=True)
            logic = {'date':'first',
                        'open'  : 'first',
                        'high'  : 'max',
                        'low'   : 'min',
                        'close' : 'last',
                        'volume': 'sum'}

            # df = pd.read_clipboard(parse_dates=['Date'], index_col=['Date'])
            dfw_tic = df_tic.resample(timeframe).apply(logic)
            if timeframe == 'W':
                dfw_tic.index = dfw_tic.index - pd.tseries.frequencies.to_offset("6D")
                dfw_tic['tic'] = tic
                dfw_tics_list.append(dfw_tic)
            else:
                dfw_tic.index = dfw_tic.index - pd.tseries.frequencies.to_offset("1M") + pd.tseries.frequencies.to_offset("1D")
                dfw_tic['tic'] = tic
                dfw_tics_list.append(dfw_tic)

        dfw_tics = pd.concat(dfw_tics_list)
        dfw_tics = dfw_tics.set_index('date')
        dfw_tics = dfw_tics.reset_index()
        dfw_tics = dfw_tics[['date','tic','open','high','low','close','volume']]
        dfw_tics.index = dfw_tics.date.factorize()[0]
        return dfw_tics


def download_ohlcv_tickers(start_date, end_date, tickers_list, download_as='h5', period = '1d'):
    df_tics = pd.DataFrame()
    for tic in tickers_list:
        if "." in tic:
            tic = tic.replace(".", "-")
            print(tic)

        if " " in tic:
            tic = tic.replace(" ", "-")
            print(tic)

        try:
            df_tic = yf.download(tickers=tic,
                                start=start_date,
                                # end=end_date,
                                progress=True,
                                #threads=True,
                                interval = period,               # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                group_by='ticker'        # select this only when you need OHLCV data ticker wise
            )
        except:
            print(f"{tic} not found")
            pass

        df_tic['tic']= tic
        df_tic = df_tic.reset_index()
        df_tic = df_tic.rename(columns={'Date':'date','Adj Close':'adj_close','Close':'close','Open':'open','High':'high','Low':'low','Volume':'volume'})

        df_tics = pd.concat([df_tics,df_tic[['date', 'tic', 'open','high','low','close','adj_close','volume']]])                 # uncomment if OHLCV data needed

    filename = 'df_tics_ohlcv.'+ download_as

    if download_as == 'h5':
        df_tics.to_hdf(filename,"df",mode = 'w')

    elif download_as == 'parquet':
        df_tics.to_parquet(filename)

    elif download_as == 'csv':
        df_tics.to_csv(filename, index = False)

    elif download_as == 'excel':
        df_tics.to_excel(filename, index = False)

    print("Data downloaded from yahoo finance")

