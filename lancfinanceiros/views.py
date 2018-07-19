
from datetime import date, timedelta, datetime
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from core.utils import add_one_month,lookahead
from django.http import HttpResponse,Http404
from .forms import FormCreateReceita,FormEditReceita,FiltroLancamentosForm,FormCreateDespesa,FormEditDespesa,\
                   FormBaixaLancamento,FiltroLancamentosbaixa,FormBaixaParcial,FormDeletaLancto
from accounts.models import User
from nilusadm.models import Sequenciais
from nilusfin.models import Indice,Cotacao
from principal.models import Instancia
from lancfinanceiros.models import Lancamentos,Movtos_lancamentos
from niluscad.models import Company,Propriety,Cadgeral,PlanoFinan,Ccusto
from nilusfin.models import Contafinanceira
from lancfinanceiros.movto_finan import grava_movimento_financeiro_b,grava_movimento_financeiro_c
# Create your views here.




@login_required
def lancfin_list(request):

    if request.is_ajax():
        template_name = '_table_lancfin.html'
    else:
        template_name = 'lancfin_list.html'

    filtrou = 'nao'
    data_hoje = datetime.today

    if request.user.is_masteruser is True:
        lanctos = Lancamentos.objects.filter(master_user=request.user.pk,situacao = False)
        empresa = Company.objects.filter(master_user=request.user.pk)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.pk)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.pk)
        c_custo = Ccusto.objects.filter(master_user=request.user.pk)
        empresa_init = Company.objects.filter(master_user=request.user.pk)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.pk)

    else:
        lanctos = Lancamentos.objects.filter(master_user=request.user.user_master,sit_lancamento ='A')
        empresa = Company.objects.filter(master_user=request.user.user_master)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.user_master)
        c_custo = Ccusto.objects.filter(master_user=request.user.user_master)
        empresa_init = Company.objects.filter(master_user=request.user.user_master)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.user_master)

    form = FiltroLancamentosForm(empresa,cadgeral,plano_finan,c_custo,conta_finan,  request.GET or None)



    if form.is_valid():
        data_venc_ini = form.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_baix_ini = form.cleaned_data.get('data_baix_ini', '')
        data_baix_fim = form.cleaned_data.get('data_baix_fim', '')
        tipo_lancamento = form.cleaned_data.get('tipo_lancamento', '')
        sit_lancamento = form.cleaned_data.get('sit_lancamento','')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        plano_finan = form.cleaned_data.get('plano_finan', '')
        c_custo = form.cleaned_data.get('c_custo', '')
        conta_finan2 = form.cleaned_data.get('conta_finan','')

        lanctos = Lancamentos.objects.filter(master_user=request.user.user_master)

        if data_venc_ini:
            lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini)
            filtrou = 'ok'

        if data_venc_fim:
            lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim+timedelta(days=1))
            filtrou = 'ok'

        if data_lanc_ini:
            lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini)
            filtrou = 'ok'

        if data_lanc_fim:
            lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim + timedelta(days=1))
            filtrou = 'ok'

        if data_baix_ini:
            lanctos = lanctos.filter(data_baixa__gte=data_baix_ini)
            filtrou = 'ok'

        if data_baix_fim:
            lanctos = lanctos.filter(data_baixa__lt=data_baix_fim + timedelta(days=1))
            filtrou = 'ok'

        if empresa:
            lanctos = lanctos.filter(company=empresa)
            filtrou = 'ok'

        if cadgeral:
            lanctos = lanctos.filter(cadgeral=cadgeral)
            filtrou = 'ok'

        if plano_finan:
            lanctos = lanctos.filter(plr_financeiro=plano_finan)
            filtrou = 'ok'

        if c_custo:
            lanctos = lanctos.filter(c_custo=c_custo)
            filtrou = 'ok'

        if conta_finan2:
            lanctos = lanctos.filter(conta_finan=conta_finan2)
            filtrou = 'ok'

        if tipo_lancamento != 'T':
            lanctos = lanctos.filter(tipo_lancamento=tipo_lancamento)
            filtrou = 'ok'

        if sit_lancamento != 'T':
            if sit_lancamento == 'A':
                lanctos = lanctos.filter(situacao=False)
            elif sit_lancamento == 'B':
                lanctos = lanctos.filter(situacao=True)
            filtrou = 'ok'

    form_baixa = FormBaixaLancamento(lanctos, conta_finan, request.POST or None)
    if form_baixa.is_valid():
        lancto = form_baixa.cleaned_data['lanc_baixa']
        data_baixa = form_baixa.cleaned_data['data_baixa']
        if data_baixa is None:
            data_baixa = datetime.now()
        conta_financeira = form_baixa.cleaned_data['conta_financeira']

        for l in lancto:

            if conta_financeira:
                l.conta_finan = conta_financeira

            l.situacao = True
            l.data_baixa = data_baixa

            grava_movimento_financeiro_b(l, l.situacao, l.saldo,request.user.user_master)
            l.saldo = 0
            l.save()

    context = {
        'lanctos': lanctos,
        'form': form,
        'form_baixa': form_baixa,
        'empresa_init' : empresa_init,
        'filtrou': filtrou,
        'data_hoje' : data_hoje,
    }

    return render(request, template_name, context)








