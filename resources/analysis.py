import numpy as np
import pandas as pd 
from datetime import datetime
import ta 
import json

def analysis(
    rates,
    multiplier=1,
    biasPercentage=60,
    consecutiveAndClose = 0,
    consecutiveOnly = 0,
    percentTimesCountedAtLeastMoreThan = 20,
):
    
    rates_frame=pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

    def toStrDate(x):
        return str(x["time"])[:10].replace("-",".")

    def toStrTime(x):
        return str(x["time"])[11:]
    
    rates_frame["date"]=rates_frame.apply(toStrDate,axis=1)
    rates_frame["time"]=rates_frame.apply(toStrTime,axis=1)
    
    rates_frame=rates_frame[['date',
    'time',
    'open',
    'high',
    'low',
    'close',
    'tick_volume',
    'real_volume',
    'spread',
    ]]

    rates_frame.columns=['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<TICKVOL>', '<VOL>', '<SPREAD>']

    DJ=rates_frame
    DJ['<ISGREEN>'] =  DJ['<CLOSE>'] > DJ['<OPEN>']
    DJ['<SIZE>'] =  DJ['<CLOSE>'] - DJ['<OPEN>']
    DJ['<VOLATILITY>'] =  DJ['<HIGH>'] - DJ['<LOW>']

    DJ.drop(['<VOL>'],axis=1,inplace=True)

    timeFrame = (int(DJ.iloc[1][1][1])-int(DJ.iloc[0][1][1]) ) * 60 + (int(DJ.iloc[1][1][3:5])-int(DJ.iloc[0][1][3:5]))
    CandlesInDay = 24 * (60//timeFrame)
    
    def candleToTime(j):
        minuteMult = CandlesInDay//24
        k=j//minuteMult
        sth=timeFrame*(j%minuteMult)
        return '{:02d}:{:02d}:00'.format(k,sth)

    uniqueDays = DJ.drop_duplicates(subset='<DATE>')
    uniqueDays = pd.DataFrame(uniqueDays)

    uniqueDaysCount=uniqueDays.shape[0]

    newnumparr = np.full((uniqueDaysCount*CandlesInDay,2),'',dtype=np.object_)

    for i in range(uniqueDaysCount):
        for j in range(CandlesInDay):
            newnumparr[(i*CandlesInDay)+j]=[uniqueDays.iloc[i][0],candleToTime(j)]

    newDF = pd.DataFrame(newnumparr,columns=['<DATE>','<TIME>'])

    newestDF = newDF.merge(DJ,on=['<DATE>','<TIME>'],how='left')

    # newestDF.drop(columns=['<OPEN>_x','<CLOSE>_x','<SIZE>_x','<VOLATILITY>_x','<ISGREEN>_x'],inplace=True)
    newestDF.fillna(0,inplace=True)

    newestDF['<EMA30>']= ta.trend.ema_indicator( newestDF['<CLOSE>'],window=30)
    newestDF['<EMA50>']= ta.trend.ema_indicator( newestDF['<CLOSE>'],window=50)
    newestDF['<EMA200>']= ta.trend.ema_indicator( newestDF['<CLOSE>'],window=200)

    def Upper(e):
        if e['<ISGREEN>'] : 
            return e['<HIGH>']-e['<CLOSE>']
        return e['<HIGH>']-e['<OPEN>']

    def Lower(e):
        if e['<ISGREEN>'] : 
            return e['<OPEN>']-e['<LOW>']
        return e['<CLOSE>']-e['<LOW>']


    newestDF['<UPPER>'] = newestDF.apply(Upper,axis=1)
    newestDF['<LOWER>'] = newestDF.apply(Lower,axis=1)

    
    # Compute RSI

    newestDF['<RSI>'] = ta.momentum.rsi(newestDF['<CLOSE>'],window=15) / 100
    newestDF['<CCI>'] = ta.trend.cci(close=newestDF['<CLOSE>'],high=newestDF['<HIGH>'],low=newestDF['<LOW>'],window=14)


    keltner = ta.volatility.KeltnerChannel(close=newestDF['<CLOSE>'],high=newestDF['<HIGH>'],low=newestDF['<LOW>'],window=20,window_atr=10,multiplier=2.5)
    newestDF['<KELTNER_H>'] = keltner.keltner_channel_hband()
    newestDF['<KELTNER_L>'] = keltner.keltner_channel_lband()
    newestDF['<KELTNER_M>'] = keltner.keltner_channel_mband()


    newestDF['<ATR_24>'] = ta.volatility.average_true_range(close=newestDF['<CLOSE>'],high=newestDF['<HIGH>'],low=newestDF['<LOW>'],window=12).apply(lambda e : e/100)


    newestDF["<GREEN>"] = newestDF["<ISGREEN>"].astype(int)




    # (newestDF,open="<OPEN>",close='<CLOSE>',high='<HIGH>',low='<LOW>',volume='<TICKVOL>',)

    
    newestDF

    


    
    list = []
    for i in range(len(newestDF)):
        
        date = newestDF.iloc[i]["<DATE>"]
        time = newestDF.iloc[i]["<TIME>"]
        isGreen = newestDF.iloc[i]["<ISGREEN>"]
        size = newestDF.iloc[i]["<SIZE>"]
        low = newestDF.iloc[i]["<LOW>"]
        high = newestDF.iloc[i]["<HIGH>"]
        volatility = newestDF.iloc[i]["<VOLATILITY>"]
        atr = newestDF.iloc[i]['<ATR_24>']
        
        list.append([date, time, isGreen, size,low,high, volatility,atr])


    
    days = []
    daysDfs = []
    for i in range(uniqueDaysCount): 
        daysDfs.append(pd.DataFrame(list[i*CandlesInDay: CandlesInDay*(i+1)],columns=[
            'date',
    'time',
    'isGreen',
    'size',
    'low',
    'high',
    'volatility',
    'atr',
        ]))
        days.append(list[i*CandlesInDay: CandlesInDay*(i+1)])


    

    maxList=np.zeros(CandlesInDay)
    minList=np.zeros(CandlesInDay)
    volatList=np.zeros(CandlesInDay)


    for i in (daysDfs):

        sth = i.loc[~((i['low'] == 0))]
        
        
        minList[(sth['size'].idxmin())]+=1
        maxList[(sth['size'].idxmax())]+=1
        volatList[(sth['volatility'].idxmax())]+=1

    
    # plt.figure(figsize=(10,8))

    # plt.bar(x=range(CandlesInDay)[1:-1],height=volatList[1:-1])


    
    # plt.bar(x=range(CandlesInDay)[1:-1],height=minList[1:-1])



    
    # plt.bar(x=range(CandlesInDay)[1:-1],height=maxList[1:-1])

    
    # plt.bar(x=range(CandlesInDay)[1:-1],height=minList[1:-1])

    
    # avgMultiplier = float(input('Only calculate candles bigger than X times the average (def=1) :' )or '1')
    avgMultiplier = float(multiplier)
    def eachDayMatrix(day):
        
        avgCandleBodySize=0
        avgCandleVolatility=0

        for i in range(len(day)):
            avgCandleBodySize+=abs(day[i][3])
            avgCandleVolatility+=abs(day[i][6])
        
        avgCandleBodySize/=len(day)
        avgCandleVolatility/=len(day)

        ansMatrix = np.zeros((CandlesInDay,CandlesInDay),dtype=int)
        countMatrix = np.zeros((CandlesInDay,CandlesInDay),dtype=int)
        
        for i in range(len(day)) : 
            for j in range (i,len(day)):
                # if abs(day[i][3])> avgCandleBodySize*avgMultiplier and abs(day[j][3])>0 : #SIZE
                if abs(day[i][6])> avgCandleVolatility*avgMultiplier and abs(day[j][6])>0 : #VOLATILITY
                # if abs(day[i][3]) > (day[i][5]*avgMultiplier) and abs(day[j][4])>0 : #ATR
                    countMatrix[i][j] += 1
                    if not(day[i][2] ^ day[j][2]):
                        ansMatrix[i][j]=1 
                    else:
                        ansMatrix[i][j]=-1
                        
                    continue
                ansMatrix[i][j]=0
                

        return [ansMatrix,countMatrix]

    ansVector = []
    countVector = []
    for i in range(len(days)):
        [ansVectorDay,countVectorDay] = eachDayMatrix(days[i])
        countVector.append(countVectorDay)
        ansVector.append(ansVectorDay)

    final = np.sum(ansVector, axis=0)
    countFinal = np.sum(countVector, axis=0)

    

    # final-=len(days)//2
    # plt.imshow(final)



    
    # plt.figure(figsize=(20,16))
    # sns.set(font_scale=2)
    # sns.heatmap(final,vmax=30,vmin=-30,annot=False)



    
    # plt.figure(figsize=(10,8))

    # sns.heatmap(countFinal,annot=False,)


    
    # float(input('Bias:')) 


    from io import StringIO
    output = StringIO()
    print(uniqueDaysCount,'Days ; ','Averages Multiplier :',avgMultiplier,file=output)
    for i in range(len(final)):
        for j in range (i,len(final)):
            percentageHigherThanAvg = int(countFinal[i][j]/uniqueDaysCount *10000) /100
            if( percentageHigherThanAvg < percentTimesCountedAtLeastMoreThan ):
                continue
            prob = int(abs(final[i][j]) / countFinal[i][j] *10000)/100 + 50.00
            if (biasPercentage<prob<100)and (not i==j):
                if(j-i==1):

                    print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% ++",
                    percentageHigherThanAvg,
                    'Consecutive',file=output) if final[i][j]>=0 else print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% --",
                    percentageHigherThanAvg,
                    'Consecutive',file=output)
                    continue

                if(j-i <= 120/timeFrame) and (not consecutiveOnly):

                    print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% ++",
                    percentageHigherThanAvg,
                    'Close',file=output) if final[i][j]>=0 else print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% --",
                    percentageHigherThanAvg,
                    'Close',file=output)
                    continue

                if not(consecutiveAndClose or consecutiveOnly): 
                    
                    print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% ++",
                    percentageHigherThanAvg,file=output) if final[i][j]>=0 else print(f"{i}-{j}",
                    f"{candleToTime(i)}-{candleToTime(j)}",
                    f"{prob}% --",
                    percentageHigherThanAvg,file=output)

    contents = output.getvalue()
    output.close()
    return({'final':str(final.tolist()),
            'countFinal':str(countFinal.tolist()),
            'text':contents})
    

