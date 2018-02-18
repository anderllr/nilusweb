from django.db import models


# Create your models here.




class Permissions(models.Model):

    user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usuário')
    nilusCadastro = models.BooleanField('Cadastros', default=False)
    nilusFinanceiro = models.BooleanField('Financeiro',default=False)
    nilusCompras = models.BooleanField('Compras',default=False)
    nilusProducao = models.BooleanField('Producao', default=False)
    nilusMaquinas = models.BooleanField('Máquinas', default=False)
    nilusFiscalCont = models.BooleanField('Fiscal e Contábil', default=False)


class Meta:
    verbose_name = 'Permissão'
    verbose_name_pural = 'Permissões'



    def __str__(self):
        return self.user



class Sequenciais(models.Model):

    user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usuário')
    empresas = models.IntegerField('Seq Cad. Empresas', default=0)
    propriedades = models.IntegerField('Seq Cad. Propriedades',default=0)
    cadgeral = models.IntegerField('Seq Cad. CadGeral',default=0)
    ccusto = models.IntegerField('Seq Cad. Ccusto', default=0)
    planofinan = models.IntegerField('Seq PlanoFinan', default=0)
    conta = models.IntegerField('Seq Conta', default=0)
    indice = models.IntegerField('Seq Indice', default=0)
    recebiveis = models.IntegerField('Seq Tit. Receber', default=0)
    lanc_financeiros = models.IntegerField('Seq Lancamento Financeiro', default=0)



class Meta:
    verbose_name = 'Sequenciais'
    verbose_name_pural = 'Sequenciais'



    def __str__(self):
        return self.user


