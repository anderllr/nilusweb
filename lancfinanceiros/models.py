from django.db import models

# Create your models here.


class Lancamentos(models.Model):
    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usuario Master')

    # dados principais (empresa e numero do lançamento)
    num_lan = models.IntegerField('Nº Registro')
    parcela = models.IntegerField('Parcela',default=1)
    company = models.ForeignKey('niluscad.Company',models.CASCADE,verbose_name='Empresa')


    #dados do titulo
    cadgeral = models.ForeignKey('niluscad.CadGeral',verbose_name='Cliente',blank=True,null=True)
    dt_lancamento = models.DateTimeField('Data Lançamento',auto_now_add=True)
    dt_vencimento = models.DateField('Data Vencimento',null=True,blank=True)
    plr_financeiro = models.ForeignKey('niluscad.Planofinan',verbose_name='Plano Financeiro')
    conta_finan = models.ForeignKey('nilusfin.Contafinanceira',verbose_name='Conta Recebimento')
    c_custo = models.ForeignKey('niluscad.Ccusto',verbose_name='Centro de Custo')
    vlr_lancamento = models.DecimalField('Valor do Lançamento',max_digits=13,decimal_places=2,blank=True,null=True)
    valor_text = models.CharField(verbose_name='Valor',  max_length=20)
    valor_original = models.DecimalField('Saldo', max_digits=13,decimal_places=2,blank=True,null=True)
    descricao = models.CharField(verbose_name='Observação', max_length=70,null=True)
    titulo = models.BooleanField('É Titulo', default=False)

    #Dados Cotação/Indice
    indice = models.ForeignKey('nilusfin.Indice',null=True,blank=True)
    cotacao = models.ForeignKey('nilusfin.Cotacao',null=True,blank=True)



    situacao = models.BooleanField('Baixado',default=False)
    data_baixa = models.DateTimeField('Data de Recebimento',null=True,blank=True)
    lancamento_pai = models.ForeignKey('self',models.SET_NULL,blank=True,null=True,verbose_name='Lançamento Pai')

    # Dados Baixa e Situação
    tipoLancto_Choices = (
        ('R', 'Recebimento'),
        ('P', 'Pagamento'),
    )

    tipo_lancamento = models.CharField('Tipo', max_length=1, choices=tipoLancto_Choices)


    def verifica_parcela(self):
        if self.lancamento_pai:
            return True
        return Lancamentos.objects.filter(lancamento_pai=self).exists()


    def altera_parcelas(self):
        if self.lancamento_pai:
            parcelas = Lancamentos.objects.filter(
                models.Q(lancamento_pai=self.lancamento_pai) | models.Q(pk=self.lancamento_pai.pk)
            )
            parcelas.update(
                plr_financeiro=self.plr_financeiro,c_custo=self.c_custo,valor_text=self.valor_text,
                vlr_lancamento = self.vlr_lancamento,indice=self.indice,cotacao=self.cotacao,
                descricao=self.descricao,valor_original=self.valor_original
            )
        else:
            parcelas = Lancamentos.objects.filter(lancamento_pai = self)
            parcelas.update(
                plr_financeiro=self.plr_financeiro, c_custo=self.c_custo,valor_text=self.valor_text,
                vlr_lancamento=self.vlr_lancamento, indice=self.indice, cotacao=self.cotacao,
                descricao=self.descricao,valor_original=self.valor_original
            )

    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        unique_together = [
            ('master_user', 'num_lan','parcela')
        ]

    def __str__(self):
        return self.valor_text
