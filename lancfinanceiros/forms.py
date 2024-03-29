from accounts.models import User
from datetime import date, timedelta, datetime
from niluscad.models import Company, Propriety, Cadgeral, Ccusto, PlanoFinan, Cadgeral
from django import forms
from nilusfin.models import Contafinanceira, Cotacao, Indice
from pip._vendor.packaging import requirements

from .models import Lancamentos


class FormCreateReceita(forms.ModelForm):
    parcela = forms.BooleanField(label='Parcelar', required=False)
    repetir = forms.BooleanField(label='repetir',required=False)
    # ja_baixado = forms.BooleanField(label='Já recebido', required=False)
    # data_liquidacao = forms.DateField(label='Data Baixa', required=False)

    qtd = forms.IntegerField(label='Quantidade', required=False)
    qtd_repetir = forms.IntegerField(label='Qtd Repetir',required=False)

    dias_entre_vencto = forms.IntegerField(label='Dias entre vencimentos',required=False)
    dia_fixo = forms.BooleanField(label='Dias entre vencimentos', required=False)
    # primeiro_vencto = forms.DateField(label='Primeiro vencimento', required=False)

    tipo_rept = forms.ChoiceField(label='Período', choices=(
        ('M', 'Mês'), ('S', 'Semana'), ('D', 'Dia'), ('Q', 'Quinzena')))

    def clean_qtd_rep(self):
        repetir = self.cleaned_data.get('repetir',False)
        qtd_rep = self.cleaned_data.get('qtd_repetir',None)
        if repetir and not qtd_rep :
            raise forms.ValidationError('Preencha a Quantidade de vezes que deve repetir')
        return qtd_rep


    def clean_dt_vencimento_rep(self):
        repetir = self.cleaned_data.get('repetir', False)
        dt_vencimento = self.cleaned_data.get('dt_vencimento', None)
        if repetir and not dt_vencimento:
            raise forms.ValidationError('Preencha o vencimento inicial')
        return dt_vencimento

    def __init__(self, user, *args, **kwargs):
        super(FormCreateReceita, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_recebimento=True)
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                 conta_recebimento=True)
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        self.fields['plr_financeiro'].empty_label = 'Selecione um plano'
        self.fields['c_custo'].empty_label = 'Selecione um centro de custo'
        self.fields['conta_finan'].empty_label = 'Selecione uma conta'
        self.fields['indice'].empty_label = 'Real'
        self.fields['cotacao'].empty_label = '1,0000'

    class Meta:
        model = Lancamentos
        fields = ['company','dt_vencimento','dt_lancamento', 'plr_financeiro', 'c_custo', 'conta_finan','descricao','valor_text','titulo','cadgeral','indice','cotacao','situacao']


class FormEditReceita(forms.ModelForm):
    altera_parcelas = forms.ChoiceField(label='Altera',required=False, choices=(
        ('N', 'Somente Este'), ('P', 'Pendentes'), ('T', 'Todos')),widget=forms.RadioSelect,initial='N')


    def __init__(self, user, *args, **kwargs):
        super(FormEditReceita, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='R')
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, cliente=True)
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_recebimento=True)

        else:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, cliente=True)
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                 conta_recebimento=True)

        self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        self.fields['plr_financeiro'].empty_label = 'Selecione um plano'
        self.fields['c_custo'].empty_label = 'Selecione um centro de custo'
        self.fields['conta_finan'].empty_label = 'Selecione uma conta'


    class Meta:
        model = Lancamentos
        fields = ['dt_vencimento','dt_lancamento','cadgeral', 'plr_financeiro', 'c_custo', 'conta_finan', 'valor_text',
                  'indice','cotacao','descricao','situacao']



