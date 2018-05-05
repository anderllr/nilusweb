from django.db import models

# Create your models here.



class Paramnfs(models.Model):

    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usario Master')
    # dados principais
    num_param = models.IntegerField('Cod. Empresa')
    company = models.ForeignKey('niluscad.Company', models.PROTECT, verbose_name='Empresa')
    cd_srv_padrao = models.CharField('Cod. Serviço Padrão',max_length=20)
    desc_srv = models.CharField('Descrição do Serviço', max_length=60)
    aliquota_iss = models.DecimalField('Aliquota',max_digits=13,decimal_places=2)
    cnae = models.CharField('CNAE', max_length=20)
    it_lista_srv = models.CharField('Item da lista de serviço',max_length=20)
    simples_nac = models.BooleanField('Optante Simples Nacional', default=False)
    incent_cult = models.BooleanField('Incentivador Cultural', default=False)

    regime_Choices = (
        (None, 'Informe o regime'),
        ('M', 'Microempresa Municipal'),
        ('E', 'Estimativa'),
        ('S', 'Sociedade de Profissionais'),
        ('C', 'Cooperativa'),

    )

    regime_trib = models.CharField('Regime especial de tributação', max_length=1, choices=regime_Choices)
    certificado_pfx = models.FileField('Certificado',upload_to='images',blank=True)
    certificado_nome = models.CharField('Nome Certificado',max_length=50,blank=True)
    certificado_senha = models.CharField('Nome Certificado',max_length=50)



    class Meta:
        verbose_name = 'Parametros NFS'
        unique_together = [
            ('master_user', 'company')
        ]

    def __str__(self):
      return self.desc_srv

