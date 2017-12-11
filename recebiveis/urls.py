from django.conf.urls import url, include
from nilusfin import views
from recebiveis import views

urlpatterns = [
    # Listagens dos cadastros
     url(r'^$', views.titrec_list, name='titrec_list'),


    # Titulos a Receber
    url(r'^insere_titulo_receber$',views.create_titrec,name='create_titrec'),
    url(r'^insere_titulo_receber/(?P<pk>\d+)$', views.edit_titrec, name='edit_titrec'),
    url(r'^recebiveis/(?P<pk>\d+)/apagar/$', views.delete_titrec, name='delete_titrec'),

]
