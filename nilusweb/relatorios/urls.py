from django.conf.urls import url,include
from relatorios import views


urlpatterns = [
    url(r'^lanfinanceiros/$', views.rel_lanfinanceiros,name='rel_lanfinanceiros'),
    url(r'^extrato_financeiro/$',views.rel_extratofinanceiro,name='rel_extratofinanceiro'),
    url(r'^rel_demonstrativo/$',views.rel_dre,name='rel_dre'),
    url(r'^rel_os/$',views.rel_os,name='rel_os'),

]
