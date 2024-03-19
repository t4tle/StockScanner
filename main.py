import yfinance as yf
import pandas as pd
import datetime as dt


dataF = yf.download("MGC=F", start="2024-2-1", end="2024-3-13", interval='15m')



#
#
#

def trend_sorter(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    high = df.High.iloc[-1]
    low = df.Low.iloc[-1]
    

    if (open>close): 
        #bear
        return "bearish"

    elif(open<close):
        #bull
        return "bullish"
    
    else:
        return "unconclusive" 


def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish Pattern
    if (open>close and 
    previous_open<previous_close and 
    close<previous_open and
    open>=previous_close):
        return "bearish engulfing"

    # Bullish Pattern
    elif (open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close):
        return "Bullish engulfing"
    
    # No clear pattern
    else:
        return "no pattern"
    

def candle_sorter(df):# check if candle is a doji
    open = df.Open.iloc[-2]
    close = df.Close.iloc[-2]
    high = df.High.iloc[-2]
    low = df.Low.iloc[-2]

    if (open>close): 
        #bear
        return "bearish"

    elif(open<close):
        #bull
        return "bullish"
    
    else:
        return "unconclusive" 



candle_position = []
engulfing_signal = []
engulfing_signal.append("no pattern")
for i in range(1,len(dataF)):
    df = dataF[i-1:i]
    df1 = dataF[i-1:i+1]
    
    candle_position.append(trend_sorter(df))
    engulfing_signal.append(signal_generator(df1))

candle_position.append(trend_sorter(df.tail(1)))


dataF["candle position"] = candle_position
dataF["engulfing signal"] = engulfing_signal



print(dataF.iloc[:,:])
#dataF.to_excel(r'outputs\output.xlxs')