class CreateReceita(LoginRequiredMixin,CreateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_receita.html"]
        else:
            return ["create_receita.html"]

    def get_context_data(self, **kwargs):
        context = super(CreateReceita, self).get_context_data(**kwargs)
        context['data_hoje'] = datetime.today
        return context

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

        if lancto.dt_lancamento is None:
            lancto.dt_lancamento = datetime.now()


        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.num_lan = seq_lanc.lanc_financeiros + 1
        lancto.tipo_lancamento = 'R'

        seq_lanc.lanc_financeiros = lancto.num_lan
        seq_lanc.save()

        if lancto.indice is None:
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master, indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao, cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.saldo = lancto.vlr_lancamento
        else:
            cotacao = lancto.cotacao
            valor_lancamento = lancto.vlr_lancamento
            conta = Decimal(valor_lancamento) * Decimal(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta
            lancto.valor_text = str(round(lancto.vlr_lancamento,2)).replace('.',',')
            lancto.saldo = lancto.vlr_lancamento


        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            valor_parcela = Decimal(lancto.vlr_lancamento) / qtd
            valor_corrigido = Decimal(valor_parcela) * qtd
            arredondamento = Decimal(lancto.vlr_lancamento) - Decimal(valor_corrigido)
            lancto.vlr_lancamento = round(valor_parcela,2)
            lancto.valor_text = str(lancto.vlr_lancamento).replace('.',',')
            lancto.saldo =  lancto.vlr_lancamento

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
            lancto.saldo = 0
        else:
            lancto.data_baixa is None


        lancto.save()

        grava_movimento_financeiro_c(lancto, self.request.user.user_master)

        id_lancto = lancto.pk


        # SE ESTIVER MARCADO PARCELAR
        if form.cleaned_data.get('parcela',False):
            lancamento_pai = Lancamentos.objects.get(pk=id_lancto)
            lancamento_pai.lancamento_pai_id = id_lancto
            lancamento_pai.save()


            qtd = form.cleaned_data['qtd']
            dias_vencto = form.cleaned_data['dias_entre_vencto']
            dia_fixo = form.cleaned_data['dia_fixo']
            for i,has_more in lookahead(range(qtd-1)):
                if arredondamento > 0.00:
                    if has_more == False:
                        lancto.vlr_lancamento = Decimal(lancto.vlr_lancamento) + Decimal(0.01)
                        lancto.saldo = lancto.vlr_lancamento
                lancto.pk = None
                lancto.parcela = lancto.parcela + 1
                lancto.lancamento_pai_id = id_lancto
                if dia_fixo :
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                else:
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=dias_vencto)

                lancto.save()
                grava_movimento_financeiro_c(lancto, self.request.user.user_master)

        # SE ESTIVER SELECIONADA A OPÇÃO REPETIR
        if form.cleaned_data.get('repetir',False):
            lancamento_pai = Lancamentos.objects.get(pk=id_lancto)
            lancamento_pai.lancamento_pai_id = id_lancto
            lancamento_pai.save()

            qtd = form.cleaned_data['qtd_repetir']
            tipo_rept = form.cleaned_data['tipo_rept']
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.dt_lancamento = lancto.dt_vencimento
                    seq_lanc.save()

                    lancto.save()

                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'S':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=7)
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.lancamento_pai_id = id_lancto
                    seq_lanc.save()

                    lancto.save()
                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'D':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=1)
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.lancamento_pai_id = id_lancto
                    seq_lanc.save()

                    lancto.save()
                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'Q':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=15)
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.lancamento_pai_id = id_lancto
                    seq_lanc.save()

                    lancto.save()
                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

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
        context['movimentacoes'] = Movtos_lancamentos.objects.filter(
            lancamento=Lancamentos.objects.get(pk=self.kwargs['pk']))
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
        lancto.vlr_lancamento = lancto.valor_text.replace('R$', '').replace('.', '').replace(',', '.')


        if 'situacao' in form.changed_data:

            if lancto.situacao is True and not lancto.reaberto:
                lancto.data_baixa = datetime.now()

                movto_lanc = Movtos_lancamentos()
                movto_lanc.company = lancto.company
                movto_lanc.master_user = self.request.user.user_master
                movto_lanc.lancamento = lancto
                movto_lanc.dt_movimento = lancto.dt_lancamento
                movto_lanc.vlr_movimento = lancto.saldo
                movto_lanc.desc_movimento = 'Recebido'
                movto_lanc.sinal = 'R'
                movto_lanc.tipo_movto = 'B'
                movto_lanc.save()

                lancto.saldo = 0
                lancto.reaberto = False

            elif lancto.reaberto:
                lancto.situacao = False
                lancto.reaberto = False
                lancto.data_baixa is None
            else:

                lancto.data_baixa is None
                lancto.saldo = lancto.vlr_lancamento
                lancto.data_baixa = None
                movto_lanc = Movtos_lancamentos.objects.filter(lancamento=lancto, tipo_movto='B')
                movto_lanc.delete()
                lancto.reaberto = False

        if 'valor_text' in form.changed_data:

            vlr_movtos_baixas = Movtos_lancamentos.objects.filter(lancamento=lancto, tipo_movto='B').aggregate(
                vlr_movimento=Sum('vlr_movimento'))
            # print(vlr_movtos_baixas['vlr_movimento'])

            if vlr_movtos_baixas['vlr_movimento'] is None:
                vlr_movtos_baixas['vlr_movimento'] = 0

            if vlr_movtos_baixas != 0:
                lancto.saldo = Decimal(lancto.vlr_lancamento) - vlr_movtos_baixas['vlr_movimento']
            else:
                lancto.saldo = lancto.vlr_lancamento

            movto_lanc = Movtos_lancamentos.objects.get(lancamento=lancto, tipo_movto='C')
            movto_lanc.vlr_movimento = lancto.vlr_lancamento
            movto_lanc.save()

        lancto.save()

        confirma_parcela = form.cleaned_data.get('altera_parcelas', 'N')
        if confirma_parcela != 'N':
            lancto = form.instance
            alterado = form.changed_data
            lancto.altera_parcelas(confirma_parcela, alterado)

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



