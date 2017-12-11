from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,Http404
from accounts.models import User
from nilusadm.models import Sequenciais
from .models import Company,Propriety,Cadgeral,Ccusto,PlanoFinan,Talhao
from .forms import FormPropriety

from django.db.models import Max,Count


# Create your views here.




########################################################################################################################
#                                      Empresas                                                                        #
########################################################################################################################



@login_required
def company_list(request):

   if request.is_ajax():
        template_name = '_table_companys.html'
   else:
       template_name = 'company_list.html'

   # user = User.objects.get(user=request.user.pk)

   if request.user.is_masteruser is True:
        companys = Company.objects.filter(master_user=request.user.pk)
   else:
        companys = Company.objects.filter(master_user=request.user.user_master)


   context = {
      'companys' : companys

   }

   return render(request, template_name,context)


class CreateCompany(LoginRequiredMixin,CreateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_company.html"]
        else:
            return ["create_company.html"]


    def get_context_data(self, **kwargs):
        context = super(CreateCompany, self).get_context_data(**kwargs)
        context['texto_modal'] = 'Inclusão de Empresas'
        return context

    model = Company
    fields = ['cnpj_cpf','razao','fantasia','cep','endereco','numero','complemento','bairro','cidade','uf',
              'email','telefone']

    def get_success_url(self):
        return reverse_lazy('company_list')

    def form_valid(self,form):
        empresa = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            empresa.master_user = self.request.user
            seq_emp = Sequenciais.objects.get(user=self.request.user)
        else:
            empresa.master_user = self.request.user.user_master
            seq_emp = Sequenciais.objects.get(user=self.request.user.user_master)

        empresa.num_company = seq_emp.empresas + 1
        seq_emp.empresas = empresa.num_company
        seq_emp.save()
        empresa.save()




        if self.request.is_ajax():
            context = self.get_context_data(form=form,ok='ok', success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




class EditCompany(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_company.html"]
        else:
            return ["edit_company.html"]

    def get_success_url(self):
        return reverse_lazy('company_list')


    def get_context_data(self, **kwargs):
        context = super(EditCompany,self).get_context_data(**kwargs)
        context['propriety_list'] = Propriety.objects.filter(company=self.kwargs['pk'])
        context['dados_cadastro'] = Company.objects.get(pk=self.kwargs['pk'])


        return context




    model = Company
    fields = [ 'razao', 'fantasia', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf',
              'email', 'telefone','situacao']


    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form ,success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())







@login_required
def delete_company(request, pk):
    if request.user.is_masteruser is True:
        empresa = get_object_or_404(Company,master_user=request.user,pk=pk)
    else:
        empresa = get_object_or_404(Company,master_user=request.user.user_master,pk=pk)


    empresa.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('company_list')



########################################################################################################################
#                                      Propriedades                                                                    #
########################################################################################################################





@login_required
def propriety_list(request):


   if request.is_ajax():
        template_name = '_table_propriety.html'
   else:
        template_name = 'propriety_list.html'




   if request.user.is_masteruser is True:
        prop = Propriety.objects.filter(master_user=request.user.pk)
   else:
        prop = Propriety.objects.filter(master_user=request.user.user_master)



   context = {
      'prop' : prop

   }

   return render(request, template_name,context)


class CreatePropriety(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_propriety.html"]
        else:
            return ["create_propriety_old.html"]

    def get_form_kwargs(self):
        kwargs = super(CreatePropriety, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(CreatePropriety,self).get_context_data(**kwargs)
        context['talhao'] = Talhao.objects.filter(propriety=None,user_cad=self.request.user)
        return context


    model = Propriety
    form_class = FormPropriety




    def get_success_url(self):
        return reverse_lazy('propriety_list')

    def form_valid(self,form):
        prop = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            prop.master_user = self.request.user
            seq_prop = Sequenciais.objects.get(user=self.request.user)
        else:
            prop.master_user = self.request.user.user_master
            seq_prop = Sequenciais.objects.get(user=self.request.user.user_master)


        prop.num_propriety = seq_prop.propriedades + 1
        seq_prop.propriedades = prop.num_propriety
        seq_prop.save()
        prop.save()

        talhao_inclusoes = Talhao.objects.filter(propriety=None, user_cad=self.request.user)
        talhao_inclusoes.update(
            propriety=prop
        )

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditPropriety(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_propriety.html"]
        else:
            return ["create_propriety.html"]

    def get_success_url(self):
        return reverse_lazy('company_list')

    def get_form_kwargs(self):
        kwargs = super(EditPropriety, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EditPropriety, self).get_context_data(**kwargs)
        context['talhao'] = Talhao.objects.filter(propriety=self.kwargs['pk'])
        return context


    model = Propriety
    form_class = FormPropriety



    def form_valid(self,form):
        prop = form.save(commit=False)
        talhao_inclusoes = Talhao.objects.filter(propriety=None, user_cad=self.request.user)
        talhao_inclusoes.update(
            propriety=prop.pk
        )
        prop.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




@login_required
def delete_propriety(request, pk):
    if request.user.is_masteruser is True:
        prop = get_object_or_404(Propriety,master_user=request.user,pk=pk)
    else:
        prop = get_object_or_404(Propriety,master_user=request.user.user_master,pk=pk)


    prop.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('propriety_list')


########################################################################################################################
#                                      Cadastro Geral                                                                  #
########################################################################################################################

@login_required
def cadgeral_list(request):

   if request.is_ajax():
       template_name = '_table_cadgeral.html'
   else:
       template_name = 'cadgeral_list.html'


   if request.user.is_masteruser is True:
        cad = Cadgeral.objects.filter(master_user=request.user.pk)
   else:
        cad = Cadgeral.objects.filter(master_user=request.user.user_master)



   context = {
      'cad' : cad

   }

   return render(request, template_name, context)


class CreateCadGeral(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_cadgeral.html"]
        else:
            return ["create_cadgeral.html"]


    # def get_context_data(self,**kwargs):
    #     context = super(CreateCompany,self).get_context_data(**kwargs)
    #     context['test'] = 'Luan'
    #
    #     return context



    model = Cadgeral
    fields = ['cnpj_cpf','razao','fantasia','cep','endereco','numero','complemento','bairro','cidade','uf',
              'email','telefone','fornecedor','cliente']

    def get_success_url(self):
        return reverse_lazy('cadgeral_list')

    def form_valid(self,form):
        Cadgeral = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            Cadgeral.master_user = self.request.user
            seq_cad = Sequenciais.objects.get(user=self.request.user)
        else:
            Cadgeral.master_user = self.request.user.user_master
            seq_cad = Sequenciais.objects.get(user=self.request.user.user_master)

        Cadgeral.num_cad = seq_cad.cadgeral + 1
        seq_cad.cadgeral = Cadgeral.num_cad
        seq_cad.save()
        Cadgeral.save()


        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())





class EditCadGeral(LoginRequiredMixin,UpdateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_cadgeral.html"]
        else:
            return ["edit_cadgeral.html"]

    def get_success_url(self):
        return reverse_lazy('cadgeral_list')

    model = Cadgeral
    fields = ['cnpj_cpf', 'razao', 'fantasia', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'uf',
              'email', 'telefone','fornecedor','cliente']


    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



@login_required
def delete_cadgeral(request, pk):
    if request.user.is_masteruser is True:
        cad = get_object_or_404(Cadgeral,master_user=request.user,pk=pk)
    else:
        cad = get_object_or_404(Cadgeral,master_user=request.user.user_master,pk=pk)


    cad.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('cadgeral_list')




########################################################################################################################
#                                      C. Custo                                                                        #
########################################################################################################################


@login_required
def ccusto_list(request):

    if request.is_ajax():
        template_name = '_table_ccusto.html'
    else:
        template_name = 'ccusto_list.html'



    if request.user.is_masteruser is True:
         ccusto = Ccusto.objects.filter(master_user=request.user.pk)
    else:
         ccusto = Ccusto.objects.filter(master_user=request.user.user_master)



    context = {
       'ccusto' : ccusto
    }

    return render(request, template_name, context)


class CreateCcusto(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_ccusto.html"]
        else:
            raise Http404


    # def get_context_data(self,**kwargs):
    #     context = super(CreatePropriety,self).get_context_data(**kwargs)
    #     context['test'] = 'Luan'
    #
    #     return context



    model = Ccusto
    fields = ['descricao']


    def get_success_url(self):
        return reverse_lazy('ccusto_list')


    def form_valid(self,form):
        ccusto = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            ccusto.master_user = self.request.user
            seq_ccusto = Sequenciais.objects.get(user=self.request.user)
        else:
            ccusto.master_user = self.request.user.user_master
            seq_ccusto = Sequenciais.objects.get(user=self.request.user.user_master)


        ccusto.num_ccusto = seq_ccusto.ccusto + 1
        seq_ccusto.ccusto= ccusto.num_ccusto
        seq_ccusto.save()
        ccusto.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditCcusto(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_ccusto.html"]
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('ccusto_list')

    model = Ccusto
    fields = ['descricao']


    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




@login_required
def delete_ccusto(request, pk):
    if request.user.is_masteruser is True:
        ccusto = get_object_or_404(Ccusto,master_user=request.user,pk=pk)
    else:
        ccusto = get_object_or_404(Ccusto,master_user=request.user.user_master,pk=pk)


    ccusto.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('ccusto_list')


########################################################################################################################
#                                      Plano Financeiro                                                                #
########################################################################################################################


@login_required
def planofinan_list(request):

    if request.is_ajax():
        template_name = '_table_planofinan.html'
    else:
        template_name = 'planofinan_list.html'



    if request.user.is_masteruser is True:
         plfin = PlanoFinan.objects.filter(master_user=request.user.pk)
    else:
         plfin = PlanoFinan.objects.filter(master_user=request.user.user_master)



    context = {
       'plfin' : plfin
    }

    return render(request, template_name, context)


class CreatePlanoFinan(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_planofinan.html"]
        else:
            raise Http404


    # def get_context_data(self,**kwargs):
    #     context = super(CreatePropriety,self).get_context_data(**kwargs)
    #     context['test'] = 'Luan'
    #
    #     return context



    model = PlanoFinan
    fields = ['descricao','sinal']


    def get_success_url(self):
        return reverse_lazy('planofinan_list')


    def form_valid(self,form):
        planofinan = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            planofinan.master_user = self.request.user
            seq_planofinan = Sequenciais.objects.get(user=self.request.user)
        else:
            planofinan.master_user = self.request.user.user_master
            seq_planofinan = Sequenciais.objects.get(user=self.request.user.user_master)



        planofinan.num_plfin = seq_planofinan.planofinan + 1
        seq_planofinan.planofinan = planofinan.num_plfin
        seq_planofinan.save()
        planofinan.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditPlanofinan(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_planofinan.html"]
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('planofinan_list')

    model = PlanoFinan
    fields = ['descricao','sinal']


    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




@login_required
def delete_planofinan(request, pk):
    if request.user.is_masteruser is True:
        planofinan = get_object_or_404(PlanoFinan,master_user=request.user,pk=pk)
    else:
        planofinan = get_object_or_404(PlanoFinan,master_user=request.user.user_master,pk=pk)


    planofinan.delete()


    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('planofinan_list')




########################################################################################################################
#                                      Talhões                                                                         #
########################################################################################################################


class CreateTalhao(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_talhao.html"]
        else:
            raise Http404


    # def get_context_data(self,**kwargs):
    #     context = super(CreatePropriety,self).get_context_data(**kwargs)
    #     context['test'] = 'Luan'
    #
    #     return context



    model = Talhao
    fields = ['talhao','area']


    def get_success_url(self):
        return reverse_lazy('propriety_list')


    def form_valid(self,form):
        talhao = form.save(commit=False)
        talhao.user_cad = self.request.user
        talhao.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())






@login_required
def delete_talhao(request, pk):
    talhao = get_object_or_404(Talhao,pk=pk,user_cad=request.user)
    talhao.delete()
    return HttpResponse('ok')









edit_company = EditCompany.as_view()
create_company =  CreateCompany.as_view()
edit_propriety = EditPropriety.as_view()
create_propriety = CreatePropriety.as_view()
edit_cadgeral = EditCadGeral.as_view()
create_cadgeral = CreateCadGeral.as_view()
edit_ccusto = EditCcusto.as_view()
create_ccusto = CreateCcusto.as_view()
edit_planofinan = EditPlanofinan.as_view()
create_planofinan = CreatePlanoFinan.as_view()
create_talhao = CreateTalhao.as_view()
