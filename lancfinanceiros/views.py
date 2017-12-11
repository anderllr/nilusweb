from datetime import date, timedelta

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from core.utils import add_one_month
from django.http import HttpResponse,Http404
from .forms import FormCreateReceita,FormEditReceita,FiltroLancamentosForm
from accounts.models import User
from nilusadm.models import Sequenciais
from principal.models import Instancia
from lancfinanceiros.models import Lancamentos
from niluscad.models import Company,Propriety,Cadgeral,PlanoFinan,Ccusto
# Create your views here.



@login_required
def lancfin_list(request):

    if request.is_ajax():
        template_name = '_table_lancfin.html'
    else:
        template_name = 'lancfin_list.html'

    if request.user.is_masteruser is True:
        lanctos = Lancamentos.objects.filter(master_user=request.user.pk)
        empresa = Company.objects.filter(master_user=request.user.pk)
        propriedade = Propriety.objects.filter(master_user=request.user.pk)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.pk)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.pk,sinal='R')
        c_custo = Ccusto.objects.filter(master_user=request.user.pk)
        empresa_init = Company.objects.filter(master_user=request.user.pk)
        propriedade_init = Propriety.objects.filter(master_user=request.user.pk)

    else:
        lanctos = Lancamentos.objects.filet(master_user=request.user.user_master)
        empresa = Company.objects.filter(master_user=request.user.user_master)
        propriedade = Propriety.objects.filter(master_user=request.user.user_master)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.user_master, sinal='R')
        c_custo = Ccusto.objects.filter(master_user=request.user.user_master)
        empresa_init = Company.objects.filter(master_user=request.user.user_master)
        propriedade_init = Propriety.objects.filter(master_user=request.user.user_master)

    form = FiltroLancamentosForm(empresa,propriedade,cadgeral,plano_finan,c_custo, request.GET or None)


    if form.is_valid():
        data_venc_ini = form.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_venc_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        propriedade = form.cleaned_data.get('propriedade', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        plano_finan = form.cleaned_data.get('plano_finan', '')
        c_custo = form.cleaned_data.get('c_custo', '')

        if data_venc_ini:
            lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini)

        if data_venc_fim:
            lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim+timedelta(days=1))

        if data_lanc_ini:
            lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini)

        if data_lanc_fim:
            lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim + timedelta(days=1))

        if empresa:
            lanctos = lanctos.filter(company=empresa)

        if propriedade:
            lanctos = lanctos.filter(propriety=propriedade)

        if cadgeral:
            lanctos = lanctos.filter(cadgeral=cadgeral)

        if plano_finan:
            lanctos = lanctos.filter(plr_financeiro=plano_finan)

        if c_custo:
            lanctos = lanctos.filter(c_custo=c_custo)



    context = {
        'lanctos': lanctos,
        'form': form,
        'empresa_init' : empresa_init,
        'propriedade_init' : propriedade_init


    }

    return render(request, template_name, context)






class CreateReceita(LoginRequiredMixin,CreateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_receita.html"]
        else:
            return ["create_receita.html"]

    def get_form_kwargs(self):
        kwargs = super(CreateReceita, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    model = Lancamentos
    form_class = FormCreateReceita

    def get_initial(self):
        initial = super(CreateReceita,self).get_initial()
        initial['company'] = self.request.user.company_p
        initial['propriety'] = self.request.user.propriety_p
        return initial

    def get_success_url(self):
        return reverse_lazy('lancfin_list')


    def form_valid(self,form):
        lancto = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            lancto.master_user = self.request.user
            seq_lanc = Sequenciais.objects.get(user=self.request.user)
        else:
            lancto.master_user = self.request.user.user_master
            seq_lanc = Sequenciais.objects.get(user=self.request.user.user_master)
        lancto.situacao = 'A'
        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.num_lan = seq_lanc.lanc_financeiros + 1
        seq_lanc.lanc_financeiros = lancto.num_lan
        seq_lanc.save()
        lancto.save()

        id_lancto = lancto.pk

        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            tipo_rept = form.cleaned_data['tipo_rept']
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_ = seq_lanc.lanc_financeiros + 1
                    seq_lanc.recebiveis = lancto.num_lan
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'W':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencto = lancto.dt_vencto + timedelta(days=7)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'D':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencto = lancto.dt_vencto + timedelta(days=1)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditReceita(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_receita.html"]
        else:
            return ["edit_receita.html"]

    def get_context_data(self, **kwargs):
        context = super(EditReceita, self).get_context_data(**kwargs)
        context['tem_parcela'] = self.object.verifica_parcela()
        context['dados_titulo'] = Lancamentos.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(EditReceita, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse_lazy('titrec_list')


    model = Lancamentos
    form_class = FormEditReceita



    def form_valid(self, form):
        lancto = form.save(commit=False)
        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.save()
        confirma_parcela = self.request.POST.get('confirma_parcela','N')
        if confirma_parcela == 'S':
            lancto = form.instance
            lancto.altera_parcelas()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




def delete_receita(request, pk):
    if request.user.is_masteruser is True:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user, pk=pk)
        lanctodel.delete()
    else:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user.user_master, pk=pk)
        lanctodel.delete()




    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('lancfin_list')




edit_receita = EditReceita.as_view()
create_receita = CreateReceita.as_view()
