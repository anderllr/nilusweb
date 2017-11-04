from django.conf.urls import url,include
from principal import views


urlpatterns = [
    url(r'^$', views.principal,name='principal'),
    url(r'^profile/$', views.profile,name='profile'),
    url(r'^alterar_senha/$',views.update_password, name='altera_senha'),
    url(r'^adm/', include('nilusadm.urls')),
    url(r'^cad/', include('niluscad.urls')),

]