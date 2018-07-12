from django.shortcuts import render, redirect
from django.views.generic import CreateView,UpdateView
from django.contrib.auth.tokens import default_token_generator
from .forms import ForgotPasswordForm
from django.http import HttpResponse,Http404
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.conf import settings


from .models import User
from .forms import UserCustomCreationForm,UserViewerCreationForm

# Create your views here.

class RegisterUser(CreateView):

    model = User
    template_name = 'register.html'
    form_class = UserCustomCreationForm
    success_url = reverse_lazy('success_register')

register = RegisterUser.as_view()



def user_active(request, token):
    user = User.objects.get(token=token)
    user.is_active = True
    # if user.is_masteruser is True:
        # user.user_master = user.pk
    user.save()

    return redirect('signin')



def recover_account(request):
    form = ForgotPasswordForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except:
            user = None
        if user:
            token = default_token_generator.make_token(user)
            from templated_email import send_templated_mail
            send_templated_mail(
                template_name='email_recupera_conta',
                from_email='michel.carvalho22@gmail.com',
                recipient_list=[user.email],
                context = {
                    'domain' : settings.SITE_DOMAIN,
                    'user' : user,
                    'token' : token
                },


            )
            return render(request,template_name='recover_info.html')

    context = {
        'form' : form
    }

    return render(request,'recover_account.html',context)



def create_new_password(request,id,token):
    user = User.objects.get(id=id)
    if default_token_generator.check_token(user,token):
        form = SetPasswordForm(user,request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('signin')
        context = {
            'form' : form
         }
        return render(request,'new_password.html', context)

    raise Http404





def success_register(request):

    return render(request,'success_register.html')




class RegisterUserViewer(LoginRequiredMixin,CreateView):


        def get_template_names(self):
            if self.request.is_ajax():
                return ["_create_viewer.html"]
            else:
                raise Http404

        def get_success_url(self):
            return reverse_lazy('users_viewers_list')

        model = User
        form_class = UserViewerCreationForm




        def form_valid(self, form):
            userv = form.save(commit=False)
            userv.user_master = self.request.user
            if userv.user_master.conta_presente == True:
                userv.conta_presente = True
            userv.is_masteruser = False
            userv.is_active = True
            userv.save()


            if self.request.is_ajax():
                context = self.get_context_data(form=form, ok='ok',success=True)
                return self.render_to_response(context)
            else:
                return redirect(self.get_success_url())


register_viewer = RegisterUserViewer.as_view()



class EditUserViewer(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_alter_viewer.html"]
        else:
           raise Http404

    model = User
    fields = ['name','email','is_active']

    def get_success_url(self):
        return reverse_lazy('users_viewers_list')

    def form_valid(self,form):
        form.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())


edit_viewer = EditUserViewer.as_view()




def reset_password(request,pk):
    form = ForgotPasswordForm(request.POST or None)
    user = User.objects.get(pk=pk)
    if user:
       token = default_token_generator.make_token(user)
       from templated_email import send_templated_mail
       send_templated_mail(
          template_name='email_recupera_conta',
          from_email='michel.carvalho22@gmail.com',
          recipient_list=[user.email],
          context = {
         'domain' : settings.SITE_DOMAIN,
         'user' : user,
         'token' : token
         },


       )
       return redirect('users_viewers_list')

    context = {
        'form' : form
    }

    return render(request,'recover_account.html',context)




