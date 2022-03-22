import get
import indicator
import slackbot
import datetime
import time
import trade
import save

wallet = {'BTC': ['', '', 0, 0, 0, 450000, "", ], 'ETH': ['', '', 0, 0, 0, 450000, ""], 'XRP': ['', '', 0, 0, 0, 450000, ""],'EOS': ['', '', 0, 0, 0, 450000, ""],'ADA': ['', '', 0, 0, 0, 450000, ""]}
# wallet = {'XRP': ['', '', 0, 0, 0, 500000]}
# 0 : 매수일
# 1 : 매도일
# 2 : 매수가
# 3 : 매도가
# 4 : 볼륨(수량)
# 5 : 자본금
# 6 : 거래 중지일
# 7 : 현재 포지션

# 나중에 XRP / LTC 추가
while True:
    bid_const = 4.5
    ask_const = 2
    starttime = time.time()
    tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-EOS', 'KRW-ADA']
    akey = ""
    skey = "" 
    
    price_dict = get.get_current_price(tickers)
    
    current_balance, current_ticker = get.get_current_balance(akey,skey)
    current_ticker = get.get_list_intersection(tickers,current_ticker)
    bid_ticker = [i for i in tickers if i not in current_ticker]
    for b in current_ticker:
        t = b[4:]
        for ba in current_balance:
            if ba['currency'] == t:
                if wallet[t][0] == "":
                    wallet[t][0] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                wallet[t][2]=float(ba['avg_buy_price'])
                wallet[t][4]=float(ba['balance'])
    print(wallet)

    for ticker in tickers:
        ma_dict = {}
        ma_const = [192, 48, 24]
        atr_const = 24
        # 데이터 가져오기
        data = get.get_past_data('{}'.format(ticker),60,max(ma_const)) # interva & count
        # 이동 평균 계산하기
        for m in ma_const:
            ma_dict[str(m)] = data.head(m)['trade_price'].mean()
        ma_dict['past48'] = data['trade_price'].iloc[1:49].mean()
        ma_dict['past24'] = data['trade_price'].iloc[1:25].mean()
        # ma_dict['2past24'] = data['trade_price'].iloc[2:26].mean()
        # ATR 계산하기
        atr = indicator.ATR(data,atr_const)
        if ticker in bid_ticker:
            target_price = ma_dict['192'] + bid_const*atr # 매수 가격 
            if price_dict['{}'.format(ticker)]>target_price and (ma_dict['24']-ma_dict['past24'])>(ma_dict['48']-ma_dict['past48']):
                side = "bid"
                # 매수 함수 실행
                # trade.trade(akey,skey,side,ticker,wallet) 
                # Wallet 수정
                wallet[ticker[4:]][0] =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 매수일
                # Slack 메세지 전송
                message = "{} : {} bid".format(ticker,target_price)
                slackbot.post_message(message)
            print("{} : {} bid".format(ticker, target_price))
                    
        if ticker in current_ticker:
            target_price = wallet[ticker[4:]][2] - ask_const*atr # 손절 가격
            if price_dict['{}'.format(ticker)]<target_price:
                side = "ask"
                # 매도 함수 실행
                trade.trade(akey,skey,side,ticker,wallet)
                # Wallet 수정
                wallet[ticker[4:]][1] =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 매도일
                wallet[ticker[4:]][3] =  price_dict['{}'.format(ticker)] # 매도가
                wallet[ticker[4:]][5] =  price_dict['{}'.format(ticker)]*wallet[ticker[4:]][4]*0.9995 # 자본금 수정
                # Slack 메세지 전송
                message = "{} : {} ask".format(ticker,target_price)
                slackbot.post_message(message)
                # CSV 파일 저장
                save.add_to_csv(ticker,wallet[ticker[4:]])
                if float(wallet[ticker[4:]][3])<float(wallet[ticker[4:]][4]):
                    wallet[ticker[4:]][6] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[0:10]
            ask_6 = ma_dict['192'] + 6*atr
            message = "{} :: L : {}  / C : {} / A6 : {}".format(ticker,target_price, price_dict['{}'.format(ticker)],ask_6)
            slackbot.post_message(message)        
            print("{} : {} loss".format(ticker, target_price))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(300.0 - ((time.time() - starttime) % 60.0))