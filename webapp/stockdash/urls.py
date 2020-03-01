from django.urls import path
from . import views

urlpatterns = [ 

	path('',views.index,name='index'),
	path('<slug:sector>/',views.top_performers,name='top_performers')
]