from django.conf.urls import url,include
from niluscad import views


urlpatterns = [
    # Listagens dos cadastros
    url(r'^empresas/$', views.company_list,name='company_list'),
    url(r'^propriedades/$',views.propriety_list,name='propriety_list'),
    url(r'^cadgeral/$',views.cadgeral_list,name='cadgeral_list'),
    url(r'^ccusto/$',views.ccusto_list,name='ccusto_list'),
    url(r'^planofinan/$',views.planofinan_list,name='planofinan_list'),


    # Empresas
    url(r'^insere_empresa/$',views.create_company,name='create_company'),
    url(r'^insere_empresa/(?P<pk>\d+)$',views.edit_company,name='edit_company'),
    # url(r'^insere_empresa/prop/(?P<pk>\d+)$',views.edit_company_prop,name='edit_company_prop'),
    url(r'^empresas/(?P<pk>\d+)/apagar/$', views.delete_company, name='delete_company'),


    # Propriedades
    url(r'^propriedades/insere_propriedade/$', views.create_propriety, name='create_propriety'),
    url(r'^propriedades/(?P<pk>\d+)/apaga_propriedade/$', views.delete_propriety, name='delete_propriety'),
    url(r'^propriedades/(?P<pk>\d+)/edita_propriedade/$', views.edit_propriety, name='edit_propriety'),

    # Cadastros Gerais
      url(r'^insere_cadastro/$', views.create_cadgeral, name='create_cadgeral'),
      url(r'^insere_cadastro/(?P<pk>\d+)$', views.edit_cadgeral, name='edit_cadgeral'),
      url(r'^cadgeral/(?P<pk>\d+)/apagar/$', views.delete_cadgeral, name='delete_cadgeral'),


    # Centros de Custo
       url(r'^insere_ccusto/$', views.create_ccusto, name='create_ccusto'),
       url(r'^insere_ccusto/(?P<pk>\d+)$', views.edit_ccusto, name='edit_ccusto'),
       url(r'^ccusto/(?P<pk>\d+)/apagar/$', views.delete_ccusto, name='delete_ccusto'),


    # Plano Financeiro
       url(r'^insere_planofinan/$', views.create_planofinan, name='create_planofinan'),
       url(r'^insere_planofinan/(?P<pk>\d+)$', views.edit_planofinan, name='edit_planofinan'),
       url(r'^planofinan/(?P<pk>\d+)/apagar/$', views.delete_planofinan, name='delete_planofinan'),

    # url(r'^permissions/(?P<pk>\d+)',views.edit_permissions,name='edit_permissions'),


]