from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserCustomCreationForm(UserCreationForm):
    # aceite = forms.BooleanField( required=False)
    #
    # def clean_aceite(self):
    #     aceite = self.cleaned_data.get('aceite', False)
    #
    #     if not aceite:
    #         raise forms.ValidationError('Você deve aceitar os termos de uso e privacidade para concluir seu cadastro')
    #     return aceite

    def __init__(self,  *args, **kwargs):
        super(UserCustomCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username','name','email','qtd_users','qtd_unity','company_p']


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','name','email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email','name','is_active','is_staff','is_superuser']



class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(label='E-mail')





class UserViewerCreationForm(UserCreationForm):


    class Meta:
        model = User
        fields = ['username','name','email']