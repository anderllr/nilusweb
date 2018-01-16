from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,Http404
from accounts.models import User
from nilusadm.models import Sequenciais
from .models import Contafinanceira,Cotacao,Indice
from .forms import FormCreateCotacao

# Create your views here.



##########################################################################################
#                   CONTAS BANCARIAS/CAIXA                                               #
##########################################################################################



@login_required
def conta_list(request):

    if request.is_ajax():
        template_name = '_table_conta.html'
    else:
        template_name = 'conta_list.html'



    if request.user.is_masteruser is True:
         conta = Contafinanceira.objects.filter(master_user=request.user.pk)
    else:
         conta = Contafinanceira.objects.filter(master_user=request.user.user_master)



    context = {
       'conta' : conta
    }

    return render(request, template_name, context)


class CreateConta(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_conta.html"]
        else:
            raise Http404


    model = Contafinanceira
    fields = ['conta_bancaria','agencia','conta','descricao','usa_limite','vlr_limite_text','conta_pagamento','conta_recebimento']


    def get_success_url(self):
        return reverse_lazy('conta_list')


    def form_valid(self,form):
        conta = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            conta.master_user = self.request.user
            seq_conta = Sequenciais.objects.get(user=self.request.user)
        else:
            conta.master_user = self.request.user.user_master
            seq_conta = Sequenciais.objects.get(user=self.request.user.user_master)


        conta.num_conta = seq_conta.conta + 1
        seq_conta.conta = conta.num_conta
        seq_conta.save()
        if conta.vlr_limite_text is not None:
            conta.vlr_limite = conta.vlr_limite_text.replace('R$','').replace('.','').replace(',','.')
        conta.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditConta(LoginRequiredMixin,UpdateView):


    def get_context_data(self, **kwargs):
        context = super(EditConta, self).get_context_data(**kwargs)
        context['dados_cadastro'] = Contafinanceira.objects.get(pk=self.kwargs['pk'])
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_conta.html"]
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('conta_list')

    model = Contafinanceira
    fields = ['conta_bancaria','agencia', 'conta', 'descricao', 'usa_limite', 'vlr_limite_text', 'conta_pagamento', 'conta_recebimento']


    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




@login_required
def delete_conta(request, pk):
    if request.user.is_masteruser is True:
        conta = get_object_or_404(Contafinanceira,master_user=request.user,pk=pk)
    else:
        conta = get_object_or_404(Contafinanceira,master_user=request.user.user_master,pk=pk)


    conta.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('conta_list')




##########################################################################################
#                               INDICES                                                  #
##########################################################################################

@login_required
def indice_list(request):

    if request.is_ajax():
        template_name = '_table_indice.html'
    else:
        template_name = 'indice_list.html'



    if request.user.is_masteruser is True:
         indice = Indice.objects.filter(master_user=request.user.pk)
    else:
         indice = Indice.objects.filter(master_user=request.user.user_master)



    context = {
       'indice' : indice
    }
    return render(request, template_name, context)


class CreateIndice(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_indice.html"]
        else:
            raise Http404



    model = Indice
    fields = ['descricao','simbolo']


    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form):
        indice = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            indice.master_user = self.request.user
            seq_indice = Sequenciais.objects.get(user=self.request.user)
        else:
            indice.master_user = self.request.user.user_master
            seq_indice = Sequenciais.objects.get(user=self.request.user.user_master)


        indice.num_indice = seq_indice.indice + 1
        seq_indice.indice = indice.num_indice
        seq_indice.save()
        indice.save()

        cotacoes_indice = Cotacao.objects.filter(indice=None,user_cad=self.request.user)
        cotacoes_indice.update(
            indice=indice
        )

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


class EditIndice(LoginRequiredMixin,UpdateView):


    def get_context_data(self, **kwargs):
        context = super(EditIndice, self).get_context_data(**kwargs)
        context['dados_cadastro'] = Indice.objects.get(pk=self.kwargs['pk'])
        context['cotacoes'] = Cotacao.objects.filter(indice=self.kwargs['pk']).order_by('data_indice')
        return context

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_indice.html"]
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('indice_list')

    model = Indice
    fields = ['descricao', 'simbolo']

    def form_valid(self,form):
        indice = form.save(commit=False)

        cotacoes_indice = Cotacao.objects.filter(indice=None, user_cad=self.request.user)
        cotacoes_indice.update(
            indice=indice
        )
        indice.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




@login_required
def delete_indice(request, pk):
    if request.user.is_masteruser is True:
        indice = get_object_or_404(Indice,master_user=request.user,pk=pk)
    else:
        indice = get_object_or_404(Indice,master_user=request.user.user_master,pk=pk)


    indice.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('indice_list')


##########################################################################################
#                               COTACAO                                                  #
##########################################################################################

@login_required
def cotacao_list(request,pk):

    if request.is_ajax():
        template_name = '_table_cotacao.html'
    else:
        template_name = 'cotacao_list.html'

    indice = Indice.objects.filter(pk=pk)


    if request.user.is_masteruser is True:
         cotacao = Cotacao.objects.filter(indice=indice)

    else:
         cotacao = Cotacao.objects.filter(indice=indice)



    context = {
       'cotacao' : cotacao,
       'indice' : indice
    }

    return render(request, template_name, context)


class CreateCotacao_create_indice(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_cotacao.html"]
        else:
            raise Http404


    model = Cotacao
    fields = ['data_indice','valor_cotacao']

    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form):
        cotacao = form.save(commit=False)
        cotacao.user_cad = self.request.user
        cotacao.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class CreateCotacao_edit_indice(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_cotacao.html"]
        else:
            raise Http404


    model = Cotacao
    fields = ['data_indice', 'valor_cotacao']

    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form):
        cotacao = form.save(commit=False)
        cotacao.user_cad = self.request.user
        cotacao.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




class CreateCotacao_grid_indice(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_cotacao_grid_indice.html"]
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(CreateCotacao_grid_indice, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    model = Cotacao
    form_class = FormCreateCotacao

    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form,**kwargs):
        cotacao = form.save(commit=False)
        cotacao.user_cad = self.request.user
        cotacao.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())






@login_required
def delete_cotacao(request, pk):
    cotacao = get_object_or_404(Cotacao,pk=pk)
    cotacao.delete()
    # messages.success(request, 'Grupo removido com sucesso !!')
    return HttpResponse('ok')




create_indice = CreateIndice.as_view()
edit_indice = EditIndice.as_view()
create_conta = CreateConta.as_view()
create_cotacao_create_indice = CreateCotacao_create_indice.as_view()
create_cotacao_edit_indice = CreateCotacao_edit_indice.as_view()
edit_conta = EditConta.as_view()
create_cotacao_grid_indice = CreateCotacao_grid_indice.as_view()




