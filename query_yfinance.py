import datetime
import re
from io import StringIO

import pandas as pd
import sqlalchemy

import requests
import yfinance as yf

engine = sqlalchemy.create_engine('postgresql://vagrant:vagrant@0.0.0.0:5432/stockdb')
with open('/home/vagrant/autofile','a+') as f:
	f.write('Program started running at :'+datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")+'\n')

def GetStockList(url):
	r = requests.get(url)
	s=str(r.content,'utf-8')
	data = StringIO(s) 
	return pd.read_csv(data)['Symbol'].tolist()

req=requests.get(
'https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/64dd3e9582b936b0352fdd826ecd3c95/constituents_json.json')
sp500json=req.json()
sp500symbols=[]
for each in sp500json:
	sp500symbols.append(each['Symbol'])

sp500symbols.remove('MON')

# url_nasdaq='''https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'''
# url_amex='''https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'''
# url_nyse='''https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'''

# uniquesymbolsonly=list(set(GetStockList(url_nasdaq)+GetStockList(url_nyse)+GetStockList(url_amex)+sp500symbols))
# uniquesymbolsonly= [sym for sym in uniquesymbolsonly if re.match("^[a-zA-Z]*$", sym)]

# for sym in sp500symbols:
# 	try:
# 		uniquesymbolsonly.remove(sym)
# 		uniquesymbolsonly.insert(0,sym)
# 	except:
# 		continue

print('Got Stock Symbol Lists......Total Symbols - ',str(len(sp500symbols)))




def Get_Data_From_Yahoo_full_load(stocklist,period='1y'):

	print("Running FULL LOAD ")
	if not isinstance(stocklist,(list,tuple)):
		stocklist=[stocklist]
	
	stockinfo={}
	stockpricehistory=pd.DataFrame()
	
	for i in range(0,len(stocklist),100):

		print('Getting Chunk..'+str((i/100)+1)+' of '+str(len(stocklist)/100),flush=True)
		symbol_list_chunk=stocklist[i:i+100]
		# when the last chunk only contains one element, the returned df is in a different format
		# below if block is ensure returned df remains in same format
		if len(symbol_list_chunk) == 1:
			symbol_list_chunk.append("AAPL")
		stocklist_str=" ".join(symbol_list_chunk)
		print(stocklist_str)
		df=yf.download(stocklist_str,period='1y')
		indiv_df=pd.DataFrame()
		main_big_df=pd.DataFrame()
		downloadedsymbols=list(set([col[1] for col in df.columns]))
		for idx,symbol in enumerate(downloadedsymbols):
			print(symbol + '...'+str(idx+i+1)+' of '+str(len(stocklist)),flush=True)
			for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
				indiv_df[col]=df[col][symbol]
			indiv_df['symbol']=symbol
			main_big_df=main_big_df.append(indiv_df)
		main_big_df.to_sql('stock_price_history',engine,schema='public',if_exists='append')



def Get_Data_From_Yahoo_daily(stocklist,period='1d'):

	print("Running DAILY ")
	if not isinstance(stocklist,(list,tuple)):
		stocklist=[stocklist]
	
	stockinfo={}
	stockpricehistory=pd.DataFrame()
	
	maxdate=pd.read_sql_query('''select max("Date") from stock_price_history 
		''',engine)['max'].values[0]
	maxdate=datetime.datetime.utcfromtimestamp(maxdate.tolist()/1e9)
	today_date_str=datetime.date.today().strftime("%Y-%m-%d")
	tomorrow_date_str=(datetime.date.today() +datetime.timedelta(days=1)).strftime("%Y-%m-%d")
	print('Maxdate ',maxdate)
	print('today_date_str ',today_date_str)
	print('tomorrow_date_str ',tomorrow_date_str)
	if datetime.date.today() > maxdate.date():
		for i in range(0,len(stocklist),100):

			print('Getting Chunk..'+str((i/100)+1)+' of '+str(len(stocklist)//100),flush=True)
			symbol_list_chunk=stocklist[i:i+100]
			# when the last chunk only contains one element, the returned df is in a different format
			# below if block is ensure returned df remains in same format
			if len(symbol_list_chunk) == 1:
				symbol_list_chunk.append("AAPL")
			stocklist_str=" ".join(symbol_list_chunk)
			print('Getting data for ......'+today_date_str+'...'+tomorrow_date_str)
			df=yf.download(stocklist_str,start=today_date_str,end=tomorrow_date_str)
			# adjusting for duplicates for same date for same symbol 
			df=df.iloc[-1:,:]
			print('Downloaded DataFrame\n',df.head())
			indiv_df=pd.DataFrame()
			main_big_df=pd.DataFrame()
			downloadedsymbols=list(set([col[1] for col in df.columns]))
			for idx,symbol in enumerate(downloadedsymbols):
				print(symbol + '...'+str(idx+i+1)+' of '+str(len(stocklist)),flush=True)
				for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
					indiv_df[col]=df[col][symbol]
				indiv_df['symbol']=symbol
				main_big_df=main_big_df.append(indiv_df)
			main_big_df.to_sql('stock_price_history',engine,schema='public',if_exists='append')



def Get_Ticker_Information(stocklist):
	for i in range(0,len(stocklist),100):
		symbol_list_chunk=stocklist[i:i+100]
		stocklist_str=" ".join(symbol_list_chunk)
		tickers=yf.Tickers(' '.join(stocklist_str))
		for tickerobj in tickers.tickers:
			try:
				stockinfodict_updated={k:[v] for k,v in tickerobj.info.items() if k in 
					('marketCap','sector','industry','symbol','shortName')}
				stockinfo_df=pd.DataFrame(stockinfodict_updated)
				stockinfo_df.to_sql('stockinfo',engine,schema='public',if_exists='append')
			except:
				continue



if not engine.dialect.has_table(engine, table_name='stock_price_history',schema='public'):
	Get_Data_From_Yahoo_full_load(sp500symbols)

else:
	Get_Data_From_Yahoo_daily(sp500symbols)


with open('/home/vagrant/autofile','a+') as f:
	f.write('Program finished running at :'+datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")+'\n')
