from accounts.models import User
from django import forms
from .models import Cotacao,Indice,Contafinanceira
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
            fields = ['indice','data_indice','valor_cotacao']




class FormAjusteSaldo(forms.ModelForm):
    vlr_novosaldo = forms.CharField(max_length=20)

    def __init__(self, user, *args, **kwargs):
        super(FormAjusteSaldo, self).__init__(*args, **kwargs)
        if user.is_masteruser is True:
            self.fields['conta_financeira'].queryset = Contafinanceira.objects.filter(master_user=user)
        else:
            self.fields['conta_financeira'].queryset = Contafinanceira.objects.filter(master_user=user.user_master)



        self.fields['conta_financeira'].empty_label = 'Selecione uma conta'

    class Meta:
        model = Movtos_lancamentos
        fields = ['conta_financeira','dt_movimento']



class FiltroLancamentosExtrato(forms.Form):
    data_lanc_ini = forms.DateField(label='Lançamento de:', required=True)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=True)
    conta_finan = forms.ModelChoiceField(label='Conta Financeira',empty_label='Todas',required=False,queryset=Contafinanceira.objects.none())

    def __init__(self, conta_finan, *args, **kwargs):
        super(FiltroLancamentosExtrato, self).__init__(*args, **kwargs)
        self.fields['conta_finan'].queryset = conta_finan


