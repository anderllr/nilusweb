from django.contrib import admin

from nilusadm.models import Permissions,Sequenciais
from niluscad.models import Company,Propriety,Cadgeral,Ccusto,PlanoFinan,Talhao
from principal.models import Instancia
from nilusfin.models import Indice,Cotacao
from recebiveis.models import Recebiveis
from lancfinanceiros.models import Lancamentos


# Register your models here.


admin.site.register(Permissions)
admin.site.register(Sequenciais)
admin.site.register(Company)
admin.site.register(Propriety)
admin.site.register(Cadgeral)
admin.site.register(Ccusto)
admin.site.register(PlanoFinan)
admin.site.register(Instancia)
admin.site.register(Indice)
admin.site.register(Cotacao)
admin.site.register(Recebiveis)
admin.site.register(Talhao)
admin.site.register(Lancamentos)
