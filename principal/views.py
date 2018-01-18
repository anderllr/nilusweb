from django.shortcuts import render,get_object_or_404
from django.views.generic import UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse,Http404

from accounts.models import User
from .models import Instancia
from niluscad.models import Company,Propriety
from nilusfin.models import Indice,Cotacao

# Create your views here.

@login_required
def principal(request):


   # dados_usuario = User.objects.get(user=request.user)

   dados_instancia = Instancia.objects.filter(user=request.user)

   if dados_instancia:
      dados_instancia = Instancia.objects.get(user=request.user)
      dados_instancia.company = request.user.company_p
      dados_instancia.propriety = request.user.propriety_p
      dados_instancia.save()




   return render(request,'principal.html')


class UpdateUserView(LoginRequiredMixin, UpdateView):
   model = User
   template_name = 'profile.html'
   fields = ['name', 'email', 'tel_user', 'img_user']

   def get_success_url(self):
      messages.success(self.request, 'Cadastro Atualizado com sucesso')
      return reverse_lazy('profile')

   def get_object(self):
      return self.request.user







class UpdatePasswordView(LoginRequiredMixin, FormView):

   def get_template_names(self):
      if self.request.is_ajax():
         return ["_altera_senha.html"]
      else:
         raise Http404

   form_class = PasswordChangeForm

   def get_success_url(self):
      messages.success(self.request, 'Senha Atualizada com sucesso')

      return reverse_lazy('profile')

   def get_form_kwargs(self):
      kwargs = super(UpdatePasswordView, self).get_form_kwargs()
      kwargs['user'] = self.request.user
      return kwargs

   def form_valid(self, form):
      form.save()
      update_session_auth_hash(self.request, form.user)
      if self.request.is_ajax():
         context = self.get_context_data(form=form, success=True)
         return self.render_to_response(context)
      else:
         return super(UpdatePasswordView, self).form_valid(form)


@login_required
def company_propriety(request):

    company_id = request.GET.get('company_id',None)
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        propriety = Propriety.objects.filter(company = company)
        context = {'company' : company, 'propriety': propriety}
        return render(request,'_select_propriety.html',context)
    raise Http404



@login_required
def indice_cotacao(request):

   indice_id = request.GET.get('indice_id',None)
   if indice_id:
      indice = get_object_or_404(Indice,pk=indice_id)
      cotacao = Cotacao.objects.filter(indice=indice).order_by('-data_indice')
      context = {'indice' : indice, 'cotacao' : cotacao}
      return render(request,'_select_cotacao.html',context)
   raise Http404



profile = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()



