from django.db import models


# Create your models here.

class Instancia(models.Model):
    user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usuário')
    company = models.ForeignKey('niluscad.Company',models.SET_NULL,verbose_name='Empresa padrão',null=True,blank=True)
    propriety = models.ForeignKey('niluscad.Propriety',models.SET_NULL,verbose_name='Propriedade Padrão',null=True,blank=True)


    class Meta:
        verbose_name= 'Instancia'
        verbose_name_plural = 'Instancias'