@login_required
def delete_receita(request, pk):
    if request.user.is_masteruser is True:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user, pk=pk)
        lanctodel.delete()
    else:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user.user_master, pk=pk)
        lanctodel.delete()

    return redirect('lancfin_list')


@login_required
def delete_lancto_vinculado(request, pk):

    # if request.is_ajax():
    #     template_name = '_opcoes_delete_lancto.html'
    # else:
    #     raise Http404


    if request.user.is_masteruser is True:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user, pk=pk)
    else:
        lanctodel = get_object_or_404(Lancamentos, master_user=request.user.user_master, pk=pk)


    tipo_baixa = request.GET.get('tipo_delete',None)

    if tipo_baixa == 'N':

        # check_pai = lanctodel
        # print(lanctodel)

        lancamento_pai_id = lanctodel.lancamento_pai_id


        if int(lancamento_pai_id) == int(pk):
            next_pai = Lancamentos.objects.filter(lancamento_pai=lanctodel.lancamento_pai).exclude(pk = lanctodel.pk).first()
            if next_pai:
                lanctos = Lancamentos.objects.filter(lancamento_pai=lanctodel.lancamento_pai)
                lanctos.update(lancamento_pai_id=int(next_pai.pk))

        lanctodel.delete()

    elif tipo_baixa == 'P':
        deletar = Lancamentos.objects.filter(lancamento_pai=lanctodel.lancamento_pai,situacao=False)
        deletar.delete()


    elif tipo_baixa == 'T':
        deletar = Lancamentos.objects.filter(lancamento_pai=lanctodel.lancamento_pai)
        deletar.delete()

    return redirect('lancfin_list')



