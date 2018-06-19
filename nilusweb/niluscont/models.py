from nilusnfs.models import TmpFat
from django.db import models
from django.db.models.signals import post_save


# Create your models here.


class Contratos(models.Model):

    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usuário Master')
    # dados principais
    num_cont = models.IntegerField('Cod. Contrato')
    company = models.ForeignKey('niluscad.Company', models.PROTECT, verbose_name='Empresa')
    data_contrato = models.DateField('Data Contrato',blank=True,null=True)
    vigencia = models.DateField('Vigência Contrato',blank=True,null=True)

    periodo_Choices = (
        ('M', 'Meses'),
        ('S', 'Semanal'),
        ('Q', 'Quinzenal'),
        ('A', 'Anual')
    )

    periodo_fat = models.CharField('Períodicidade de Faturamento', max_length=1,choices=periodo_Choices,default='M')

    modofat_Choices = (
        ('U', 'Valor Único na data Base'),
        ('S', 'Soma das ordens de serviço no período'),
        ('A', 'Avulso'),
    )

    modo_fat = models.CharField('Modo de Faturamento', max_length=1, choices=modofat_Choices, default='U')
    dia_base = models.PositiveIntegerField('Dia Base')

    prox_faturamento = models.DateField('Próximo Faturamento', blank=True, null=True)


    cadgeral = models.ForeignKey('niluscad.Cadgeral', models.PROTECT,verbose_name='Cliente')
    gera_nfs = models.BooleanField('Gera nota fiscal de serviços?',default=False)
    gera_boleto = models.BooleanField('Gera boleto bancário?',default=False)
    vinculo_os = models.BooleanField('Permite vínculo nas ordens de serviço?',default=False)
    valor = models.DecimalField('Valor', max_digits=13, decimal_places=2, null=True, blank=True)
    item = models.CharField(verbose_name='Item',max_length=40)
    valor_unit_text = models.CharField(verbose_name='Valor unitário', max_length=20)
    valor_unit = models.DecimalField('Valor', max_digits=13, decimal_places=2, null=True, blank=True)
    indice = models.ForeignKey('nilusfin.Indice', models.PROTECT, null=True, blank=True)
    cotacao = models.ForeignKey('nilusfin.Cotacao', models.PROTECT, null=True, blank=True)
    obs_contrato = models.TextField('Observações',blank=True)

    class Meta:
        verbose_name = 'Contratos'
        unique_together = [
            ('cadgeral', 'item')
        ]

    def __str__(self):
      return '%s - %s' % (str(self.num_cont), self.item)






class OrdemServico(models.Model):
    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usuário Master')
    num_os = models.PositiveIntegerField('Nº Ordem Serviço',)
    data_os = models.DateField('Data Contrato', blank=True, null=True)
    company = models.ForeignKey('niluscad.Company', models.PROTECT, verbose_name='Empresa')
    cadgeral = models.ForeignKey('niluscad.Cadgeral', models.PROTECT, verbose_name='Cliente')
    contrato = models.ForeignKey('niluscont.Contratos',models.PROTECT,verbose_name='Contrato',null=True,blank=True)
    desc_item = models.CharField(verbose_name='Item',max_length=40)
    valor_unit_text = models.CharField(verbose_name='Valor unitário', max_length=20)
    valor_unit = models.DecimalField('Valor', max_digits=13, decimal_places=2, null=True, blank=True)
    obs = models.TextField('Observações', blank=True)
    prestador = models.IntegerField('Cod. Prestador',null=True)

    situacao_Choices = (
        ('A', 'Ativo'),
        ('F', 'Faturada'),
    )

    situacao_fat = models.CharField('Situação de faturamento', max_length=1, choices=situacao_Choices, default='A')

    os_avulsa = models.BooleanField('OS Avulsa', default=False)

    class Meta:
        verbose_name = 'Ordens de Serviço'


    def __str__(self):
      return str(self.desc_item)



