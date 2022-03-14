import csv

def add_to_csv(ticker,ea_wallet):
    ea_wallet.insert(0,ticker)
    with open('trade_history.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(ea_wallet)
    
