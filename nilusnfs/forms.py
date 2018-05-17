from django import forms
from niluscad.models import Company,Cadgeral
from nilusnfs.models import Paramnfs
from niluscont.models import Contratos,OrdemServico


class FormCreateParamnfs(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(FormCreateParamnfs, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['regime_trib'].empty_label = 'Informe o regime'

    class Meta:
        model = Paramnfs

        fields = ['company','cd_srv_padrao','desc_srv', 'aliquota_iss','cnae','it_lista_srv', 'simples_nac', 'incent_cult','regime_trib',
                  'certificado_pfx','certificado_nome','certificado_senha']




class FiltroBuscaFaturamento(forms.Form):

    # data_emissao_ini = forms.DateField(label='Data Contrato/OS de:',required=False)
    # data_emissao_fim = forms.DateField(label='Data Contrato/OS de:', required=False)

    prox_fat_ini = forms.DateField(label='Ultimo Faturamento de:', required=False)
    prox_fat_fim = forms.DateField(label='Ultimo Faturamento até:', required=False)

    # dt_vigencia_ini = forms.DateField(label='Vigência de:', required=False)
    # dt_vigencia_fim = forms.DateField(label='Vigência até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor', empty_label='Todos', required=False,
                                      queryset=Cadgeral.objects.none())

    # contratos = forms.ModelChoiceField(label='Contratos', empty_label='Todos', required=False,
    #                                   queryset=Contratos.objects.none())

    lista_os = forms.BooleanField(label='listar O.S', required=False)

    def __init__(self, empresa, cliente, *args, **kwargs):
        super(FiltroBuscaFaturamento, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cliente
        # self.fields['contratos'].queryset = contratos


class FormFaturamento(forms.Form):

    lanc_fat = forms.ModelMultipleChoiceField(queryset=Contratos.objects.none())
    data_fat = forms.DateField(required=True)
    fat_unificado = forms.BooleanField(label='Faturar na mesma nota?', required=False)

    def __init__(self,*args, **kwargs):
        super(FormFaturamento, self).__init__(*args, **kwargs)
        # self.fields['lanc_baixa'].queryset = contratos


