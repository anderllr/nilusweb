from django.conf.urls import url,include
from nilusfin import views


urlpatterns = [
    # Listagens dos cadastros
    url(r'^conta/$',views.conta_list,name='conta_list'),
    url(r'^indice/$',views.indice_list,name='indice_list'),
    url(r'^cotacao/(?P<pk>\d+)$',views.cotacao_list,name='cotacao_list'),

    # Conta
    url(r'^insere_conta/$', views.create_conta, name='create_conta'),
    url(r'^insere_conta/(?P<pk>\d+)$', views.edit_conta, name='edit_conta'),
    url(r'^conta/(?P<pk>\d+)/apagar/$', views.delete_conta, name='delete_conta'),


    # Indices
    url(r'^insere_indice/$', views.create_indice, name='create_indice'),
    url(r'^indice/(?P<pk>\d+)/apagar/$', views.delete_indice, name='delete_indice'),
    # url(r'^permissions/(?P<pk>\d+)',views.edit_permissions,name='edit_permissions'),


    # Cotações
    url(r'^indice/insere_cotacao/$', views.create_cotacao, name='create_cotacao'),
    # url(r'^cotacao/(?P<pk>\d+)/apagar/$', views.delete_cotacao, name='delete_cotacao'),


    # Recebiveis
    # url(r'^recebiveis/',include('recebiveis.urls')),

]
