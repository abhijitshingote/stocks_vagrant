from django.shortcuts import render
from stockdash.models import PriceHistory,Return1Day
from django.http import JsonResponse,HttpResponse
import json
# Create your views here.

def index(request):
	oneday_objects=Return1Day.objects.using('stockdb').filter(marketcap__gt=1).order_by('-return_percentage')[:10]
	return render(request,'stockdash/index.html',context={'oneday_objects':oneday_objects})

def top_performers(request,sector):
	# if sector=='Financials':
	# 	sector='Financial Services'
	oneday_objects=Return1Day.objects.using('stockdb').filter(marketcap__gt=1,sector=sector).order_by('-return_percentage')[:10]
	return render(request,'stockdash/index.html',context={'oneday_objects':oneday_objects})

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

def huh(request):
	# return HttpResponse("Get out")
	print('HUHUHU')
	return render(request,'stockdash/huh.html')