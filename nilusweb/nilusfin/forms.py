from accounts.models import User
from django import forms
from .models import Cotacao,Indice,Contafinanceira
from niluscad.models import Company
from lancfinanceiros.models import Movtos_lancamentos


class FormCreateCotacao(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormCreateCotacao,self).__init__(*args,**kwargs)
        if user.is_masteruser:
            self.fields['indice'].queryset=Indice.objects.filter(master_user=user)
            self.fields['indice'].empty_label = 'Selecione um indice'
        else:
            self.fields['indice'].queryset = Indice.objects.filter(
                master_user=user.user_master
            )
            self.fields['indice'].empty_label = 'Selecione um indice'


    class Meta:
            model = Cotacao
            fields = ['indice','data_indice','valor_cotacao_text']




class FormAjusteSaldo(forms.ModelForm):
    vlr_novosaldo = forms.CharField(max_length=20)
    saldo_negativo = forms.BooleanField(label='Saldo Negativo', required=False)


    def __init__(self, user, *args, **kwargs):
        super(FormAjusteSaldo, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['conta_financeira'].queryset = Contafinanceira.objects.filter(master_user=user)
            self.fields['company'].queryset = Company.objects.filter(master_user=user)

        else:
            self.fields['conta_financeira'].queryset = Contafinanceira.objects.filter(master_user=user.user_master)
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)



        self.fields['conta_financeira'].empty_label = 'Selecione uma conta'
        self.fields['company'].empty_label = 'Selecione uma empresa'

    class Meta:
        model = Movtos_lancamentos
        fields = ['conta_financeira','dt_movimento','company']



class FiltroLancamentosExtrato(forms.Form):
    data_lanc_ini = forms.DateField(label='Lançamento de:', required=True)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=True)
    empresa = forms.ModelChoiceField(label='Empresa',empty_label='Todas',required=False,queryset=Company.objects.none())
    conta_finan = forms.ModelChoiceField(label='Conta Financeira',empty_label='Todas',required=False,queryset=Contafinanceira.objects.none())

    def __init__(self, conta_finan,empresa, *args, **kwargs):
        super(FiltroLancamentosExtrato, self).__init__(*args, **kwargs)
        self.fields['conta_finan'].queryset = conta_finan
        self.fields['empresa'].queryset=empresa



class FiltroDre(forms.Form):
    data_lanc_ini = forms.DateField(label='Lançamento de:', required=True)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=True)
    empresa = forms.ModelChoiceField(label='Empresa',empty_label='Todas',required=False,queryset=Company.objects.none())


    f_lancamento = parcela = forms.BooleanField(label='Data Lançamento', required=False)
    f_vencimento = forms.BooleanField(label='Data Vencimento', required=False)
    f_baixa = forms.BooleanField(label='Data Baixa', required=False)

    def __init__(self,empresa, *args, **kwargs):
        super(FiltroDre, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset= empresa


class FormFluxoCaixa(forms.Form):
    data_venc_ini = forms.DateField(label='Vencimento de:', required=True)
    data_venc_fim = forms.DateField(label='Vencimento até:', required=True)
    empresa = forms.ModelChoiceField(label='Empresa', empty_label='Todas', required=False,
                                     queryset=Company.objects.none())
    contas_financeiras = forms.ModelMultipleChoiceField(queryset=Contafinanceira.objects.none())
    considera_atraso = forms.BooleanField(label='Considera Atrasados',required=False)

    def __init__(self,empresa,contas,*args, **kwargs):
        super(FormFluxoCaixa, self).__init__(*args, **kwargs)
        self.fields['contas_financeiras'].queryset = contas
        self.fields['empresa'].queryset = empresa

