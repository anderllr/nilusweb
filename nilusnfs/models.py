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
        ('0', 'Normal'),
        ('1', 'Isenta'),
        ('2', 'Imune'),
        ('3', 'Suspenso/decisão judicial'),
    )


    regime_trib = models.CharField('Regime especial de tributação', max_length=1, choices=regime_Choices)
    certificado_pfx = models.FileField('Certificado',upload_to='images',blank=True)
    certificado_nome = models.CharField('Nome Certificado',max_length=50,blank=True)
    certificado_senha = models.CharField('Nome Certificado',max_length=50)

    key_empresa = models.CharField('Key Enotas', max_length=100,blank=True)
    habilitada_faturamento = models.BooleanField('Pendencias Cadastrais',default=False)

    conf_sequenciaNFE = models.PositiveIntegerField('Sequencia NFS-e',default=1)
    conf_serieNFE = models.CharField('Serie NFS-e',max_length=4,default='1')
    conf_sequencialoteNFe = models.PositiveIntegerField('Sequencia Lote NFe',default=1)

    conf_usuarioAcesso = models.CharField('Usuário site prefeitura',max_length=30)
    conf_senhaUsuarioAcesso = models.CharField('Senha site prefeitura',max_length=30)

    conf_enviaEmail = models.BooleanField('Envia email',default=True)



    class Meta:
        verbose_name = 'Parametros NFS'
        unique_together = [
            ('master_user', 'company'), ('master_user', 'num_param')
        ]


    def __str__(self):
      return self.desc_srv



class TmpFat(models.Model):
    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usario Master')
    company = models.ForeignKey('niluscad.Company',models.CASCADE,verbose_name='Empresa')
    tipo = models.CharField('Tipo',max_length=10)
    cadgeral = models.ForeignKey('niluscad.Cadgeral',models.CASCADE,verbose_name='Cliente',null=True,blank=True)
    contrato = models.ForeignKey('niluscont.Contratos',models.CASCADE,verbose_name='Contrato',null=True,blank=True)
    os = models.ForeignKey('niluscont.OrdemServico',models.CASCADE,verbose_name='O.S',null=True,blank=True)
    vlr_fat = models.DecimalField(verbose_name='Valor Fatura',null=True,blank=True,decimal_places=2,max_digits=18)
    data_fat = models.DateField('Data Faturamento')
    situacao = models.BooleanField('Faturado',default=False)


    class Meta:
        verbose_name = 'PendenteFaturamento'

    def __str__(self):
        return 'Nº Contrato %s - Nº O.s %s' % (str(self.contrato), str(self.os))



class ErrosParametrosNFS(models.Model):
    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usario Master')
    paramnfs = models.ForeignKey('nilusnfs.Paramnfs',models.CASCADE, verbose_name='Parametro Empresa')
    mensagem = models.CharField('Mensagem Erro',max_length=100)

    class Meta:
        verbose_name = 'Erros Parametros NFS'

    def __str__(self):
        return str(self.paramnfs)




class NotasFiscais(models.Model):


    master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Usario Master')
    company = models.ForeignKey('niluscad.Company', models.CASCADE, verbose_name='Empresa')
    cadgeral = models.ForeignKey('niluscad.Cadgeral', models.CASCADE, verbose_name='Cliente', null=True, blank=True)

    num_nf = models.PositiveIntegerField('Nº Nota Fiscal',null=True,blank=True)
    data_emissao = models.DateTimeField('Emissão',null=True,blank=True)
    vlr_nota = models.DecimalField(verbose_name='Valor Nota',null=True,blank=True,decimal_places=2,max_digits=18)

    obs_nota = models.CharField('Observacoes',max_length=1000)

    id_key = models.CharField('Key Enotas',max_length=100)
    link_pdf = models.CharField('Link PDF',max_length=1000)
    link_xml = models.CharField('Link XML', max_length=1000)
    desc_status_nfs = models.CharField('Status NFS',max_length=100)
    motivoStatus = models.CharField('Motivo Status',max_length=300)

    id_origem = models.CharField('ID Externo',null=True,blank=True,max_length=60)


    tipoorigem_Choices = (
        ('O', 'OrdemServico'),
        ('C', 'Contrato')
    )
    tipo_origem = models.CharField('tipo_origem', max_length=1, null=True, blank=True, choices=tipoorigem_Choices)
    tipo = models.CharField('tipo registro', max_length=1,null=True,blank=True)
    envio_concluido = models.CharField('Envio Concluido', null=True, blank=True, max_length=2)

    class Meta:
        verbose_name = 'Notas Fiscais'

    def __str__(self):
        return 'Empresa %s - Nº Nota %s' % (str(self.cadgeral), str(self.num_nf))

