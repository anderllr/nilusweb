from datetime import date, timedelta, datetime
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,Http404
from .models import Contratos,OrdemServico
from nilusfin.models import Indice,Cotacao
from nilusadm.models import Sequenciais
from niluscad.models import Company,Cadgeral
from .forms import FormContrato,FiltroContratosForm,FiltroOSForm,FormOS
from django.db.models import Max,Count

@login_required
def contratos_list(request):

   if request.is_ajax():
        template_name = '_table_contratos.html'
   else:
       template_name = 'contratos_list.html'

   filtrou = 'nao'
   data_hoje = datetime.today




   contratos = Contratos.objects.filter(master_user=request.user.user_master)
   empresa = Company.objects.filter(master_user=request.user.user_master)
   cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
   indice = Indice.objects.filter(master_user=request.user.user_master)

   form = FiltroContratosForm(empresa,cadgeral,indice, request.GET or None)


   if form.is_valid():
       data_contrato_ini = form.cleaned_data.get('data_contrato_ini','')
       data_contrato_fim = form.cleaned_data.get('data_contrato_fim', '')
       data_vigencia_ini = form.cleaned_data.get('data_vigencia_ini', '')
       data_vigencia_fim = form.cleaned_data.get('data_vigencia_fim', '')
       periodofat = form.cleaned_data.get('periodofat','')
       empresa = form.cleaned_data.get('empresa', '')
       cadgeral = form.cleaned_data.get('cadgeral', '')
       indice = form.cleaned_data.get('indice','')

       if data_contrato_ini:
           contratos = contratos.filter(data_contrato__gte=data_contrato_ini)
           filtrou = 'ok'

       if data_contrato_fim:
           contratos = contratos.filter(data_contrato__lt=data_contrato_fim)
           filtrou = 'ok'

       if data_vigencia_ini:
           contratos = contratos.filter(vigencia__gte=data_vigencia_ini)
           filtrou = 'ok'

       if data_vigencia_ini:
           contratos = contratos.filter(vigencia__lt=data_vigencia_fim)
           filtrou = 'ok'

       if empresa:
           contratos = contratos.filter(company=empresa)
           filtrou = 'ok'

       if cadgeral:
           contratos = contratos.filter(cadgeral=cadgeral)
           filtrou = 'ok'

       if indice:
           contratos = contratos.filter(indice=indice)
           filtrou = 'ok'

       if periodofat != 'T':
           contratos = contratos.filter(periodo_fat=periodofat)
           filtrou = 'ok'


   context = {
        'contratos' : contratos,
        'form' : form,
        'filtrou' : filtrou,
        'data_hoje' : data_hoje,
   }

   return render(request, template_name,context)


