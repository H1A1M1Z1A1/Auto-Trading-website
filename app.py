
from msilib.schema import Error
from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import numpy as np
from binance.client import Client
from binance import BinanceSocketManager
from binance.enums import*
from binance.exceptions import BinanceAPIException, BinanceOrderException
import time
import datetime
from binance.enums import HistoricalKlinesType
from datetime import datetime
app = Flask(__name__, template_folder='templates', static_folder='static')
client = Client()
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')
def getmindata(symbol, interval, start):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, start))
    frame = frame.iloc[:, :6]
    frame.columns = ['opentime', "open", 'high', 'low', 'close', 'volume']
    frame.opentime = frame['opentime'].add(19800000)
    frame = frame.set_index('opentime')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    frame.reset_index(inplace=True)    
    frame['min']=pd.DatetimeIndex(frame['opentime']).minute
    return frame

@app.route('/')
def welcome():

    return render_template('index.html')

@app.route("/withraw")
def withraw():
    return render_template("withraw.html")
    


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        option = str(request.form['option'])
        if option=="back":
            return render_template('indexb.html',option="back")
        else:
            return render_template('index2.html',option="alert")


@app.route('/submi', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        option = str(request.form['option'])
        symbol=request.form.getlist('symbol')
        timeframe=str(request.form['timeframe'])
        strat=str(request.form['strategy'])
        if option=="back":
            back=str(request.form['back'])



    class coin:
        def __init__(self,i):
            self.i=i
            i=self.i
            self.buy_at=dn.iloc[i,4]
            self.buy_time=dn.iloc[i,0]
            self.length=((dn.iloc[i,2]-dn.iloc[i,3])/(dn.iloc[i,3]))*100
            if (dn.iloc[i,1]>dn.iloc[i,4]) & (dn.iloc[i,4]-dn.iloc[i,3]>dn.iloc[i,2]-dn.iloc[i,1]):
                self.q=((dn.iloc[i,2]-dn.iloc[i,4])/(dn.iloc[i,2]-dn.iloc[i,3]+.0000011))
                self.tail=dn.iloc[i,3]
                self.strategy="long"
                
            elif (dn.iloc[i,1]>dn.iloc[i,4]) & (dn.iloc[i,4]-dn.iloc[i,3]<dn.iloc[i,2]-dn.iloc[i,1]):
                self.q=((dn.iloc[i,1]-dn.iloc[i,3])/(dn.iloc[i,2]-dn.iloc[i,3]+.0000011))
                self.tail=dn.iloc[i,2]
                self.strategy="short"
                
                
            elif (dn.iloc[i,4]>dn.iloc[i,1]) & (dn.iloc[i,1]-dn.iloc[i,3]>dn.iloc[i,2]-dn.iloc[i,4]):
                self.q=((dn.iloc[i,2]-dn.iloc[i,1])/(dn.iloc[i,2]-dn.iloc[i,3]+.0000011))
                self.tail=dn.iloc[i,3]
                self.strategy="long"
                
                
            elif (dn.iloc[i,4]>dn.iloc[i,1]) & (dn.iloc[i,2]-dn.iloc[i,4]>dn.iloc[i,1]-dn.iloc[i,3]):
                self.q=((dn.iloc[i,4]-dn.iloc[i,3])/(dn.iloc[i,2]-dn.iloc[i,3]+.0000011))
                self.tail=dn.iloc[i,2]
                self.strategy="short"           
            else :  
                self.q=1
                self.strategy="none"

    money=100
    # print(option)
    if option=="alert":
        if timeframe=="1m" or timeframe=="5m" :
            back="3h"
        elif timeframe=="30m" or timeframe=="1h":
            back="3d"
        else:
            back="30d"
    dn=getmindata(symbol[0],timeframe,back)
    ds=pd.DataFrame()
    li=symbol
    o=0
    i=2
    while (option=="alert"):
        cl=coin(-1)    
        if len(li)!=1:
            dn=getmindata(li[o],timeframe,back)
            print(strat)
            dn['MA1']=dn['close'].rolling(window=int(strat[:2])).mean()
            dn['MA2']=dn['close'].rolling(window=int(strat[2:])).mean()          
            o=o+1
        else:
            dn=getmindata(li[0],timeframe,back)
            dn['MA1']=dn['close'].rolling(window=int(strat[:2])).mean()
            dn['MA2']=dn['close'].rolling(window=int(strat[2:])).mean()
        if ((option=="alert") & (coin(-2).q<.4) & (strat=="1111")) or ((dn.iloc[-2,8]<=dn.iloc[-2,7]) & (dn.iloc[-1,8]>=dn.iloc[-1,7])& (strat!="1111")) or ((dn.iloc[-2,8]>=dn.iloc[-2,7]) & (dn.iloc[-1,8]<=dn.iloc[-1,7]) & (strat!="1111")): 
            return render_template("index2.html",d=li[o-1])            
        elif o==len(li):
            o=0
    if len(li)!=1:
        dn=getmindata(li[0],timeframe,back)      
    while (option=="back"):
        if i<len(dn):
            cl=coin(i)
        else:
            break
        strategy=cl.strategy
        if (cl.q<.4)&(cl.length>3):
            a=i+1
            profit=.01
            f=.001
            strategy=cl.strategy

            x=profit
            stop_loss=cl.tail
            # if ((strategy=="long") & (dn.iloc[i-1,4]-dn.iloc[i-1,1]<0)) or ((strategy=="short") & (dn.iloc[i-1,4]-dn.iloc[i-1,1]>0)):
            


        

            while a<len(dn.index):


                if (dn.iloc[a,3]<=stop_loss ) & (strategy=="long") :
                    loss=((cl.buy_at-stop_loss)/cl.buy_at)+f       
                    i=a
                    money=money-abs(loss)*money   
                    ds=ds.append({"position":strategy,"buy_time":cl.buy_time,"buy_price":cl.buy_at,'sell_time':dn.iloc[a,0],"sell_price":dn.iloc[a,3],'profit%':-abs(loss), 'Amount':money}, ignore_index=True)

                    break
                elif (dn.iloc[a,4]>cl.buy_at+x*cl.buy_at) & (strategy=="long") :
   
                    # profit=profit-f
                    profit=((cl.buy_at-dn.iloc[a,4])/cl.buy_at)-f
                    i=a
                    money=money+abs(profit)*money
                    ds=ds.append({"position":strategy,"buy_time":cl.buy_time,"buy_price":cl.buy_at,'sell_time':dn.iloc[a,0],"sell_price":dn.iloc[a,3],'profit%':abs(profit), 'Amount':money}, ignore_index=True)

                    break

                elif (dn.iloc[a,2]>=stop_loss) & (strategy=="short"):
                    loss=((cl.buy_at-stop_loss)/cl.buy_at)-f
                    money=money-abs(loss)*money
                    ds=ds.append({"position":strategy,"buy_time":cl.buy_time,"buy_price":cl.buy_at,'sell_time':dn.iloc[a,0],"sell_price":dn.iloc[a,3],'profit%':-abs(loss), 'Amount':money}, ignore_index=True)   
                    i=a
                    break

                elif (dn.iloc[a,4]<=cl.buy_at-x*cl.buy_at) & (strategy=="short"):
                    # profit=-profit+f
                    profit=((cl.buy_at-dn.iloc[a,4])/cl.buy_at)-f
                    money=(money+abs(profit)*money)
                    ds=ds.append({"position":strategy,"buy_time":cl.buy_time,"buy_price":cl.buy_at,'sell_time':dn.iloc[a,0],"sell_price":dn.iloc[a,3],'profit%':abs(profit), 'Amount':money}, ignore_index=True)
                    i=a

                    break
                else:

                    a=a+1
            if a>=len(dn):
                break
        else:
            i=i+1
    t=len(ds)
    if len(ds)!=0:
        perc=(float(ds["Amount"][-1:])-100)
    else:
        perc=0
    return render_template('result.html',  tables=[ds.to_html(classes='data')], titles=ds.columns.values,t=t,symb=li[0],perc=round(perc,3))

# @app.errorhandler(Exception)          
# def basic_error(e):          
#     return render_template('no.html')

if __name__ == '__main__':
    app.run(debug=True)