class DeleteLanctoVinculo(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_opcoes_delete_lancto.html"]
        else:
            raise Http404

        def get_success_url(self):
          return reverse_lazy('titrec_list')

    model = Lancamentos
    form_class = FormDeletaLancto





    def form_valid(self, form):
        tipo_baixa = form.cleand_data.get['delete_parcelas']
        # if tipo_baixa == 'N':
        #     lanctodel.delete()
        # if tipo_baixa == 'P':
        #     deletar = Lancamentos.objects.filter(lancamento_pai=lanctodel, situacao=False)
        #     deletar.delete()
        # if tipo_baixa == 'T':
        #     deletar = Lancamentos.objects.filter(lancamento_pai=lanctodel)
        #     deletar.delete()


        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())





# DESPESAS


class CreateDespesa(LoginRequiredMixin,CreateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_despesa.html"]
        else:
            raise Http404


    def get_context_data(self, **kwargs):
        context = super(CreateDespesa, self).get_context_data(**kwargs)
        context['data_hoje'] = datetime.today
        return context

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

        lancto.vlr_lancamento = lancto.valor_text.replace('R$','').replace('.','').replace(',','.')
        lancto.num_lan = seq_lanc.lanc_financeiros + 1
        lancto.tipo_lancamento = 'D'

        seq_lanc.lanc_financeiros = lancto.num_lan
        seq_lanc.save()


        if lancto.indice is None:
            indice_padrao = Indice.objects.get(master_user=self.request.user.user_master, indice_padrao=True)
            cotacao_padrao = Cotacao.objects.get(indice=indice_padrao, cotacao_padrao=True)
            lancto.indice = indice_padrao
            lancto.cotacao = cotacao_padrao
            lancto.saldo = lancto.vlr_lancamento
        else:
            cotacao = lancto.cotacao
            valor_lancamento = lancto.vlr_lancamento
            conta = Decimal(valor_lancamento) * Decimal(cotacao.valor_cotacao)
            lancto.vlr_lancamento = conta
            lancto.valor_text =str(round(lancto.vlr_lancamento,2)).replace('.',',')
            lancto.saldo = lancto.vlr_lancamento



        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            valor_parcela = Decimal(lancto.vlr_lancamento) / qtd
            valor_corrigido = Decimal(valor_parcela) * qtd
            arredondamento = Decimal(lancto.vlr_lancamento) - Decimal(valor_corrigido)
            lancto.vlr_lancamento = round(valor_parcela,2)
            lancto.valor_text = str(lancto.vlr_lancamento).replace('.',',')
            lancto.saldo = lancto.vlr_lancamento

        if lancto.situacao is True:
            lancto.data_baixa = datetime.now()
            lancto.saldo = 0
        else:
            lancto.data_baixa is None


        lancto.save()

        grava_movimento_financeiro_c(lancto, self.request.user.user_master)

        id_lancto = lancto.pk

        # SELECIONADO PARCELA
        if form.cleaned_data.get('parcela',False):
            lancamento_pai = Lancamentos.objects.get(pk=id_lancto)
            lancamento_pai.lancamento_pai_id = id_lancto
            lancamento_pai.save()

            qtd = form.cleaned_data['qtd']
            dias_vencto = form.cleaned_data['dias_entre_vencto']
            dia_fixo = form.cleaned_data['dia_fixo']
            for i,has_more in lookahead(range(qtd-1)):
                if arredondamento > 0.00:
                    if has_more == False:
                        lancto.vlr_lancamento = Decimal(lancto.vlr_lancamento) + Decimal(0.01)
                        lancto.saldo = lancto.vlr_lancamento
                lancto.pk = None
                lancto.parcela = lancto.parcela + 1
                lancto.lancamento_pai_id = id_lancto
                if dia_fixo :
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                else:
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=dias_vencto)
                lancto.save()

                grava_movimento_financeiro_c(lancto, self.request.user.user_master)

        # SELECIONADA A OPÇÃO DE REPETIR
        if form.cleaned_data.get('repetir',False):
            lancamento_pai = Lancamentos.objects.get(pk=id_lancto)
            lancamento_pai.lancamento_pai_id = id_lancto
            lancamento_pai.save()

            qtd = form.cleaned_data['qtd_repetir']
            tipo_rept = form.cleaned_data['tipo_rept']
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = add_one_month(lancto.dt_vencimento)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.dt_lancamento = lancto.dt_vencimento
                    seq_lanc.save()
                    lancto.save()

                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'S':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=7)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.save()
                    seq_lanc.save()

                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'D':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    seq_lanc.lanc_financeiros = lancto.num_lan
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=1)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.save()
                    seq_lanc.save()

                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

            if tipo_rept == 'Q':
                for i in range(qtd-1):
                    lancto.pk = None
                    lancto.num_lan = seq_lanc.lanc_financeiros + 1
                    lancto.dt_vencimento = lancto.dt_vencimento + timedelta(days=15)
                    lancto.lancamento_pai_id = id_lancto
                    lancto.dt_lancamento = lancto.dt_vencimento
                    lancto.save()
                    seq_lanc.save()

                    grava_movimento_financeiro_c(lancto, self.request.user.user_master)

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
        context['movimentacoes'] = Movtos_lancamentos.objects.filter(lancamento=Lancamentos.objects.get(pk=self.kwargs['pk']))
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

        # if lancto.indice is None and not lancto.situacao:
        #     indice_padrao = Indice.objects.get(master_user=self.request.user.user_master, indice_padrao=True)
        #     cotacao_padrao = Cotacao.objects.get(indice=indice_padrao, cotacao_padrao=True)
        #     lancto.indice = indice_padrao
        #     lancto.cotacao = cotacao_padrao
        #     if not lancto.situacao:
        #         lancto.saldo = lancto.vlr_lancamento
        # else:
        #     cotacao = lancto.cotacao
        #     valor_lancamento = lancto.vlr_lancamento
        #     conta = Decimal(valor_lancamento) * Decimal(cotacao.valor_cotacao)
        #     lancto.vlr_lancamento = conta
        #     lancto.valor_text =str(round(lancto.vlr_lancamento,2)).replace('.',',')
        #     if not lancto.situacao:
        #         lancto.saldo = lancto.vlr_lancamento





        if 'situacao' in form.changed_data:

            if lancto.situacao is True and not lancto.reaberto:
                lancto.data_baixa = datetime.now()

                movto_lanc = Movtos_lancamentos()
                movto_lanc.master_user = self.request.user.user_master
                movto_lanc.company = lancto.company
                movto_lanc.lancamento = lancto
                movto_lanc.dt_movimento = lancto.dt_lancamento
                movto_lanc.vlr_movimento = lancto.saldo
                movto_lanc.desc_movimento = 'Pago'
                movto_lanc.sinal = 'D'
                movto_lanc.tipo_movto = 'B'
                movto_lanc.save()

                lancto.saldo = 0
                lancto.reaberto = False

            elif lancto.reaberto:
                lancto.situacao = False
                lancto.reaberto = False
                lancto.data_baixa is None
            else:

                lancto.data_baixa is None
                lancto.saldo = lancto.vlr_lancamento
                lancto.data_baixa = None
                movto_lanc = Movtos_lancamentos.objects.filter(lancamento=lancto, tipo_movto='B')
                movto_lanc.delete()
                lancto.reaberto = False



        if 'valor_text' in form.changed_data:

            vlr_movtos_baixas = Movtos_lancamentos.objects.filter(lancamento=lancto,tipo_movto='B').aggregate(vlr_movimento=Sum('vlr_movimento'))


            if vlr_movtos_baixas != 0:
                lancto.saldo = Decimal(lancto.vlr_lancamento) - vlr_movtos_baixas['vlr_movimento']
            else:
                lancto.saldo = lancto.vlr_lancamento

            movto_lanc = Movtos_lancamentos.objects.get(lancamento=lancto, tipo_movto='C')
            movto_lanc.vlr_movimento = lancto.vlr_lancamento
            movto_lanc.save()

        lancto.save()

        confirma_parcela = form.cleaned_data.get('altera_parcelas', 'N')
        if confirma_parcela != 'N':
            lancto = form.instance
            alterado = form.changed_data
            lancto.altera_parcelas(confirma_parcela, alterado)


        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())






