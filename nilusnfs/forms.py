from django import forms
from niluscad.models import Company
from nilusnfs.models import Paramnfs


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
