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
    dt_lancamento = models.DateField('Data Lançamento',auto_now_add=True)
    dt_vencimento = models.DateField('Data Vencimento',null=True,blank=True)
    plr_financeiro = models.ForeignKey('niluscad.Planofinan',verbose_name='Plano Financeiro')
    conta_finan = models.ForeignKey('nilusfin.Contafinanceira',verbose_name='Conta Recebimento')
    c_custo = models.ForeignKey('niluscad.Ccusto',verbose_name='Centro de Custo')
    vlr_lancamento = models.DecimalField('Valor do Lançamento',max_digits=13,decimal_places=2,blank=True,null=True)
    valor_text = models.CharField(verbose_name='Valor',  max_length=20)
    saldo = models.DecimalField('Saldo', max_digits=13,decimal_places=2,blank=True,null=True)
    descricao = models.CharField(verbose_name='Observação', max_length=70,null=True,blank=True)
    titulo = models.BooleanField('É Titulo', default=False)


    #Dados Cotação/Indice
    indice = models.ForeignKey('nilusfin.Indice',null=True,blank=True)
    cotacao = models.ForeignKey('nilusfin.Cotacao',null=True,blank=True)



    situacao = models.BooleanField('Baixado',default=False)
    reaberto = models.BooleanField('Reaberto',default=False)
    data_baixa = models.DateField('Data de Recebimento',null=True,blank=True)
    lancamento_pai = models.ForeignKey('self',models.SET_NULL,blank=True,null=True,verbose_name='Lançamento Pai')

    # Dados Baixa e Situação
    tipoLancto_Choices = (
        ('R', 'Receita'),
        ('D', 'Despesa'),
    )

    tipo_lancamento = models.CharField('Tipo', max_length=1, choices=tipoLancto_Choices)


    def verifica_parcela(self):
        if self.lancamento_pai:
            return True
        return Lancamentos.objects.filter(lancamento_pai=self).exists()


    def altera_parcelas(self,confirma_parcela,alterado):
        if confirma_parcela == 'T':
            if self.lancamento_pai:
                parcelas = Lancamentos.objects.filter(
                    models.Q(lancamento_pai=self.lancamento_pai) | models.Q(pk=self.lancamento_pai.pk)
                )
                for a in alterado:
                    if a == 'situacao':
                        situacao_new = a
                        parcelas.update(situacao=self.situacao)
                        if self.situacao == True:
                            parcelas.update(data_baixa=self.data_baixa)
                    else:
                        situacao_new = 'N'

                parcelas.update(
                    plr_financeiro=self.plr_financeiro,c_custo=self.c_custo,valor_text=self.valor_text,
                    vlr_lancamento = self.vlr_lancamento,indice=self.indice,cotacao=self.cotacao,
                    descricao=self.descricao,saldo=self.saldo,cadgeral=self.cadgeral

                )
                for p in parcelas:
                    movto_lanc = Movtos_lancamentos.objects.get(lancamento=p, tipo_movto='C')
                    movto_lanc.vlr_movimento = p.vlr_lancamento
                    movto_lanc.save()
                    if situacao_new == 'situacao':
                        if p.situacao == True:
                            movto_lanc_del = Movtos_lancamentos.objects.get(lancamento=p,tipo_movto='B')
                            movto_lanc_del.delete()

                            movto_lanc = Movtos_lancamentos()
                            movto_lanc.lancamento = p
                            movto_lanc.dt_movimento = p.dt_baixa
                            movto_lanc.vlr_movimento = p.saldo
                            if p.tipo_lancamento == 'R':
                                movto_lanc.desc_movimento = 'Recebido'
                            else:
                                movto_lanc.desc_movimento = 'Pago'
                            movto_lanc.tipo_movto = 'B'
                            movto_lanc.save()
            else:
                parcelas = Lancamentos.objects.filter(lancamento_pai = self)

                for a in alterado:
                    if a == 'situacao':
                        situacao_new = a
                        parcelas.update(situacao=self.situacao)
                        if self.situacao == True:
                            parcelas.update(data_baixa=self.data_baixa)
                    else:
                        situacao_new = 'N'


                parcelas.update(
                    plr_financeiro=self.plr_financeiro, c_custo=self.c_custo,valor_text=self.valor_text,
                    vlr_lancamento=self.vlr_lancamento, indice=self.indice, cotacao=self.cotacao,
                    descricao=self.descricao,saldo=self.saldo,cadgeral=self.cadgeral
                )
                for p in parcelas:
                    movto_lanc = Movtos_lancamentos.objects.get(lancamento=p, tipo_movto='C')
                    movto_lanc.vlr_movimento = p.vlr_lancamento
                    movto_lanc.save()
                    if situacao_new == 'situacao':
                        if p.situacao == True:
                            movto_lanc_del = Movtos_lancamentos.objects.filter(lancamento=p, tipo_movto='B')
                            movto_lanc_del.delete()

                            movto_lanc = Movtos_lancamentos()
                            movto_lanc.lancamento = p
                            movto_lanc.dt_movimento = p.data_baixa
                            movto_lanc.vlr_movimento = p.saldo
                            if p.tipo_lancamento == 'R':
                                movto_lanc.desc_movimento = 'Recebido'
                            else:
                                movto_lanc.desc_movimento = 'Pago'
                            movto_lanc.tipo_movto = 'B'
                            movto_lanc.save()
                        else:
                            movto_lanc_del = Movtos_lancamentos.objects.filter(lancamento=p, tipo_movto='B')
                            movto_lanc_del.delete()

        elif confirma_parcela == 'P':
            if self.lancamento_pai:
                parcelas = Lancamentos.objects.filter(
                    models.Q(lancamento_pai=self.lancamento_pai) | models.Q(pk=self.lancamento_pai.pk,situacao=False)
                )

                for a in alterado:
                    if a == 'situacao':
                        situacao_new = a
                        parcelas.update(situacao=self.situacao)
                        if self.situacao == True:
                            parcelas.update(data_baixa=self.data_baixa)
                    else:
                        situacao_new = 'N'

                parcelas.update(
                    plr_financeiro=self.plr_financeiro,c_custo=self.c_custo,valor_text=self.valor_text,
                    vlr_lancamento = self.vlr_lancamento,indice=self.indice,cotacao=self.cotacao,
                    descricao=self.descricao,saldo=self.saldo,cadgeral=self.cadgeral
                )
                for p in parcelas:
                    movto_lanc = Movtos_lancamentos.objects.get(lancamento=p, tipo_movto='C')
                    movto_lanc.vlr_movimento = p.vlr_lancamento
                    movto_lanc.save()
                    if situacao_new == 'situacao':
                        if p.situacao == True:
                            movto_lanc_del = Movtos_lancamentos.objects.get(lancamento=p,tipo_movto='B')
                            movto_lanc_del.delete()

                            movto_lanc = Movtos_lancamentos()
                            movto_lanc.lancamento = p
                            movto_lanc.dt_movimento = p.dt_baixa
                            movto_lanc.vlr_movimento = p.saldo
                            if p.tipo_lancamento == 'R':
                                movto_lanc.desc_movimento = 'Recebido'
                            else:
                                movto_lanc.desc_movimento = 'Pago'
                            movto_lanc.tipo_movto = 'B'
                            movto_lanc.save()
            else:
                parcelas = Lancamentos.objects.filter(situacao=False,lancamento_pai=self)

                for a in alterado:
                    if a == 'situacao':
                        situacao_new = a
                        parcelas.update(situacao=self.situacao)
                        if self.situacao == True:
                            parcelas.update(data_baixa=self.data_baixa)
                    else:
                        situacao_new = 'N'


                parcelas.update(
                    plr_financeiro=self.plr_financeiro, c_custo=self.c_custo,valor_text=self.valor_text,
                    vlr_lancamento=self.vlr_lancamento, indice=self.indice, cotacao=self.cotacao,
                    descricao=self.descricao,saldo=self.saldo,cadgeral=self.cadgeral
                )
                for p in parcelas:
                    movto_lanc = Movtos_lancamentos.objects.get(lancamento=p, tipo_movto='C')
                    movto_lanc.vlr_movimento = p.vlr_lancamento
                    movto_lanc.save()
                    if situacao_new == 'situacao':
                        if p.situacao == True:
                            movto_lanc_del = Movtos_lancamentos.objects.filter(lancamento=p, tipo_movto='B')
                            movto_lanc_del.delete()

                            movto_lanc = Movtos_lancamentos()
                            movto_lanc.lancamento = p
                            movto_lanc.dt_movimento = p.data_baixa
                            movto_lanc.vlr_movimento = p.saldo
                            if p.tipo_lancamento == 'R':
                                movto_lanc.desc_movimento = 'Recebido'
                            else:
                                movto_lanc.desc_movimento = 'Pago'
                            movto_lanc.tipo_movto = 'B'
                            movto_lanc.save()
                        else:
                            movto_lanc_del = Movtos_lancamentos.objects.filter(lancamento=p, tipo_movto='B')
                            movto_lanc_del.delete()




    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        unique_together = [
            ('master_user', 'num_lan','parcela')
        ]

    def __str__(self):
         return str(int((self.pk)))



class Movtos_lancamentos(models.Model):

    lancamento = models.ForeignKey('lancfinanceiros.Lancamentos',models.CASCADE,verbose_name='lancamento')
    dt_movimento = models.DateField('Data Movimento')
    vlr_movimento = models.DecimalField('Valor do Lançamento', max_digits=13, decimal_places=2, blank=True, null=True)
    conta_financeira = models.ForeignKey('nilusfin.Contafinanceira',verbose_name='Conta Financeira',blank=True,null=True)
    desc_movimento = models.CharField(verbose_name='Observação', max_length=70,null=True)


    tipoMovto_Choices = (
        ('C', 'Criação'),
        ('B', 'Baixa'),
        ('D', 'Desconto'),
        ('J', 'Juros'),
        ('M', 'Multa')
    )
    tipo_movto = models.CharField('Tipo', max_length=1, choices=tipoMovto_Choices)


    class Meta:
        verbose_name = 'Movimentos'
        verbose_name_plural = 'Movimentos'

    # def __str__(self):
    #     return self.desc_movimento


