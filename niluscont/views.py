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
from .models import Contratos
from nilusfin.models import Indice,Cotacao
from nilusadm.models import Sequenciais
from niluscad.models import Company,Cadgeral
from .forms import FormContrato,FiltroContratosForm
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





create_contratos = CreateContrato.as_view()
edit_contratos = EditContrato.as_view()