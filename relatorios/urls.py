from django.conf.urls import url,include
from relatorios import views


urlpatterns = [
    url(r'^lanfinanceiros/$', views.rel_lanfinanceiros,name='rel_lanfinanceiros'),

]
