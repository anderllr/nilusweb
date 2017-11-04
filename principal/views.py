from django.shortcuts import render
from django.views.generic import UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse,Http404

from accounts.models import User

# Create your views here.

@login_required
def principal(request):


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


profile = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()



