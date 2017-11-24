from accounts.models import User
from niluscad.models import Company,Propriety,Cadgeral,Ccusto,PlanoFinan,Cadgeral
from django import forms
from nilusfin.models import Contafinanceira,Cotacao,Indice
from .models import Recebiveis



class FormCreateTitRec(forms.ModelForm):
    parcela = forms.BooleanField(label='Parcelar',required=False)
    qtd = forms.IntegerField(label='Quantidade',required=False)
    cc_custo_extra = forms.CharField



    tipo_rept = forms.ChoiceField(label='Período',choices=(
        ('M','Mês'),('S', 'Semana'),('D','Dia')))


    def clean_qtd(self):
        parcela = self.cleaned_data.get('parcela',False)
        qtd = self.cleaned_data.get('qtd',None)
        if parcela and not qtd:
            raise forms.ValidationError('Preencher a quantidade de parcelas do titulo')
        return qtd

    def __init__(self,user,*args,**kwargs):
        super(FormCreateTitRec,self).__init__(*args,**kwargs)
        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
            self.fields['propriety'].queryset = Propriety.objects.filter(master_user=user)
            self.fields['client'].queryset = Cadgeral.objects.filter(master_user=user,cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user,sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user)
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
            self.fields['propriety'].queryset = Propriety.objects.filter(master_user=user.user_master)
            self.fields['client'].queryset = Cadgeral.objects.filter(master_user=user.user_master, cliente=True)
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user.user_master)

    class Meta:
        model = Recebiveis
        fields = ['company','propriety','client','dt_vencimento','plr_financeiro','c_custo','valor_text',
                  'indice','cotacao']



class FormEditTitRec(forms.ModelForm):



    def __init__(self,user,*args,**kwargs):
        super(FormEditTitRec,self).__init__(*args,**kwargs)
        if user.is_masteruser is True:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user)
        else:
            self.fields['plr_financeiro'].queryset = PlanoFinan.objects.filter(master_user=user.user_master, sinal='R')
            self.fields['c_custo'].queryset = Ccusto.objects.filter(master_user=user.user_master)
            self.fields['indice'].queryset = Indice.objects.filter(master_user=user.user_master)
            self.fields['cotacao'].queryset = Cotacao.objects.filter(master_user=user.user_master)

    class Meta:
        model = Recebiveis
        fields = ['dt_vencimento','plr_financeiro','c_custo','valor_text',
                  'indice','cotacao']




class FiltroRecebimentosForm(forms.Form):

    data_venc_ini = forms.DateField(label='Vencimento de:', required=False)
    data_venc_fim = forms.DateField(label='Vencimento até:', required=False)

    data_lanc_ini = forms.DateField(label='Lançamento de:', required=False)
    data_lanc_fim = forms.DateField(label='Lançamento até:', required=False)

    empresa = forms.ModelChoiceField(label='Empresa',required=False,empty_label='Todos', queryset=Company.objects.none())
    propriedade = forms.ModelChoiceField(label='Propriedade', required=False, queryset=Propriety.objects.none())
    cliente = forms.ModelChoiceField(label='Cliente', required=False, queryset=Cadgeral.objects.none())
    plano_finan = forms.ModelChoiceField(label='Plano Financeiro', required=False, queryset=PlanoFinan.objects.none())
    c_custo = forms.ModelChoiceField(label='Centro de Custo', required=False, queryset=Ccusto.objects.none())



    def __init__(self,empresa,propriedade,cliente,plano_finan,c_custo,  *args,**kwargs):
        super(FiltroRecebimentosForm,self).__init__(*args,**kwargs)
        self.fields['empresa'].queryset = empresa
        self.fields['propriedade'].queryset = propriedade
        self.fields['cliente'].queryset = cliente
        self.fields['plano_finan'].queryset = plano_finan
        self.fields['c_custo'].queryset = c_custo

