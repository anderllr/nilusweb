from django.conf.urls import url,include
from django.contrib.auth.views import  login,logout
from accounts import views





urlpatterns = [
    url(r'^$',views.register, name='register'),
    url(r'^registro/sucesso/$' ,views.success_register, name='success_register'),
    url(r'^ativar/(?P<token>\w+)/$',views.user_active, name='user_active'),
    url(r'^recuperar/$',views.recover_account, name='recover_account'),
    url(r'^recuperar/(?P<id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.create_new_password, name='create_new_password'),
    url(r'^inclui_usuario',views.register_viewer,name='register_viewer'),
    url(r'^altera_usuario/(?P<pk>\d+)',views.edit_viewer,name='edit_viewer'),
    url(r'^reset_password/(?P<pk>\d+)',views.reset_password,name='reset_password')


]