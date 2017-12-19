from accounts.models import User
from django import forms
from niluscad.models import Company,Propriety



class FormConfigUsuario(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormConfigUsuario,self).__init__(*args,**kwargs)
        if user.is_masteruser is True:
            self.fields['company_p'].queryset= Company.objects.filter(master_user=user)
            self.fields['propriety_p'].queryset = Propriety.objects.filter(master_user=user)
        else:
            self.fields['company_p'].queryset= Company.objects.filter(master_user=user.user_master)
            self.fields['propriety_p'].queryset = Propriety.objects.filter(master_user=user.user_master)



    class Meta:
        model = User
        fields = ['company_p','propriety_p']





