from django.conf.urls import url,include
from niluscont import views


urlpatterns = [
    # Listagens dos cadastros
    url(r'^contratos/$',views.contratos_list,name='contratos_list'),
    url(r'^insere_contratos/$', views.create_contratos, name='create_contratos'),
    url(r'^insere_contratos/(?P<pk>\d+)$', views.edit_contratos, name='edit_contratos'),
    url(r'^contratos/(?P<pk>\d+)/apagar/$', views.delete_contratos, name='delete_contratos'),
    url(r'^os/$',views.os_list,name='os_list'),
    url(r'^insere_os/$', views.create_os, name='create_os'),
    url(r'^insere_os/(?P<pk>\d+)$', views.edit_os, name='edit_os'),
    url(r'^os/(?P<pk>\d+)/apagar/$', views.delete_os, name='delete_os'),

    #
]