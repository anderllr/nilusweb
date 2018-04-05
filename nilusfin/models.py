from django.db import models

# Create your models here.

class Contafinanceira(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usuario Master')
    num_conta = models.IntegerField('Código')

    # dados principais
    conta_bancaria = models.BooleanField('Conta Bancária?',default=False)
    agencia = models.CharField('Agencia',null=True,blank=True,max_length=5)
    conta = models.CharField('Conta',null=True,blank=True,max_length=12)
    descricao = models.CharField('Nome Conta',max_length=60)

    #dados de limite
    usa_limite = models.BooleanField('Utiliza Limite',default=False)
    vlr_limite = models.DecimalField('Valor Limite',decimal_places=2,max_digits=50,default=0)
    vlr_limite_text = models.CharField('Valor Limite',null=True,blank=True,max_length=50)

    #dados de movimentação
    conta_pagamento = models.BooleanField('Conta de Pagamento?',default=False)
    conta_recebimento = models.BooleanField('Conta de Recebimento?', default=False)



    class Meta:
        verbose_name = 'Contas'
        verbose_name_plural = 'Contas'
        unique_together = [
            ('master_user', 'num_conta')
        ]


    def __str__(self):
        return self.descricao



class Indice(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Uusario Master')
    num_indice = models.IntegerField('Código')

    # dados principais
    descricao = models.CharField('Nome Indice',max_length=20)
    simbolo = models.CharField('Simbolo', max_length=5)

    indice_padrao = models.BooleanField('Indice Padrao',default=False)


    class Meta:
        verbose_name = 'Indice'
        verbose_name_plural = 'Indices'
        unique_together = [
          ('master_user', 'num_indice')
        ]


    def __str__(self):
        return self.descricao



class Cotacao(models.Model):
    # informação do dono da conta (usuario Master)
    # master_user = models.ForeignKey('accounts.User', models.CASCADE, verbose_name='Uusario Master')
    indice = models.ForeignKey('nilusfin.Indice',models.PROTECT,verbose_name='Indice',null=True,blank=True)

    data_indice = models.DateField('Data',null=True,blank=True)
    valor_cotacao = models.DecimalField('Valor',null=True,blank=True,decimal_places=4,max_digits=13)
    user_cad = models.ForeignKey('accounts.User',models.SET_NULL, verbose_name='Usuario Criação',null=True,blank=True)

    cotacao_padrao = models.BooleanField('Cotação Padrão',default=False)

    class Meta:
        verbose_name = 'Cotacao'
        verbose_name_plural = 'Cotações'
        unique_together = [
            ('indice', 'data_indice')
        ]



    def __str__(self):
        return str(self.valor_cotacao)






