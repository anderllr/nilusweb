from django.contrib import admin

from nilusadm.models import Permissions,Sequenciais
from niluscad.models import Company,Propriety,Cadgeral,Ccusto,PlanoFinan,Talhao,Grupodre
from nilusfin.models import Contafinanceira
from principal.models import Instancia
from nilusfin.models import Indice,Cotacao
from recebiveis.models import Recebiveis
from lancfinanceiros.models import Lancamentos,Movtos_lancamentos
from niluscont.models import Contratos,OrdemServico

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
admin.site.register(Contafinanceira)
admin.site.register(Movtos_lancamentos)
admin.site.register(Grupodre)
admin.site.register(Contratos)
admin.site.register(OrdemServico)