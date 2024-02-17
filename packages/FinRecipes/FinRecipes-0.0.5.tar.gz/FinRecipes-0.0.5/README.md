# FinRecipes

```
from FinRecipes import Load_n_Preprocess

TICKERS_LIST_WORLD = ['AIT']
START_DATE = '2023-01-01'
END_DATE = '2024-12-01'
PATH_DAILY_DATA = "examples/df_ohlcv_daily.h5"
LP = Load_n_Preprocess(TICKERS_LIST_WORLD, START_DATE, END_DATE, path_daily_data = PATH_DAILY_DATA)
df_tics_daily = LP.load_daily_data()
print(df_tics_daily)

```