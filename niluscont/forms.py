from django import forms
from .models import Contratos
from niluscad.models import Company, Propriety, Cadgeral, Ccusto, PlanoFinan, Cadgeral
from nilusfin.models import Contafinanceira, Cotacao, Indice


class FormContrato(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormContrato,self).__init__(*args,**kwargs)
        self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
        self.fields['cadgeral'].queryset = Cadgeral.objects.filter(master_user=user.user_master, cliente=True)
        self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
        self.fields['modo_fat'].widget = forms.RadioSelect(
            choices=self.fields['modo_fat'].widget.choices)

        self.fields['indice'].empty_label = 'Escolha o índice'
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['cadgeral'].empty_label = 'Selecione um cadastro'
        self.fields['cotacao'].empty_label = '1,0000'


    class Meta:
        model = Contratos
        fields = ['company','data_contrato','vigencia','periodo_fat','modo_fat','cadgeral','gera_nfs','gera_boleto',
                  'vinculo_os','item','valor_unit_text','indice','cotacao','obs_contrato','dia_base']



class FiltroContratosForm(forms.Form):
    data_contrato_ini = forms.DateField(label='Vencimento de:', required=False)
    data_contrato_fim = forms.DateField(label='Vencimento até:', required=False)

    data_vigencia_ini = forms.DateField(label='Lançamento de:', required=False)
    data_vigencia_fim = forms.DateField(label='Lançamento até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor', empty_label='Todos', required=False,
                                      queryset=Cadgeral.objects.none())

    indice = forms.ModelChoiceField(label='Índice', required=False, empty_label='Todos',
                                     queryset=Indice.objects.none())

    def __init__(self,empresa,cadgeral,indice,*args,**kwargs):
        super(FiltroContratosForm,self).__init__(*args,**kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cadgeral
        self.fields['indice'].queryset = indice