########################################################################################################################
#                                BAIXAS DE LANCAMENTOS                                                                 #
########################################################################################################################

@login_required
def baixfin_list(request):

    if request.is_ajax():
        template_name = '_table_lancfin.html'
    else:
        template_name = 'baixfin_list.html'



    filtrou = 'nao'

    if request.user.is_masteruser is True:
        lanctos = Lancamentos.objects.filter(master_user=request.user.pk,situacao=False)
        empresa = Company.objects.filter(master_user=request.user.pk)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.pk)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.pk)
        c_custo = Ccusto.objects.filter(master_user=request.user.pk)
        empresa_init = Company.objects.filter(master_user=request.user.pk)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.pk)

    else:
        lanctos = Lancamentos.objects.filter(master_user=request.user.user_master,situacao=False)
        empresa = Company.objects.filter(master_user=request.user.user_master)
        cadgeral = Cadgeral.objects.filter(master_user=request.user.user_master)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.user_master)
        c_custo = Ccusto.objects.filter(master_user=request.user.user_master)
        empresa_init = Company.objects.filter(master_user=request.user.user_master)
        conta_finan = Contafinanceira.objects.filter(master_user=request.user.user_master)

    form = FiltroLancamentosbaixa(empresa,cadgeral,plano_finan,c_custo,conta_finan, request.GET or None)

    if form.is_valid():
        data_venc_ini = form.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_baix_ini = form.cleaned_data.get('data_baix_ini', '')
        data_baix_fim = form.cleaned_data.get('data_baix_fim', '')
        tipo_lancamento = form.cleaned_data.get('tipo_lancamento','')
        empresa = form.cleaned_data.get('empresa', '')
        cadgeral = form.cleaned_data.get('cadgeral', '')
        plano_finan = form.cleaned_data.get('plano_finan', '')
        c_custo = form.cleaned_data.get('c_custo', '')
        conta_finan = form.cleaned_data.get('conta_finan','')

        if data_venc_ini:
            lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini)
            filtrou = 'ok'

        if data_venc_fim:
            lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim+timedelta(days=1))
            filtrou = 'ok'

        if data_lanc_ini:
            lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini)
            filtrou = 'ok'

        if data_lanc_fim:
            lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim + timedelta(days=1))
            filtrou = 'ok'

        if data_baix_ini:
            lanctos = lanctos.filter(data_baixa__gte=data_baix_ini)
            filtrou = 'ok'

        if data_baix_fim:
            lanctos = lanctos.filter(data_baixa__lt=data_baix_fim + timedelta(days=1))
            filtrou = 'ok'

        if tipo_lancamento != 'T':
            lanctos = lanctos.filter(tipo_lancamento=tipo_lancamento)
            filtrou = 'ok'


        if empresa:
            lanctos = lanctos.filter(company=empresa)
            filtrou = 'ok'

        if cadgeral:
            lanctos = lanctos.filter(cadgeral=cadgeral)
            filtrou = 'ok'

        if plano_finan:
            lanctos = lanctos.filter(plr_financeiro=plano_finan)
            filtrou = 'ok'

        if c_custo:
            lanctos = lanctos.filter(c_custo=c_custo)
            filtrou = 'ok'

        if conta_finan:
            lanctos = lanctos.filter(conta_finan=conta_finan)
            filtrou = 'ok'

    form_baixa = FormBaixaLancamento(lanctos,request.POST or None)
    if form_baixa.is_valid():
        lancto = form_baixa.cleaned_data['lanc_baixa']
        data_baixa = form_baixa.cleaned_data['data_baixa']
        if data_baixa is None:
            data_baixa = datetime.now()
        conta_financeira = form_baixa.cleaned_data['conta_financeira']

        for l in lancto:

            if conta_financeira:
                l.conta_finan = conta_financeira

            l.situacao = True
            l.data_baixa = data_baixa

            grava_movimento_financeiro_b(l, l.situacao, l.saldo,request.user.user_master)

            l.saldo = 0
            l.save()



    context = {
        'lanctos': lanctos,
        'form': form,
        # 'form_baixa': form_baixa,
        'filtrou': filtrou,
        'empresa_init' : empresa_init,
    }

    return render(request, template_name, context)



