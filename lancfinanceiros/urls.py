from django.conf.urls import url, include
from nilusfin import views
from lancfinanceiros import views

urlpatterns = [

    url(r'^$', views.lancfin_list, name='lancfin_list'),
    url(r'^lancamentos/baixas',views.baixfin_list,name='baixfin_list'),

    url(r'^insere_receita$',views.create_receita,name='create_receita'),
    url(r'^insere_despesa$',views.create_despesa,name='create_despesa'),
    url(r'^insere_receita/(?P<pk>\d+)$', views.edit_receita, name='edit_receita'),
    url(r'^insere_despesa/(?P<pk>\d+)$', views.edit_despesa, name='edit_despesa'),
    url(r'^receita/(?P<pk>\d+)/apagar/$', views.delete_receita, name='delete_receita'),

    # url(r'^fin/lanc/baixas', include('nilusfin.urls')),
    # url(r'^despesa/(?P<pk>\d+)/apagar/$', views.delete_despesa, name='delete_despesa'),


]
