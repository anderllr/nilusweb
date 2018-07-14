from threading import Thread
from django.http import HttpResponse,Http404
from datetime import date, timedelta, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from .models import Paramnfs,TmpFat
from .forms import FormCreateParamnfs,FiltroBuscaFaturamento,FormFaturamento,FiltroBuscaNotas
from nilusadm.models import Sequenciais
from nilusfin.models import Contafinanceira
from niluscad.models import Company,Cadgeral,PlanoFinan
from niluscont.servicos import cria_lancamento_credito,cria_lancamento_credito_unificado,fat
from nilusnfs.models import NotasFiscais
from django.db.models import Q
from .enotas_util import cad_empresa_emissora,edit_empresa_emissora,refresh_situacao_nfs,cancela_nfs



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

        cad_empresa_emissora(paramnfs)
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
        paramnfs = form.save(commit=False)

        edit_empresa_emissora(paramnfs)
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

    lista_fat = TmpFat.objects.filter(master_user=request.user.user_master,tipo='C',situacao=False)
    empresa = Company.objects.filter(master_user=request.user.user_master)
    cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
    planofinan = PlanoFinan.objects.filter(master_user=request.user.user_master,sinal='R')
    contafinan = Contafinanceira.objects.filter(master_user=request.user.user_master,conta_recebimento=True)



    form = FiltroBuscaFaturamento(empresa,cadgeral,request.GET or None)




    if form.is_valid():
        prox_fat_ini = form.cleaned_data.get('prox_fat_ini', '')
        prox_fat_fim = form.cleaned_data.get('prox_fat_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        lista_os = form.cleaned_data.get('lista_os','')




        if lista_os:
            lista_fat = TmpFat.objects.filter(master_user=request.user.user_master, situacao=False)
            filtrou = 'ok'

        if prox_fat_ini:
            lista_fat = lista_fat.filter(data_fat__gte=prox_fat_ini)
            filtrou = 'ok'

        if prox_fat_fim:
            lista_fat = lista_fat.filter(data_fat__lt=prox_fat_fim+timedelta(days=1))
            filtrou = 'ok'

        if empresa:
            lista_fat = lista_fat.filter(Q(contrato__company=empresa) | Q(os__company=empresa))
            filtrou = 'ok'

        if cadgeral:
            lista_fat = lista_fat.filter(Q(contrato__cadgeral=cadgeral) | Q(os__cadgeral=cadgeral))
            filtrou = 'ok'





    form_fat = FormFaturamento(lista_fat,planofinan,contafinan,request.POST or None)
    if form_fat.is_valid():
        plano_financeiro = form_fat.cleaned_data['plano_financeiro']
        # fat_unificado = form_fat.cleaned_data['fatura_unificado']
        faturar = form_fat.cleaned_data['ids_fat']
        data_fat = form_fat.cleaned_data['data_fat']
        contafinan = form_fat.cleaned_data['conta_financeira']
        if data_fat is None:
            data_fat = datetime.now()




        faturamento = Thread(target=fat,
                     args=[faturar, plano_financeiro, data_fat, contafinan])
        faturamento.start()
        # else:
        #
        #         retorno_unificado = cria_lancamento_credito_unificado(faturar,plano_financeiro,data_fat,contafinan)



    context = {
        'lista': lista_fat,
        'form' : form,
        'filtrou' : filtrou,
        'data_hoje' : data_hoje,
        'form_fat': form_fat,
    }
    return render(request, template_name, context)




# ######################################################################################################
#               NOTAS FISCAIS EMITIDAS                                                                 #
########################################################################################################

@login_required
def nfs_list(request):

    if request.is_ajax():
        template_name = '_table_nfs.html'
    else:
        template_name = 'nfs_list.html'

    filtrou = 'nao'
    data_hoje = datetime.today

    notas = NotasFiscais.objects.filter(master_user=request.user.user_master).order_by('-data_emissao')
    empresa = Company.objects.filter(master_user=request.user.user_master)
    cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)

    notas_pendentes = NotasFiscais.objects.filter(master_user=request.user.user_master,
                                                  envio_concluido='N')
    # print(notas_pendentes)

    refresh_notas = Thread(target=refresh_situacao_nfs,
                           args=[notas_pendentes])
    refresh_notas.start()

    form = FiltroBuscaNotas(empresa,cadgeral,request.GET or None)

    if form.is_valid():
        dt_emissao_ini = form.cleaned_data.get('dt_emissao_ini', '')
        dt_emissao_fim = form.cleaned_data.get('dt_emissao_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')





        if dt_emissao_ini:
            notas = notas.filter(data_emissao__gte=dt_emissao_ini)
            filtrou = 'ok'

        if dt_emissao_fim:
            notas = notas.filter(data_emissao__lt=dt_emissao_fim+timedelta(days=1))
            filtrou = 'ok'

        if empresa:
            notas = notas.filter(company=empresa)
            filtrou = 'ok'

        if cadgeral:
            notas = notas.filter(cadgeral=cadgeral)
            filtrou = 'ok'


        notas = notas.order_by('-data_emissao')





    context = {
        'notas': notas,
        'form' : form,
        'filtrou' : filtrou,
        'data_hoje' : data_hoje,
    }
    return render(request, template_name, context)



@login_required
def refresh_nfs(request, pk):
    nfs = NotasFiscais.objects.filter(master_user=request.user.user_master,pk=pk)
    refresh_situacao_nfs(nfs)

    return redirect('nfs_list')



@login_required
def info_nfs(request,pk):

    if request.is_ajax():
        template_name = '_info_nfs.html'
    else:
        raise Http404

    nf = NotasFiscais.objects.get(pk=pk)

    context = {
        'nf': nf,
    }

    return render(request, template_name, context)


@login_required
def cancel_nfs(request,pk):

    nf = NotasFiscais.objects.get(master_user=request.user.user_master,pk=pk)
    cancela_nfs(nf)

    return redirect('nfs_list')



















create_paramnfs =  CreateParamNFS.as_view()
edit_paramnfs = EditParamNFS.as_view()