class FormCreateDespesa(forms.ModelForm):
    parcela = forms.BooleanField(label='Parcelar', required=False)
    repetir = forms.BooleanField(label='repetir',required=False)
    # ja_baixado = forms.BooleanField(label='Já recebido', required=False)
    # data_liquidacao = forms.DateField(label='Data Baixa', required=False)

    qtd = forms.IntegerField(label='Quantidade', required=False)
    qtd_repetir = forms.IntegerField(label='Qtd Repetir',required=False)

    dias_entre_vencto = forms.IntegerField(label='Dias entre vencimentos',required=False)
    dia_fixo = forms.BooleanField(label='Dias entre vencimentos', required=False)
    # primeiro_vencto = forms.DateField(label='Primeiro vencimento', required=False)

    tipo_rept = forms.ChoiceField(label='Período', choices=(
        ('M', 'Mês'), ('S', 'Semana'), ('D', 'Dia'), ('Q', 'Quinzena')))

    def clean_qtd_rep(self):
        repetir = self.cleaned_data.get('repetir',False)
        qtd_rep = self.cleaned_data.get('qtd_repetir',None)
        if repetir and not qtd_rep :
            raise forms.ValidationError('Preencha a Quantidade de vezes que deve repetir')
        return qtd_rep


    def clean_dt_vencimento_rep(self):
        repetir = self.cleaned_data.get('repetir', False)
        dt_vencimento = self.cleaned_data.get('dt_vencimento', None)
        if repetir and not dt_vencimento:
            raise forms.ValidationError('Preencha o vencimento inicial')
        return dt_vencimento

    def __init__(self, user, *args, **kwargs):
        super(FormCreateDespesa, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, fornecedor=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='D')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_pagamento=True)
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, fornecedor=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='D')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                 conta_pagamento=True)
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        self.fields['plr_financeiro'].empty_label = 'Selecione um plano'
        self.fields['c_custo'].empty_label = 'Selecione um centro de custo'
        self.fields['conta_finan'].empty_label = 'Selecione uma conta'
        self.fields['indice'].empty_label = 'Real'
        self.fields['cotacao'].empty_label = '1,0000'


    class Meta:
        model = Lancamentos
        fields = ['company','dt_lancamento','dt_vencimento', 'plr_financeiro', 'c_custo', 'conta_finan','descricao','valor_text','titulo','cadgeral','indice','cotacao','situacao']





class FormEditDespesa(forms.ModelForm):
    altera_parcelas = forms.ChoiceField(label='Altera',required=False, choices=(
        ('N', 'Somente Este'), ('A', 'Ativos'), ('T', 'Todos')),widget=forms.RadioSelect,initial='N')



    def __init__(self, user, *args, **kwargs):
        super(FormEditDespesa, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='D')
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, fornecedor=True)
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_pagamento=True)
        else:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='D')
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, fornecedor=True)
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                                   conta_pagamento=True)
        self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        self.fields['plr_financeiro'].empty_label = 'Selecione um plano'
        self.fields['c_custo'].empty_label = 'Selecione um centro de custo'
        self.fields['conta_finan'].empty_label = 'Selecione uma conta'

    class Meta:
        model = Lancamentos
        fields = ['dt_vencimento','dt_lancamento','cadgeral', 'plr_financeiro', 'c_custo', 'conta_finan', 'valor_text',
                  'indice','cotacao','descricao','situacao']






