from pandas_datareader import data as web
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import datetime as dt
from empyrical import*
import quantstats as qs
from tkinter import *
from pandastable import Table, TableModel


today = dt.date.today()

class Engine:


  def __init__(self,start_date, portfolio, weights=None, benchmark=['SPY'], end_date=today, optimizer=None, max_vol=0.15):
    self.start_date = start_date
    self.end_date = end_date
    self.portfolio = portfolio
    self.weights = weights
    self.benchmark = benchmark
    self.optimizer = optimizer
    self.max_vol = max_vol

    if self.weights==None:
      self.weights = [1.0/len(self.portfolio)]*len(self.portfolio)



def get_returns(stocks,wts, start_date, end_date=today):
  if len(stocks) > 1:
    assets = web.DataReader(stocks, data_source='yahoo', start = start_date, end= end_date)['Adj Close']
    ret_data = assets.pct_change()[1:]
    returns = (ret_data * wts).sum(axis = 1)
    return returns
  else:
    df = web.DataReader(stocks, data_source='yahoo', start = start_date, end= end_date)['Adj Close']
    df = pd.DataFrame(df)
    returns = df.pct_change()
    return returns

def information_ratio(returns, benchmark_returns, days=252):
 return_difference = returns - benchmark_returns
 volatility = return_difference.std() * np.sqrt(days)
 information_ratio = return_difference.mean() / volatility
 return information_ratio




def empyrial(my_portfolio, rf=0.0, sigma_value=1, confidence_value=0.95):

  returns = get_returns(my_portfolio.portfolio, my_portfolio.weights, start_date=my_portfolio.start_date,end_date=my_portfolio.end_date)
  benchmark = get_returns(my_portfolio.benchmark, wts=[1], start_date=my_portfolio.start_date,end_date=my_portfolio.end_date)

  CAGR = cagr(returns, period=DAILY, annualization=None)
  CAGR = round(CAGR,2)
  CAGR = CAGR.tolist()
  CAGR = str(round(CAGR*100,2)) + '%'

  CUM = cum_returns(returns, starting_value=0, out=None)*100
  CUM = CUM.iloc[-1]
  CUM = CUM.tolist()
  CUM = str(round(CUM,2)) + '%'


  VOL = qs.stats.volatility(returns, annualize=True, trading_year_days=252)
  VOL = VOL.tolist()
  VOL = str(round(VOL*100,2))+' %'

  SR = sharpe_ratio(returns, risk_free=rf, period=DAILY)
  SR = np.round(SR, decimals=2)
  SR = str(SR)

  CR =  qs.stats.calmar(returns)
  CR = CR.tolist()
  CR = str(round(CR,2))

  STABILITY = stability_of_timeseries(returns)
  STABILITY = round(STABILITY,2)
  STABILITY = str(STABILITY)


  MD = max_drawdown(returns, out=None)
  MD = str(round(MD*100,2))+' %'

  
  '''OR = omega_ratio(returns, risk_free=0.0, required_return=0.0)
  OR = round(OR,2)
  OR = str(OR)
  print(OR)'''

  SOR = sortino_ratio(returns, required_return=0, period=DAILY)
  SOR = round(SOR,2)
  SOR = str(SOR)


  SK = qs.stats.skew(returns)
  SK = round(SK,2)
  SK = SK.tolist()
  SK = str(SK)


  KU = qs.stats.kurtosis(returns)
  KU = round(KU,2)
  KU = KU.tolist()
  KU = str(KU)

  TA = tail_ratio(returns)
  TA = round(TA,2)
  TA = str(TA)


  CSR = qs.stats.common_sense_ratio(returns)
  CSR = round(CSR,2)
  CSR = CSR.tolist()
  CSR = str(CSR)


  VAR = qs.stats.value_at_risk(returns, sigma=sigma_value, confidence=confidence_value)
  VAR = np.round(VAR, decimals=2)
  VAR = str(VAR*100)+' %'

  AL = alpha_beta(returns, benchmark, risk_free=rf)
  AL = AL[0]
  AL = round(AL,2)

  BTA = alpha_beta(returns, benchmark, risk_free=rf)
  BTA = BTA[1]
  BTA = round(BTA,2)

  def condition(x):
    return x > 0

  win = sum(condition(x) for x in returns)
  total = len(returns)
  win_ratio = win/total
  win_ratio = win_ratio*100
  win_ratio = round(win_ratio,2)

  IR = information_ratio(returns, benchmark.iloc[:,0])
  IR = round(IR,2)

  data = {'':['Start date', 'End date', 'Annual return', 'Cumulative return', 'Annual volatility','Winning day ratio', 'Sharpe ratio','Calmar ratio', 'Information ratio', 'Stability', 'Max Drawdown','Sortino ratio','Skew', 'Kurtosis', 'Tail Ratio', 'Common sense ratio', 'Daily value at risk',
              'Alpha', 'Beta'

  ],
        'Backtest':[str(returns.index[0]),str(returns.index[-1]), CAGR, CUM, VOL,f'{win_ratio}%', SR, CR, IR, STABILITY, MD, SOR, SK, KU, TA, CSR, VAR, AL, BTA]}

  # Create DataFrame

  df = pd.DataFrame(data)
  df.style.set_properties(**{'background-color': 'black',
                           'color': 'white',
                           'border-color':'black'})

  return df

    



