from accounts.models import User
from niluscad.models import Company, Propriety, Cadgeral, Ccusto, PlanoFinan, Cadgeral
from django import forms
from nilusfin.models import Contafinanceira, Cotacao, Indice
from .models import Lancamentos


class FormCreateReceita(forms.ModelForm):
    # parcela = forms.BooleanField(label='Parcelar', required=False)
    ja_baixado = forms.BooleanField(label='Já recebido', required=False)
    data_liquidacao = forms.DateField(label='Data Baixa', required=False)
    qtd = forms.IntegerField(label='Quantidade', required=False)
    dias_entre_vencto = forms.IntegerField(label='Dias entre vencimentos',required=False)
    primeiro_vencto = forms.DateField(label='Primeiro vencimento', required=False)

    # tipo_rept = forms.ChoiceField(label='Período', choices=(
    #     ('M', 'Mês'), ('S', 'Semana'), ('D', 'Dia'), ('Q', 'Quinzena')))

    def clean_qtd(self):
        # parcela = self.cleaned_data.get('parcela', False)
        qtd = self.cleaned_data.get('qtd', None)
        if not qtd:
            raise forms.ValidationError('Preencher a quantidade de parcelas do titulo')
        return qtd

    def __init__(self, user, *args, **kwargs):
        super(FormCreateReceita, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
            self.fields['propriety'].queryset = Propriety.objects.filter(master_user=user)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user, cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_recebimento=True)
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
            self.fields['propriety'].queryset = Propriety.objects.filter(master_user=user.user_master)
            self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                 conta_recebimento=True)

    class Meta:
        model = Lancamentos
        fields = ['company', 'propriety', 'cadgeral', 'dt_vencimento', 'plr_financeiro', 'c_custo', 'conta_finan',
                  'valor_text',
                  'indice', 'cotacao']


class FormEditReceita(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(FormEditReceita, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user,
                                                                                 conta_recebimento=True)
        else:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user.user_master)
            self.fields['conta_finan'].queryset = Contafinanceira.objects.filter(master_user=user.user_master,
                                                                                 conta_recebimento=True)

    class Meta:
        model = Lancamentos
        fields = ['dt_vencimento', 'plr_financeiro', 'c_custo', 'conta_finan', 'valor_text',
                  'indice', 'cotacao']


class FiltroLancamentosForm(forms.Form):
    data_venc_ini = forms.DateField(label='Vencimento de:', required=False)
    data_venc_fim = forms.DateField(label='Vencimento até:', required=False)

    data_lanc_ini = forms.DateField(label='Lançamento de:', required=False)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=False)
    sit_tit = forms.ChoiceField(label='Situacao', choices=(
         ('A', 'Ativo'), ('B', 'Baixado'), ('C', 'Cancelado')))


    empresa = forms.ModelChoiceField(label='Empresa', required=False,empty_label = 'Todas', queryset=Company.objects.none())
    propriedade = forms.ModelChoiceField(label='Propriedade', required=False, empty_label='Todas', queryset=Propriety.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor', required=False, empty_label='Todos', queryset=Cadgeral.objects.none())
    plano_finan = forms.ModelChoiceField(label='Plano Financeiro', required=False, empty_label='Todos', queryset=PlanoFinan.objects.none())
    c_custo = forms.ModelChoiceField(label='Centro de Custo', required=False, empty_label='Todos' ,queryset=Ccusto.objects.none())

    def __init__(self, empresa, propriedade, cliente, plano_finan, c_custo,situacao, *args, **kwargs):
        super(FiltroLancamentosForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['propriedade'].queryset = propriedade
        self.fields['cadgeral'].queryset = cliente
        self.fields['plano_finan'].queryset = plano_finan
        self.fields['c_custo'].queryset = c_custo
        self.fields['situcaco'] = situacao



