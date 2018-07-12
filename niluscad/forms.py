from accounts.models import User
from niluscad.models import Company,Propriety,Talhao,PlanoFinan,Grupodre
from django import forms





class FormPropriety(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormPropriety,self).__init__(*args,**kwargs)

        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
            self.fields['company'].empty_label = "Selecione a empresa"
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)
            self.fields['company'].empty_label = "Selecione a empresa"


    def get_initial(self):
        initial = super(FormPropriety,self).get_initial()
        initial['company'] = 'Empresa'
        return initial


    class Meta:
        model = Propriety
        fields = ['company','ie', 'razao', 'fantasia', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade',
                  'uf','area']




class FormPlanoFinanceiro(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(FormPlanoFinanceiro, self).__init__(*args, **kwargs)
        self.fields['grupodre'].queryset = Grupodre.objects.filter(master_user=user.user_master)
        self.fields['grupodre'].empty_label = 'Informe o grupo'
        self.fields['sinal'].empty_label = "Informe o Sinal da Conta"


    class Meta:
        model = PlanoFinan
        fields = ['descricao','sinal','grupodre']





