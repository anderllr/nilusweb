from datetime import date, timedelta, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,Http404
from .models import Paramnfs
from niluscont.models import Contratos,OrdemServico
from niluscont.servicos import lista_contratoeos
from .forms import FormCreateParamnfs,FiltroBuscaFaturamento,FormFaturamento
from nilusadm.models import Sequenciais
from niluscad.models import Company,Cadgeral
from django.db.models import Max,Count
from operator import itemgetter

@login_required
def paramnfs_list(request):

   if request.is_ajax():
        template_name = '_table_paramnfs.html'
   else:
       template_name = 'paramnfs_list.html'

   paramnfs = Paramnfs.objects.filter(master_user=request.user.user_master)
   pendencias_cad = []
   for p in paramnfs:
        if not p.company.fantasia or\
            not p.company.insc_mun or\
                not p.company.endereco or\
                    not p.company.endereco or\
                        not p.company.cidade or\
                            not p.company.uf or\
                                not p.company.cep or\
                                    not p.company.bairro:
                                        pendencias_cad.append({'pk_empresa': p.company.pk })



   context = {
      'paramnfs' : paramnfs,
      'pendencias' : pendencias_cad
   }

   return render(request, template_name,context)





class CreateParamNFS(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        return ["create_paramnfs.html"]

    def get_context_data(self, **kwargs):
        context = super(CreateParamNFS, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateParamNFS, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




    model = Paramnfs
    form_class = FormCreateParamnfs


    def get_success_url(self):
        return reverse_lazy('paramnfs_list')


    def form_valid(self,form):
        paramnfs = form.save(commit=False)
        paramnfs.master_user = self.request.user.user_master
        seq_paramnfs = Sequenciais.objects.get(user=self.request.user.user_master)


        paramnfs.num_param = seq_paramnfs.paramnfs + 1
        seq_paramnfs.paramnfs = paramnfs.num_param
        seq_paramnfs.save()
        paramnfs.save()

        return redirect(self.get_success_url())




class EditParamNFS(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
       return ["edit_paramnfs.html"]

    def get_success_url(self):
        return reverse_lazy('paramnfs_list')

    def get_form_kwargs(self):
        kwargs = super(EditParamNFS, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(EditParamNFS, self).get_context_data(**kwargs)
        context['dados_cadastro'] = Paramnfs.objects.get(pk=self.kwargs['pk'])
        return context

    model = Paramnfs
    form_class = FormCreateParamnfs

    def form_valid(self,form):
        form.save()
        return redirect(self.get_success_url())


@login_required
def delete_paramnfs(request, pk):
    paramnfs = get_object_or_404(Paramnfs,master_user=request.user.user_master,pk=pk)
    try:
       paramnfs.delete()
    except:
       print('erro na exclusao')

    return redirect('paramnfs_list')



# ######################################################################################################
#               FATURAMENTO E EMISSÃO DE NOTAS DE SERVIÇOS                                             #
########################################################################################################

@login_required
def fat_list(request):

    if request.is_ajax():
        template_name = '_table_faturamento.html'
    else:
        template_name = 'fat_list.html'

    filtrou = 'nao'
    data_hoje = datetime.today

    contratos = Contratos.objects.filter(master_user=request.user.user_master)
    ordemservico = OrdemServico.objects.none()
    empresa = Company.objects.filter(master_user=request.user.user_master)
    cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
    # contratos_filtro = Contratos.objects.filter(master_user = request.user.user_master)

    form = FiltroBuscaFaturamento(empresa,cadgeral,request.GET or None)

    if form.is_valid():
        prox_fat_ini = form.cleaned_data.get('prox_fat_ini', '')
        prox_fat_fim = form.cleaned_data.get('prox_fat_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        lista_os = form.cleaned_data.get('lista_os','')



        if lista_os:
            ordemservico = OrdemServico.objects.filter(master_user=request.user.user_master, situacao_fat='A')
            filtrou = 'ok'

        if prox_fat_ini:
            contratos = contratos.filter(prox_faturamento__gte=prox_fat_ini)
            ordemservico = ordemservico.filter(data_os__gte=prox_fat_ini)
            filtrou = 'ok'

        if prox_fat_fim:
            contratos = contratos.filter(prox_faturamento__lt=prox_fat_fim+timedelta(days=1))
            ordemservico = ordemservico.filter(data_os__lt=prox_fat_fim+timedelta(days=1))
            filtrou = 'ok'

        if empresa:
            contratos = contratos.filter(company=empresa)
            ordemservico = ordemservico.filter(company=empresa)
            filtrou = 'ok'

        if cadgeral:
            contratos = contratos.filter(cadgeral=cadgeral)
            ordemservico = ordemservico.filter(cadgeral=cadgeral)
            filtrou = 'ok'


    lista = lista_contratoeos(contratos,ordemservico)

    lista = sorted(lista,key=itemgetter('pfat'))

    context = {
        'lista': lista,
        'form' : form,
        'filtrou' : filtrou,
        'data_hoje' : data_hoje
    }
    return render(request, template_name, context)




create_paramnfs =  CreateParamNFS.as_view()
edit_paramnfs = EditParamNFS.as_view()