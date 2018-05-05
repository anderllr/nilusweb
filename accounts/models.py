import re, random




from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin
from django.conf import settings

from nilusadm.models import Permissions,Sequenciais
from principal.models import Instancia
from nilusfin.models import Indice,Cotacao
# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        'Usuário',max_length=50,unique=True,validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras e números '
                ,'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    name = models.CharField('Nome', max_length=100,blank=True)
    email = models.EmailField('E-mail', unique=True)
    tel_user = models.CharField('Telefone', max_length=25,null=True,blank=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=False)
    is_masteruser = models.BooleanField('Usuario Master', default=True)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)
    img_user = models.ImageField('Imagem do perfil', blank=True, upload_to='images', null=True)
    qtd_users = models.PositiveIntegerField('Usuarios',blank=True, null=True)
    qtd_unity = models.PositiveIntegerField('Unidades', blank=True, null=True)
    # qtd_propriety = models.PositiveIntegerField('Propriedades', blank=True, null=True)
    user_master = models.ForeignKey('self',models.CASCADE,verbose_name='Usuario Master',blank=True,null=True)
    token = models.CharField('Token Senha', max_length=100, blank=True)
    company_p = models.ForeignKey('niluscad.Company',models.SET_NULL,verbose_name='Empresa Padrão',null=True)
    propriety_p = models.ForeignKey('niluscad.Propriety',models.SET_NULL, verbose_name='Propriedade Padrão',null=True,blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()



    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        unique_together = [
            ('username', 'user_master','email')
        ]


    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)


    def get_short_name(self):
        return str(self).split(" ")[0]




def pre_save_user(instance,**kwargs):
  if not instance.token:
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        instance.token = ''.join(random.choice(alphabet) for i in range(100))




def post_save_user(instance,created,**kwargs):
    if created:
        if instance.is_masteruser is True:

            usuario = instance
            usuario.user_master = instance
            usuario.save()

            # Insere permissões gerais.
            permissions = Permissions()
            permissions.user = instance
            permissions.nilusCadastro = True
            permissions.nilusFinanceiro = True
            permissions.nilusCompras = True
            permissions.nilusProducao = True
            permissions.nilusMaquinas = True
            permissions.nilusFiscalCont = True
            permissions.nulusContratos = True
            permissions.save()

            # Insere Sequencias.
            sequenciais = Sequenciais()
            sequenciais.user = instance
            sequenciais.empresas = 0
            sequenciais.propriedades = 0
            sequenciais.cadgeral = 0
            sequenciais.indice = 1
            sequenciais.save()

            # Insere Instancia.
            instancia = Instancia()
            instancia.user = instance
            instancia.save()

            # Insere Indice Padrao
            indice = Indice()
            indice.num_indice = 1
            indice.master_user = instance
            indice.descricao = 'Real'
            indice.simbolo = 'R$'
            indice.indice_padrao = True
            indice.save()

            # Insere Cotação Padrao
            cotacao = Cotacao()
            cotacao.indice = Indice.objects.get(master_user=instance)
            cotacao.valor_cotacao = 1.00
            cotacao.valor_cotacao_text = '1,00'
            cotacao.cotacao_padrao = True
            cotacao.save()



            from templated_email import send_templated_mail
            send_templated_mail(
                template_name='email_ativa_conta.html',
                from_email='michel.carvalho22@gmail.com',
                recipient_list=[instance.email],
                context={
                    'domain' : settings.SITE_DOMAIN,
                    'user' : instance,
                },

            )
        else:
            permissions = Permissions()
            permissions.user = instance
            permissions.nilusCadastro = False
            permissions.nilusFinanceiro = False
            permissions.nilusCompras = False
            permissions.nilusProducao = False
            permissions.nilusMaquinas = False
            permissions.nilusFiscalCont = False
            permissions.nilusContratos = False
            permissions.save()

            # Insere Instancia.
            instancia = Instancia()
            instancia.user = instance
            instancia.save()




models.signals.pre_save.connect(pre_save_user,User)
models.signals.post_save.connect(post_save_user,User)
