from enum import unique

from django.db import models


# Create your models here.



class Company(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Usario Master')
    # dados principais
    num_company = models.IntegerField('Cod. Empresa')
    cnpj_cpf = models.CharField('CNPJ/CPF', max_length=20,unique=True)
    razao = models.CharField('Razão/Nome',max_length=60)
    fantasia = models.CharField('Fantasia',max_length=40,blank=True)

    # endereço
    cep = models.CharField('CEP', max_length=12, blank=True, null=True)
    endereco = models.CharField('Endereço',max_length=60,blank=True,null=True)
    numero = models.CharField('Nº',max_length=10, blank=True,null=True)
    complemento = models.CharField('Complemento', max_length=20,blank=True,null=True)
    bairro = models.CharField('Bairro', max_length=40, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=30, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)

    # dados contato
    email = models.EmailField('Email',max_length=100,blank=True,null=True)
    telefone = models.CharField('Telefone',max_length=20,blank=True,null=True)


    # outros dados
    data_cadastro = models.DateTimeField('Data de cadastro', auto_now_add=True,blank=True,null=True)
    situacao = models.BooleanField('Ativo',default=True)


    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'



    def __str__(self):
        return self.razao



class Propriety(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User', verbose_name='Uusario Master')
    company = models.ForeignKey('niluscad.Company',models.CASCADE,verbose_name='Empresa Vinculada')
    # dados principais
    num_propriety = models.IntegerField('Cod. Propriedade')
    ie = models.CharField('I.E*', max_length=20,unique=True)
    razao = models.CharField('Razão/Nome*',max_length=60)
    fantasia = models.CharField('Fantasia',max_length=40,blank=True)

    # endereço
    cep = models.CharField('CEP', max_length=12, blank=True, null=True)
    endereco = models.CharField('Endereço',max_length=60,blank=True,null=True)
    numero = models.CharField('Nº',max_length=10, blank=True,null=True)
    complemento = models.CharField('Complemento', max_length=20,blank=True,null=True)
    bairro = models.CharField('Bairro', max_length=40, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=30, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)

    # dados contato
    email = models.EmailField('Email',max_length=100,blank=True,null=True)
    telefone = models.CharField('Telefone',max_length=20,blank=True,null=True)


    # outros dados
    data_cadastro = models.DateTimeField('Data de cadastro', auto_now_add=True,blank=True,null=True)
    situacao = models.BooleanField('Ativo',default=True)


    class Meta:
        verbose_name = 'Propriedade'
        verbose_name_plural = 'Propriedades'
        unique_together = [
           ('master_user', 'ie'),('master_user', 'num_propriety'),('master_user','num_propriety','company')
        ]


    def __str__(self):
        return self.razao





class Cadgeral(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Uusario Master')
    # dados principais
    num_cad = models.IntegerField('Cod. Cadastro')
    cnpj_cpf = models.CharField('CNPJ/CPF', max_length=20,unique=True)
    razao = models.CharField('Razão/Nome',max_length=60)
    fantasia = models.CharField('Fantasia',max_length=40,blank=True)

    # endereço
    cep = models.CharField('CEP', max_length=12, blank=True, null=True)
    endereco = models.CharField('Endereço',max_length=60,blank=True,null=True)
    numero = models.CharField('Nº',max_length=10, blank=True,null=True)
    complemento = models.CharField('Complemento', max_length=20,blank=True,null=True)
    bairro = models.CharField('Bairro', max_length=40, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=30, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)

    # dados contato
    email = models.EmailField('Email',max_length=100,blank=True,null=True)
    telefone = models.CharField('Telefone',max_length=20,blank=True,null=True)


    # outros dados
    data_cadastro = models.DateTimeField('Data de cadastro', auto_now_add=True,blank=True,null=True)
    situacao = models.BooleanField('Ativo',default=True)

    # Fornecedor ou Cliente
    fornecedor = models.BooleanField('Fornecedor', default=False)
    cliente = models.BooleanField('Cliente', default=False)


    class Meta:
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'
        unique_together = [
           ('master_user', 'cnpj_cpf'),('master_user', 'num_cad')
        ]


    def __str__(self):
        return self.razao




class Ccusto(models.Model):

    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Uusario Master')
    # dados principais
    num_ccusto = models.IntegerField('Código')
    descricao = models.CharField('Descricao',max_length=60)


    class Meta:
        verbose_name = 'C. Custo'
        verbose_name_plural = 'C. Custos'
        unique_together = [
             ('master_user', 'num_ccusto')
        ]


    def __str__(self):
        return self.descricao



class PlanoFinan(models.Model):

    Scategoria_Choices = (
        ('D', 'Despesas'),
        ('R', 'Receitas'),
    )


    # informação do dono da conta (usuario Master)
    master_user = models.ForeignKey('accounts.User',models.CASCADE,verbose_name='Uusario Master')
    # dados principais
    num_plfin = models.IntegerField('Código')
    descricao = models.CharField('Descricão',max_length=60)
    sinal = models.CharField('Sinal Conta',max_length=1,choices=Scategoria_Choices)


    class Meta:
        verbose_name = 'Plano Financeiro'
        verbose_name_plural = 'Plano Financeiro'
        unique_together = [
            ('master_user', 'num_plfin')
        ]


    def __str__(self):
        return self.descricao