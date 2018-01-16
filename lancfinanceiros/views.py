from datetime import date, timedelta, datetime
import decimal
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from core.utils import add_one_month
from django.http import HttpResponse,Http404
from .forms import FormCreateReceita,FormEditReceita,FiltroLancamentosForm,FormCreateDespesa,FormEditDespesa,FormBaixaLancamento
from accounts.models import User
from nilusadm.models import Sequenciais
from nilusfin.models import Indice,Cotacao
from principal.models import Instancia
from lancfinanceiros.models import Lancamentos
from niluscad.models import Company,Propriety,Cadgeral,PlanoFinan,Ccusto
from nilusfin.models import Contafinanceira
# Create your views here.




@login_required
def lancfin_list(request):

    if request.is_ajax():
        template_name = '_table_lancfin.html'
    else:
        template_name = 'lancfin_list.html'


    form_baixa = FormBaixaLancamento(request.POST or None)
    if form_baixa.is_valid():
        lancto = form_baixa.cleaned_data['lanc_baixa']
        data_baixa = form_baixa.cleaned_data['data_baixa']

        lancto.update(situacao=True,data_baixa=data_baixa)


    if request.user.is_masteruser is True:
        lanctos = Lancamentos.objects.filter(master_user=request.user.pk)
        empresa = Company.objects.filter(master_user=request.user.pk)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.pk)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.pk)
        c_custo = Ccusto.objects.filter(master_user=request.user.pk)
        empresa_init = Company.objects.filter(master_user=request.user.pk)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.pk)

    else:
        lanctos = Lancamentos.objects.filet(master_user=request.user.user_master)
        empresa = Company.objects.filter(master_user=request.user.user_master)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.user_master)
        c_custo = Ccusto.objects.filter(master_user=request.user.user_master)
        empresa_init = Company.objects.filter(master_user=request.user.user_master)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.user_master)

    form = FiltroLancamentosForm(empresa,cadgeral,plano_finan,c_custo,conta_finan, request.GET or None)

    if form.is_valid():
        data_venc_ini = form.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_baix_ini = form.cleaned_data.get('data_baix_ini', '')
        data_baix_fim = form.cleaned_data.get('data_baix_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        plano_finan = form.cleaned_data.get('plano_finan', '')
        c_custo = form.cleaned_data.get('c_custo', '')
        conta_finan = form.cleaned_data.get('conta_finan','')

        if data_venc_ini:
            lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini)

        if data_venc_fim:
            lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim+timedelta(days=1))

        if data_lanc_ini:
            lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini)

        if data_lanc_fim:
            lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim + timedelta(days=1))

        if data_baix_ini:
            lanctos = lanctos.filter(data_baixa__gte=data_baix_ini)

        if data_baix_fim:
            lanctos = lanctos.filter(data_baixa__lt=data_baix_fim + timedelta(days=1))

        if empresa:
            lanctos = lanctos.filter(company=empresa)

        if cadgeral:
            lanctos = lanctos.filter(cadgeral=cadgeral)

        if plano_finan:
            lanctos = lanctos.filter(plr_financeiro=plano_finan)

        if c_custo:
            lanctos = lanctos.filter(c_custo=c_custo)

        if conta_finan:
            lanctos = lanctos.filter(conta_finan=conta_finan)

    context = {
        'lanctos': lanctos,
        'form': form,
        'empresa_init' : empresa_init,
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

        if lancto.dt_vencimento is None:
            lancto.dt_vencimento = datetime.now()

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
        else:
            lancto.data_baixa is None

        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.num_lan = seq_lanc.lanc_financeiros + 1
        lancto.tipo_lancamento = 'R'

        seq_lanc.lanc_financeiros = lancto.num_lan
        seq_lanc.save()

        if lancto.indice is None :
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master,indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao,cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.valor_original = lancto.vlr_lancamento
        else:
            lancto.valor_original = lancto.vlr_lancamento
            cotacao = lancto.cotacao
            valor_lancamento = lancto.valor_original
            conta = float(valor_lancamento) * float(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta

        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            valor_original = lancto.vlr_lancamento
            valor_parcela = float(lancto.vlr_lancamento) / qtd
            lancto.vlr_lancamento = round(valor_parcela,2)
            lancto.valor_text = str(lancto.vlr_lancamento).replace('.',',')

        lancto.save()

        id_lancto = lancto.pk

        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            dias_vencto = form.cleaned_data['dias_entre_vencto']
            dia_fixo = form.cleaned_data['dia_fixo']
            for i in range(qtd-1):
                lancto.pk = None
                lancto.parcela = lancto.parcela + 1
                lancto.lancamento_pai_id = id_lancto
                if dia_fixo :
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                else:
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=dias_vencto)
                lancto.save()


        if form.cleaned_data.get('repetir',False):
            qtd = form.cleaned_data['qtd_repetir']
            tipo_rept = form.cleaned_data['tipo_rept']
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                    lancto.lancamento_pai_id = id_lancto
                    seq_lanc.save()
                    lancto.save()
            if tipo_rept == 'S':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=7)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'D':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=1)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'Q':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=15)
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

        if lancto.indice is None:
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master, indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao, cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.valor_original = lancto.vlr_lancamento
        else:
            lancto.valor_original = lancto.vlr_lancamento
            cotacao = lancto.cotacao
            valor_lancamento = lancto.valor_original
            conta = float(valor_lancamento) * float(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
        else:
            lancto.data_baixa is None


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



# DESPESAS


class CreateDespesa(LoginRequiredMixin,CreateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_despesa.html"]
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(CreateDespesa, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    model = Lancamentos
    form_class = FormCreateDespesa

    def get_initial(self):
        initial = super(CreateDespesa,self).get_initial()
        initial['company'] = self.request.user.company_p
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


        if lancto.dt_vencimento is None:
            lancto.dt_vencimento = datetime.now()

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
        else:
            lancto.data_baixa is None

        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.num_lan = seq_lanc.lanc_financeiros + 1
        lancto.tipo_lancamento = 'D'

        seq_lanc.lanc_financeiros = lancto.num_lan
        seq_lanc.save()

        if lancto.indice is None :
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master,indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao,cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.valor_original = lancto.vlr_lancamento
        else:
            lancto.valor_original = lancto.vlr_lancamento
            cotacao = lancto.cotacao
            valor_lancamento = lancto.valor_original
            conta = float(valor_lancamento) * float(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta




        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            valor_original = lancto.vlr_lancamento
            valor_parcela = float(lancto.vlr_lancamento) / qtd
            lancto.vlr_lancamento = round(valor_parcela,2)
            lancto.valor_text = str(lancto.vlr_lancamento).replace('.',',')

        lancto.save()

        id_lancto = lancto.pk

        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            dias_vencto = form.cleaned_data['dias_entre_vencto']
            dia_fixo = form.cleaned_data['dia_fixo']
            for i in range(qtd-1):
                lancto.pk = None
                lancto.parcela = lancto.parcela + 1
                lancto.lancamento_pai_id = id_lancto
                if dia_fixo :
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                else:
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=dias_vencto)
                lancto.save()


        if form.cleaned_data.get('repetir',False):
            qtd = form.cleaned_data['qtd_repetir']
            tipo_rept = form.cleaned_data['tipo_rept']
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                    lancto.lancamento_pai_id = id_lancto
                    seq_lanc.save()
                    lancto.save()
            if tipo_rept == 'S':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=7)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'D':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=1)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()
            if tipo_rept == 'Q':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=15)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.save()
                    seq_lanc.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditDespesa(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_despesa.html"]
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(EditDespesa, self).get_context_data(**kwargs)
        context['tem_parcela'] = self.object.verifica_parcela()
        context['dados_titulo'] = Lancamentos.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(EditDespesa, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse_lazy('titrec_list')


    model = Lancamentos
    form_class = FormEditDespesa



    def form_valid(self, form):
        lancto = form.save(commit=False)
        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')

        if lancto.indice is None:
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master, indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao, cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.valor_original = lancto.vlr_lancamento
        else:
            lancto.valor_original = lancto.vlr_lancamento
            cotacao = lancto.cotacao
            valor_lancamento = lancto.valor_original
            conta = float(valor_lancamento) * float(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
        else:
            lancto.data_baixa is None


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







edit_despesa = EditDespesa.as_view()
edit_receita = EditReceita.as_view()
create_receita = CreateReceita.as_view()
create_despesa = CreateDespesa.as_view()