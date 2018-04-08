from django.conf.urls import url
from .import views

urlpatterns = [
	url(r'^$',views.surveys, name='surveys'),
	 #url(r'^(?P<surveyid>[0-9]+)/$',views.question,name='question'),
	
]