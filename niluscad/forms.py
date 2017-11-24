from accounts.models import User
from niluscad.models import Company,Propriety
from django import forms





class FormPropriety(forms.ModelForm):


    def __init__(self,user,*args,**kwargs):
        super(FormPropriety,self).__init__(*args,**kwargs)
        if user.is_masteruser is True:
            self.fields['company'].queryset = Company.objects.filter(master_user=user)
        else:
            self.fields['company'].queryset = Company.objects.filter(master_user=user.user_master)

    class Meta:
        model = Propriety
        fields = ['company','ie', 'razao', 'fantasia', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade',
                  'uf','email', 'telefone']



