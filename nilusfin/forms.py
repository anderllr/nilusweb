from accounts.models import User
from django import forms
from .models import Cotacao,Indice


class FormCreateCotacao(forms.ModelForm):

    def __init__(self,user,*args,**kwargs):
        super(FormCreateCotacao,self).__init__(*args,**kwargs)
        if user.is_masteruser:
            self.fields['indice'].queryset=Indice.objects.filter(master_user=user)
        else:
            self.fields['indice'].queryset = Indice.objects.filter(
                master_user=user.user_master
            )


    class Meta:
            model = Cotacao
            fields = ['indice','data_indice','valor_cotacao']