class FiltroLancamentosForm(forms.Form):
    data_venc_ini = forms.DateField(label='Vencimento de:', required=False)
    data_venc_fim = forms.DateField(label='Vencimento até:', required=False)

    data_lanc_ini = forms.DateField(label='Lançamento de:', required=False)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=False)

    data_baix_ini = forms.DateField(label='Baixa de:', required=False)
    data_baix_fim = forms.DateField(label='Baixa até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor',empty_label='Todos', required=False, queryset=Cadgeral.objects.none())
    plano_finan = forms.ModelChoiceField(label='Plano Financeiro',empty_label='Todos' , required=False, queryset=PlanoFinan.objects.none())
    c_custo = forms.ModelChoiceField(label='Centro de Custo', empty_label='Todos', required=False, queryset=Ccusto.objects.none())
    conta_finan = forms.ModelChoiceField(label='Conta Financeira',empty_label='Todas',required=False,queryset=Ccusto.objects.none())

    tipoLancto_Choices = (
        ('T', 'Todos'),
        ('R', 'Receita'),
        ('D', 'Despesa'),
    )
    tipo_lancamento = forms.ChoiceField(label='Tipo lançamento', choices=tipoLancto_Choices, initial='T')

    situalancamento = (
        ('T', 'Todos'),
        ('A', 'Abertos'),
        ('B', 'Baixados'),
    )
    sit_lancamento = forms.ChoiceField(label='Situação', choices=situalancamento, initial='T')



    def __init__(self, empresa,cliente,plano_finan,c_custo,conta_finan, *args, **kwargs):
        super(FiltroLancamentosForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cliente
        self.fields['plano_finan'].queryset = plano_finan
        self.fields['c_custo'].queryset = c_custo
        self.fields['conta_finan'].queryset = conta_finan


class FiltroLancamentosbaixa(forms.Form):
    data_venc_ini = forms.DateField(label='Vencimento de:', required=False)
    data_venc_fim = forms.DateField(label='Vencimento até:', required=False)

    data_lanc_ini = forms.DateField(label='Lançamento de:', required=False)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=False)

    data_baix_ini = forms.DateField(label='Baixa de:', required=False)
    data_baix_fim = forms.DateField(label='Baixa até:', required=False)

    tipoLancto_Choices = (
        ('T', 'Todos'),
        ('R', 'Receita'),
        ('D', 'Despesa'),
    )

    tipo_lancamento = forms.ChoiceField(label='Tipo lançamento', choices=tipoLancto_Choices,initial='T')

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor',empty_label='Todos', required=False, queryset=Cadgeral.objects.none())
    plano_finan = forms.ModelChoiceField(label='Plano Financeiro',empty_label='Todos' , required=False, queryset=PlanoFinan.objects.none())
    c_custo = forms.ModelChoiceField(label='Centro de Custo', empty_label='Todos', required=False, queryset=Ccusto.objects.none())
    conta_finan = forms.ModelChoiceField(label='Conta Financeira',empty_label='Todas',required=False,queryset=Contafinanceira.objects.none())


    def __init__(self, empresa, cliente, plano_finan, c_custo, conta_finan, *args, **kwargs):
        super(FiltroLancamentosbaixa, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cliente
        self.fields['plano_finan'].queryset = plano_finan
        self.fields['c_custo'].queryset = c_custo
        self.fields['conta_finan'].queryset = conta_finan






class FormBaixaLancamento(forms.Form):

    lanc_baixa = forms.ModelMultipleChoiceField(queryset=Lancamentos.objects.none())
    data_baixa = forms.DateField(required=True)
    conta_financeira = forms.ModelChoiceField(label="Conta Financeira",empty_label='Escolha a Conta',required=False,queryset=Contafinanceira.objects.none())


    def __init__(self,lanctos,conta_finan,*args, **kwargs):
        super(FormBaixaLancamento, self).__init__(*args, **kwargs)
        self.fields['lanc_baixa'].queryset = lanctos
        self.fields['conta_financeira'].queryset = conta_finan







class FormBaixaParcial(forms.ModelForm):
    valor_baixar = forms.CharField(max_length=20)
    baixa_total = forms.BooleanField(label='Baixar Total',required=False)


    def __init__(self, user, *args, **kwargs):
        super(FormBaixaParcial, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            # self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='D')
            # self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, fornecedor=True)
            # self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            # self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_pagamento=True)
        else:
            # self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='D')
            # self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, fornecedor=True)
            # self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            # self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                                   conta_pagamento=True)
        # self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        # self.fields['plr_financeiro'].empty_label = 'Selecione um plano'
        # self.fields['c_custo'].empty_label = 'Selecione um centro de custo'
        self.fields['conta_finan'].empty_label = 'Selecione uma conta'

    class Meta:
        model = Lancamentos
        fields = ['conta_finan','data_baixa']



class FormDeletaLancto(forms.ModelForm):
    delete_parcelas = forms.ChoiceField(label='Altera',required=False, choices=(
        ('N', 'Somente Este'), ('A', 'Ativos'), ('T', 'Todos')),widget=forms.RadioSelect,initial='N')