class BaixaParcial(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_baixa_parcial.html"]
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(BaixaParcial, self).get_context_data(**kwargs)
        # context['tem_parcela'] = self.object.verifica_parcela()
        context['dados_titulo'] = Lancamentos.objects.get(pk=self.kwargs['pk'])
        context['data_hoje'] = datetime.today
        return context

    def get_form_kwargs(self):
        kwargs = super(BaixaParcial, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse_lazy('titrec_list')


    model = Lancamentos
    form_class = FormBaixaParcial

    def form_valid(self, form):
        lancto = form.save(commit=False)
        valor_baixa = self.request.POST.get('valor_baixar').replace('.', '').replace(',', '.')
        baixar_totalmente = form.cleaned_data.get('baixa_total', '')
        diferenca = Decimal(lancto.saldo) - Decimal(valor_baixa)
        lancto.saldo = diferenca

        if diferenca == 0:
            lancto.situacao = True

        if baixar_totalmente is True:
            lancto.situacao = True
            lancto.saldo = 0
            lancto.vlr_lancamento = valor_baixa
            lancto.valor_text = valor_baixa
            vlr_movtos_baixas = Movtos_lancamentos.objects.filter(lancamento=lancto).exclude(tipo_movto='C').aggregate(
                                                                             vlr_movimento=Sum('vlr_movimento'))
            if vlr_movtos_baixas['vlr_movimento'] is None:
                vlr_movtos_baixas['vlr_movimento'] = 0

            if baixar_totalmente:
                valor_baixa = Decimal(valor_baixa)
            else:
                valor_baixa = Decimal(valor_baixa) - vlr_movtos_baixas['vlr_movimento']

            movto_lanc = Movtos_lancamentos.objects.get(lancamento=lancto, tipo_movto='C')
            movto_lanc.vlr_movimento = lancto.vlr_lancamento
            movto_lanc.save()



        grava_movimento_financeiro_b(lancto,lancto.situacao,valor_baixa,self.request.user.user_master)

        if diferenca != 0:
            lancto.data_baixa = None


        lancto.save()


        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True, ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



@login_required
def infoLanctos(request,pk):

    if request.is_ajax():
        template_name = '_info_lancto.html'
    else:
        raise Http404

    lancto = Lancamentos.objects.get(pk=pk)
    movimentacoes = Movtos_lancamentos.objects.filter(lancamento=lancto)

    context = {
        'lancto': lancto,
        'movimentacoes' : movimentacoes,
    }

    return render(request, template_name, context)





@login_required
def exclui_movimentacao(request,pk):

    movtodel = Movtos_lancamentos.objects.get(pk=pk)
    lancto = Lancamentos.objects.get(pk=movtodel.lancamento.pk)

    saldo = lancto.saldo
    novo_saldo = saldo + movtodel.vlr_movimento

    movtodel.delete()
    lancto.saldo = novo_saldo
    if lancto.situacao is True:
        lancto.situacao = False
        lancto.reaberto = True
    lancto.save()



    return HttpResponse('ok')


edit_despesa = EditDespesa.as_view()
edit_receita = EditReceita.as_view()
create_receita = CreateReceita.as_view()
create_despesa = CreateDespesa.as_view()
baixa_parcial = BaixaParcial.as_view()
# delete_lancto_vinculado = DeleteLanctoVinculo.as_view()