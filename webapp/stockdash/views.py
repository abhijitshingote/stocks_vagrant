from django.shortcuts import render
from stockdash.models import PriceHistory,Return1Day,Return30Day,TotalReturn
from django.http import JsonResponse,HttpResponse
import json
import matplotlib.pyplot as plt, mpld3
from stockdash.filters import TotalReturnFilter

# Create your views here.

def index(request):
	gainers=TotalReturn.objects.using('stockdb').filter(marketcap__gt=10,return_1_day__gt=0).order_by('-return_1_day')[:10]
	losers=TotalReturn.objects.using('stockdb').filter(marketcap__gt=10,return_1_day__lt=0).order_by('return_1_day')[:10]
	return render(request,'stockdash/index.html',context={'gainers':gainers,'losers':losers})

def top_performers(request,sector):
	gainers=TotalReturn.objects.using('stockdb').filter(marketcap__gt=10,sector=sector,return_1_day__gt=0).order_by('-return_1_day')[:10]
	losers=TotalReturn.objects.using('stockdb').filter(marketcap__gt=10,sector=sector,return_1_day__lt=0).order_by('return_1_day')[:10]
	return render(request,'stockdash/index.html',context={'gainers':gainers,'losers':losers})

def somefunction(request):
	data={'message':'Your request was pretty successful'}
	# print(HttpResponse(
 #            json.dumps(data),
 #            content_type="application/json"
 #        ))
	# return HttpResponse(
 #            json.dumps(data),
 #            content_type="application/json"
#        )
	if request.is_ajax():
		return HttpResponse(
		json.dumps(data),
		content_type="application/json"
		)

def stock_screener(request):
	stockobjects = TotalReturnFilter(request.GET, queryset=TotalReturn.objects.using('stockdb').filter(
		marketcap__gt=0).exclude(return_30_day__isnull=True).order_by('-return_30_day'))
	# stockobjects=TotalReturn.objects.using('stockdb').filter(marketcap__gt=10)
	return render(request,'stockdash/stock_screener.html',context={'stockobjects':stockobjects})

def stockpage(request,symbol):
	symbol=symbol.upper()
	# print(symbol)
	totalreturnobj=TotalReturn.objects.using('stockdb').get(symbol=symbol)
	
	stockobj=PriceHistory.objects.using('stockdb').filter(symbol=symbol)
	prices=[(p.date_traded,p.close_price) for p in stockobj]
	prices=sorted(prices,key=lambda x:x[0])
	dates,prices=list(zip(*prices))
	fig = plt.figure(figsize=[12,5])
	# print(dates)
	plt.plot(dates,prices)
	myfig=mpld3.fig_to_html(fig)
	context=	{
		'totalreturnobj':totalreturnobj,
		'stockobj':stockobj,
		'myfig':myfig,
		'prices':list(zip(dates,prices))
		}
	return render(request,'stockdash/stockpage.html',context=context)