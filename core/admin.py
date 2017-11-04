from django.contrib import admin

from nilusadm.models import Permissions,Sequenciais
from niluscad.models import Company,Propriety,Cadgeral,Ccusto,PlanoFinan


# Register your models here.


admin.site.register(Permissions)
admin.site.register(Sequenciais)
admin.site.register(Company)
admin.site.register(Propriety)
admin.site.register(Cadgeral)
admin.site.register(Ccusto)
admin.site.register(PlanoFinan)