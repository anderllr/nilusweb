from django.conf.urls import url,include
from principal import views


urlpatterns = [
    url(r'^$', views.principal,name='principal'),
    url(r'^profile/$', views.profile,name='profile'),
    url(r'^alterar_senha/$',views.update_password, name='altera_senha'),
    url(r'^ajax/$', views.company_propriety, name='company_propriety'),
    url(r'^ajax/indice$', views.indice_cotacao, name='indice_cotacao'),
    url(r'^adm/', include('nilusadm.urls')),
    url(r'^cad/', include('niluscad.urls')),
    url(r'^fin/', include('nilusfin.urls')),
    # url('r^rel/', include('relatorios.urls')),
    url(r'^fin/lanc/', include('lancfinanceiros.urls')),


]