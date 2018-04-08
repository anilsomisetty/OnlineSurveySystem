from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from survey import views as survey_views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$',include('survey.urls')),
  url(r'^(?P<sid>[0-9]+)/$',survey_views.dashboard,name='dashboard'),
  url(r'^addquestion/$',survey_views.addquestion,name='addquestion'),
  url(r'^(?P<sid>[0-9]+)/deletequestion/(?P<id>[0-9]+)$',survey_views.deletequestion,name='deletequestion'),
  url(r'^(?P<sid>[0-9]+)/editquestion/(?P<id>[0-9]+)$',survey_views.editquestion,name='editquestion'),
  url(r'^signup/$', survey_views.signup, name='signup'),
  url(r'^login/$', auth_views.login,{'template_name': 'survey/index.html'},name='index'),
  url(r'^logout/$', auth_views.logout, name='logout'),
  url(r'^profile/',survey_views.profile, name='profile'),
  url(r'^editprofile/',survey_views.update_profile, name='update_profile'),
  url(r'^updatepassword/',survey_views.change_password, name='change_password'),
  url(r'^showsurveys/',survey_views.showsurveys, name='showsurveys'),
  url(r'^hissurveys/',survey_views.hissurveys, name='hissurveys'),
  url(r'^getresults/(?P<sid>[0-9]+)$',survey_views.getresults,name='getresults'),
]
