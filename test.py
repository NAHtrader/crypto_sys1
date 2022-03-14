import csv

a = ['2022-03-12 15:55:19', '2022-03-12 15:57:19', 23000.0, 28000, 2.19735497, 61495.17619042]
a.insert(0,'DOT')

with open('trade_history.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(a)