class CreateContrato(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_contrato.html"]
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(CreateContrato, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateContrato, self).get_context_data(**kwargs)
        context['data_hoje'] = datetime.today
        return context

    model = Contratos
    form_class =  FormContrato

    def get_initial(self):
        initial = super(CreateContrato,self).get_initial()
        initial['company'] = self.request.user.company_p
        initial['indice'] = Indice.objects.get(master_user=self.request.user.user_master,indice_padrao=True)
        return initial

    def get_success_url(self):
        return reverse_lazy('contrato_list')


    def form_valid(self,form):
        contrato = form.save(commit=False)

        if contrato.data_contrato is None:
             contrato.data_contrato = datetime.now()

        contrato.valor_unit = contrato.valor_unit_text.replace('R$','').replace('.','').replace(',','.')

        cotacao = contrato.cotacao
        conta = Decimal(contrato.valor_unit) * Decimal(cotacao.valor_cotacao)
        contrato.valor = conta


        contrato.master_user = self.request.user.user_master
        seq_contrato = Sequenciais.objects.get(user=self.request.user.user_master)
        contrato.num_cont = seq_contrato.contratos + 1
        seq_contrato.contratos = contrato.num_cont
        seq_contrato.save()
        contrato.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditContrato(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_contrato.html"]
        else:
            raise Http404



    def get_success_url(self):
        return reverse_lazy('contratos_list')



    def get_context_data(self, **kwargs):
        context = super(EditContrato, self).get_context_data(**kwargs)
        context['dados_cadastro'] = Contratos.objects.get(pk=self.kwargs['pk'])
        context['data_hoje'] = datetime.today
        return context

    def get_form_kwargs(self):
        kwargs = super(EditContrato, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    model = Contratos
    form_class =  FormContrato

    def form_valid(self,form):
        contrato = form.save(commit=False)



        if 'indice' in form.changed_data:

            contrato.valor_unit = contrato.valor_unit_text.replace('R$', '').replace('.', '').replace(',', '.')

            cotacao = contrato.cotacao
            conta = Decimal(contrato.valor_unit) * Decimal(cotacao.valor_cotacao)
            contrato.valor = conta

        if 'cotacao' in form.changed_data:

            contrato.valor_unit = contrato.valor_unit_text.replace('R$', '').replace('.', '').replace(',', '.')

            cotacao = contrato.cotacao
            conta = Decimal(contrato.valor_unit) * Decimal(cotacao.valor_cotacao)
            contrato.valor = conta

        if 'valor_unit_text' in form.changed_data:

            contrato.valor_unit = contrato.valor_unit_text.replace('R$', '').replace('.', '').replace(',', '.')

            cotacao = contrato.cotacao
            conta = Decimal(contrato.valor_unit) * Decimal(cotacao.valor_cotacao)
            contrato.valor = conta

        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


@login_required
def delete_contratos(request, pk):

    contrato = get_object_or_404(Contratos,master_user=request.user.user_master,pk=pk)

    try:
       contrato.delete()
    except:
       print('erro na exclusao')

    return redirect('contratos_list')



###################################################################################
#                   ORDENS DE SERVIÇOS                                            #
###################################################################################

@login_required
def os_list(request):

   if request.is_ajax():
        template_name = '_table_os.html'
   else:
       template_name = 'os_list.html'

   filtrou = 'nao'
   data_hoje = datetime.today




   os = OrdemServico.objects.filter(master_user=request.user.user_master)
   empresa = Company.objects.filter(master_user=request.user.user_master)
   cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
   contratos = Contratos.objects.filter(master_user=request.user.user_master)

   form = FiltroOSForm(empresa,cadgeral,contratos, request.GET or None)


   if form.is_valid():
       data_os_ini = form.cleaned_data.get('data_os_ini','')
       data_os_fim = form.cleaned_data.get('data_os_fim', '')
       empresa = form.cleaned_data.get('empresa', '')
       cadgeral = form.cleaned_data.get('cadgeral', '')
       contratos = form.cleaned_data.get('contratos','')

       if data_os_ini:
           os = os.filter(data_os__gte=data_os_ini)
           filtrou = 'ok'

       if data_os_fim:
           os = os.filter(data_os__lt=data_os_fim)
           filtrou = 'ok'

       if empresa:
           os = os.filter(company=empresa)
           filtrou = 'ok'

       if cadgeral:
           os = os.filter(cadgeral=cadgeral)
           filtrou = 'ok'

       if contratos:
           os = os.filter(contrato=contratos)
           filtrou = 'ok'

   context = {
        'os' : os,
        'form' : form,
        'filtrou' : filtrou,
        'data_hoje' : data_hoje,
   }

   return render(request, template_name,context)




class CreateOS(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_os.html"]
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(CreateOS, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateOS, self).get_context_data(**kwargs)
        context['data_hoje'] = datetime.today
        return context

    model = OrdemServico
    form_class =  FormOS

    def get_initial(self):
        initial = super(CreateOS,self).get_initial()
        initial['company'] = self.request.user.company_p
        return initial

    def get_success_url(self):
        return reverse_lazy('os_list')


    def form_valid(self,form):
        os = form.save(commit=False)

        if os.data_os is None:
             os.data_os = datetime.now()

        os.valor_unit = os.valor_unit_text.replace('R$','').replace('.','').replace(',','.')

        os.master_user = self.request.user.user_master
        seq_os = Sequenciais.objects.get(user=self.request.user.user_master)
        os.num_os = seq_os.ordensservico + 1
        seq_os.ordensservico = os.num_os
        seq_os.save()
        os.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


class EditOS(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_os.html"]
        else:
            raise Http404



    def get_success_url(self):
        return reverse_lazy('os_list')



    def get_context_data(self, **kwargs):
        context = super(EditOS, self).get_context_data(**kwargs)
        context['dados_cadastro'] = OrdemServico.objects.get(pk=self.kwargs['pk'])
        context['data_hoje'] = datetime.today
        return context

    def get_form_kwargs(self):
        kwargs = super(EditOS, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    model = OrdemServico
    form_class = FormOS

    def form_valid(self,form):
        os = form.save(commit=False)


        if 'valor_unit_text' in form.changed_data:

            os.valor_unit = os.valor_unit_text.replace('R$', '').replace('.', '').replace(',', '.')

        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


@login_required
def delete_os(request, pk):

    os = get_object_or_404(OrdemServico,master_user=request.user.user_master,pk=pk)

    try:
       os.delete()
    except:
       print('erro na exclusao')

    return redirect('os_list')




edit_os = EditOS.as_view()
create_os = CreateOS.as_view()
create_contratos = CreateContrato.as_view()
edit_contratos = EditContrato.as_view()