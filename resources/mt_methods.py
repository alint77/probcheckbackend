
from datetime import datetime
import MetaTrader5 as mt5
from .analysis import analysis
import numpy as np


def getAllSymbolNames():
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # get every symbol name
    symbols=mt5.symbols_get()
    print('SymbolsCount:',len(symbols))
    mt5.shutdown()


    symbolNames = []

    for s in symbols:
        symbolNames.append(s.name)
    return symbolNames

def copy_rates_from_pos(symbol,timeframe,start_pos,count,multiplier=0,threshold=60,closeOnly=0):
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    
    
    match timeframe:
        case "M5":
            tf=mt5.TIMEFRAME_M5
        case "M15":
            tf=mt5.TIMEFRAME_M15
        case "M20":
            tf=mt5.TIMEFRAME_M20
        case "M30":
            tf=mt5.TIMEFRAME_M30
        case "H1":
            tf=mt5.TIMEFRAME_H1
        case "H2":
            tf=mt5.TIMEFRAME_H2
        case "H4":
            tf=mt5.TIMEFRAME_H4
        case _ : 
            mt5.shutdown()
            raise ValueError("pass the right timeframe as string eg: 'M1'")

    # get data
    print("retreiving data from mt5...")
    rates=mt5.copy_rates_from_pos(symbol,tf,start_pos,count)
    print("data received ")
    mt5.shutdown()
    analysedData = analysis(rates,multiplier=multiplier,biasPercentage=threshold,consecutiveAndClose=closeOnly)
    print("Analyse completed! : ".capitalize(),analysedData)
    return analysedData

def get_historical_data(symbol,timeframe,start_pos,count,multiplier=0,threshold=60,closeOnly=0):
    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code = ",mt5.last_error())
        quit()
    
    
    match timeframe:
        case "M5":
            tf=mt5.TIMEFRAME_M5
        case "M15":
            tf=mt5.TIMEFRAME_M15
        case "M20":
            tf=mt5.TIMEFRAME_M20
        case "M30":
            tf=mt5.TIMEFRAME_M30
        case "H1":
            tf=mt5.TIMEFRAME_H1
        case "H2":
            tf=mt5.TIMEFRAME_H2
        case "H4":
            tf=mt5.TIMEFRAME_H4
        case "D1":
            tf=mt5.TIMEFRAME_D1
        case _ : 
            mt5.shutdown()
            raise ValueError("pass the right timeframe as string eg: 'M1'")

    # get data
    print("retreiving data from mt5...")
    rates=(mt5.copy_rates_from_pos(symbol,tf,start_pos,count))
    print("data received")
    mt5.shutdown()
    return {"rates":str(rates.tolist())}

