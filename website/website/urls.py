from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from survey import views as survey_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',include('survey.urls')),
    url(r'^(?P<sid>[0-9]+)/$',survey_views.dashboard,name='dashboard'),
      url(r'^addquestion/$',survey_views.addquestion,name='addquestion'),
    url(r'^signup/$', survey_views.signup, name='signup'),
    url(r'^login/$', auth_views.login,{'template_name': 'survey/index.html'},name='index'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
