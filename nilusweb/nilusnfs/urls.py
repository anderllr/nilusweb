from django.conf.urls import url,include
from nilusnfs import views


urlpatterns = [
    # Listagens dos cadastros
    url(r'^pnfs/$',views.paramnfs_list,name='paramnfs_list'),
    url(r'^insere_parametros/$', views.create_paramnfs, name='create_paramnfs'),
    url(r'^insere_parametros/(?P<pk>\d+)$', views.edit_paramnfs, name='edit_paramnfs'),
    url(r'^paramnfs/(?P<pk>\d+)/apagar/$', views.delete_paramnfs, name='delete_paramnfs'),
    url(r'^faturamento/$',views.fat_list,name='fat_list'),
    url(r'^notasemitidas/$',views.nfs_list,name='nfs_list'),
    url(r'^notasemitidas/atualiza/(?P<pk>\d+)$',views.refresh_nfs,name='refresh_nfs'),
    url(r'^notasemitidas/info/(?P<pk>\d+)$', views.info_nfs, name='info_nfs'),
    url(r'^notasemitidas/cancela/(?P<pk>\d+)$',views.cancel_nfs,name='cancel_nfs')
]