from django.conf.urls import url,include
from nilusadm import views


urlpatterns = [
    url(r'^users_viewers/$', views.users_viewers_list,name='users_viewers_list'),
    url(r'^permissions/(?P<pk>\d+)',views.edit_permissions,name='edit_permissions'),
    url(r'^config_conta/$',views.config_conta,name='config_conta'),


]