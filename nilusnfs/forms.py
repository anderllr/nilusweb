from django import forms
from niluscad.models import Company,Cadgeral
from nilusnfs.models import Paramnfs,TmpFat
from niluscad.models import PlanoFinan
from nilusfin.models import Contafinanceira


class FormCreateParamnfs(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(FormCreateParamnfs, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
        self.fields['company'].empty_label = 'Selecione uma empresa'
        self.fields['regime_trib'].empty_label = 'Informe o regime'

    class Meta:
        model = Paramnfs

        fields = ['company','cd_srv_padrao','desc_srv', 'aliquota_iss','cnae','it_lista_srv', 'simples_nac', 'incent_cult','regime_trib',
                  'certificado_pfx','certificado_nome','certificado_senha','conf_sequenciaNFE','conf_serieNFE',
                  'conf_sequencialoteNFe','conf_usuarioAcesso','conf_senhaUsuarioAcesso']




class FiltroBuscaFaturamento(forms.Form):


    prox_fat_ini = forms.DateField(label='Ultimo Faturamento de:', required=False)
    prox_fat_fim = forms.DateField(label='Ultimo Faturamento até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor', empty_label='Todos', required=False,
                                      queryset=Cadgeral.objects.none())

    lista_os = forms.BooleanField(label='listar O.S', required=False)

    def __init__(self, empresa, cliente, *args, **kwargs):
        super(FiltroBuscaFaturamento, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cliente






class FormFaturamento(forms.Form):

    ids_fat = forms.ModelMultipleChoiceField(queryset=TmpFat.objects.none())
    data_fat = forms.DateField(required=False)

    plano_financeiro = forms.ModelChoiceField(label="Plano Financeiro", empty_label='Escolha o plano', required=True,
                                              queryset=PlanoFinan.objects.none())

    conta_financeira = forms.ModelChoiceField(label="Conta Recebimento", empty_label='Escolha a conta', required=True,
                                              queryset=Contafinanceira.objects.none())

    fatura_unificado = forms.BooleanField(label='Faturamento Agrupado',required=False)


    def __init__(self,lista_fat,planofinan,contafinan,*args, **kwargs):
        super(FormFaturamento, self).__init__(*args, **kwargs)
        self.fields['ids_fat'].queryset = lista_fat
        self.fields['plano_financeiro'].queryset = planofinan
        self.fields['conta_financeira'].queryset = contafinan





class FiltroBuscaNotas(forms.Form):


    dt_emissao_ini = forms.DateField(label='Emissão de:', required=False)
    dt_emissao_fim = forms.DateField(label='Emissão até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa', required=False, empty_label='Todas',
                                     queryset=Company.objects.none())
    cadgeral = forms.ModelChoiceField(label='Cliente / Fornecedor', empty_label='Todos', required=False,
                                      queryset=Cadgeral.objects.none())


    def __init__(self, empresa, cliente, *args, **kwargs):
        super(FiltroBuscaNotas, self).__init__(*args, **kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['cadgeral'].queryset = cliente
