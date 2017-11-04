from accounts.models import User
from django import forms
from niluscad.models import Company,Propriety



class FormConfigUsuario(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormConfigUsuario,self).__init__(*args,**kwargs)
        self.fields['company_p'].queryset=Company.objects.filter(user=user.pk)
        self.fields['propriety_p'].queryset=Propriety.objects.filter(user=user.pk)


    class Meta:
        model = User
        fields = ['company_p','propriety_p']