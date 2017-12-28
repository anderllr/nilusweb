from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from accounts.models import User
from .forms import FormConfigUsuario
from .models import Permissions

# Create your views here.



@login_required
def users_viewers_list(request):

    if request.is_ajax():
        template_name = '_table_users_viewers.html'
    else:
        template_name = 'users_viewers_list.html'


    users_viewers = User.objects.filter(user_master=request.user)


    context = {
        'users_viewers' : users_viewers,
    }
    return render(request,template_name,context)




class EditPermissions(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_alter_permissions.html"]
        else:
            raise Http404



    model = Permissions
    fields = ['nilusCadastro','nilusFinanceiro','nilusCompras','nilusProducao','nilusMaquinas','nilusFiscalCont']



    def get_success_url(self):
        return reverse_lazy('users_viewers_list')

    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


class ConfiguracaoConta(LoginRequiredMixin, UpdateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_config_conta.html"]
        else:
            raise Http404

    # def get_form_kwargs(self):
    #     kwargs=super(ConfiguracaoConta,self).get_form_kwargs()
    #     kwargs['user']=self.request.user.user_master
    #     return kwargs



    model = User
    # fields = ['company_p','propriety_p']
    form_class = FormConfigUsuario


    def get_object(self):
        return self.request.user


    def get_form_kwargs(self):
        kwargs=super(ConfiguracaoConta,self).get_form_kwargs()
        kwargs['user']=self.request.user
        return kwargs


    def form_valid(self,form):
        form.save()
        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


edit_permissions = EditPermissions.as_view()
config_conta = ConfiguracaoConta.as_view()








