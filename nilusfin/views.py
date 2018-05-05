from datetime import date, timedelta, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,Http404
from decimal import Decimal
from accounts.models import User
from nilusadm.models import Sequenciais
from lancfinanceiros.models import Movtos_lancamentos,Lancamentos
from .models import Contafinanceira,Cotacao,Indice
from niluscad.models import Company,Grupodre,PlanoFinan
from .forms import FormCreateCotacao,FormAjusteSaldo,FiltroLancamentosExtrato,FiltroDre,FormFluxoCaixa
from django.db.models import Sum
from nilusfin.calculos import calc_dre,saldo_conta,lanctos_atraso,lanctos_avencer

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

    try:
        conta.delete()
    except:
        print('erro na exclusao')



    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('conta_list')



class AjusteSaldo(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_ajuste_saldo_conta.html"]
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super(AjusteSaldo, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AjusteSaldo, self).get_context_data(**kwargs)
        context['data_hoje'] = datetime.today
        return context

    model = Movtos_lancamentos
    form_class = FormAjusteSaldo


    def get_initial(self):
        initial = super(AjusteSaldo,self).get_initial()
        initial['company'] = self.request.user.company_p
        return initial

    def get_success_url(self):
        return reverse_lazy('conta_list')


    def form_valid(self,form,**kwargs):
        mvt_ajcsaldo = form.save(commit=False)
        saldo_negativo = form.cleaned_data.get('saldo_negativo', '')

        movtos_creditos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                            conta_financeira=mvt_ajcsaldo.conta_financeira,
                                                            sinal='R',dt_movimento__lte=mvt_ajcsaldo.dt_movimento)
        movtos_creditos = movtos_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))
        movtos_debitos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                           conta_financeira=mvt_ajcsaldo.conta_financeira,
                                                           sinal='D',dt_movimento__lte=mvt_ajcsaldo.dt_movimento)
        movtos_debitos = movtos_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))


        if movtos_debitos['vlr_debitos'] is None:
            movtos_debitos['vlr_debitos'] = 0

        if movtos_creditos['vlr_creditos'] is None:
            movtos_creditos['vlr_creditos'] = 0

        saldo_sistema = movtos_creditos['vlr_creditos'] - movtos_debitos['vlr_debitos']
        vlr_novo_saldo = self.request.POST.get('vlr_novosaldo').replace('.', '').replace(',', '.')

        if saldo_negativo:
            vlr_novo_saldo = Decimal(vlr_novo_saldo) * -1


        if Decimal(vlr_novo_saldo) > Decimal(saldo_sistema):
            vlr_ajuste_saldo = Decimal(vlr_novo_saldo) - Decimal(saldo_sistema)
            sinal = 'R'
        else:
            if saldo_negativo:
                vlr_novo_saldo = Decimal(vlr_novo_saldo) * 1
            vlr_ajuste_saldo = Decimal(saldo_sistema )- Decimal(vlr_novo_saldo)
            sinal = 'D'

        mvt_ajcsaldo.master_user = self.request.user.user_master
        mvt_ajcsaldo.vlr_movimento = vlr_ajuste_saldo
        mvt_ajcsaldo.sinal = sinal
        mvt_ajcsaldo.desc_movimento = 'Ajuste de Saldo'
        mvt_ajcsaldo.tipo_movto = 'A'
        mvt_ajcsaldo.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True,cad_ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



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



class CreateIndice_lancto(LoginRequiredMixin,CreateView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_indice_lancto.html"]
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
            context = self.get_context_data(form=form, success=True,cad_ok='ok')
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

    try:
        indice.delete()
    except:
        print('erro na exclusao')

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
    fields = ['data_indice','valor_cotacao_text']

    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form):
        cotacao = form.save(commit=False)
        cotacao.user_cad = self.request.user
        cotacao.valor_cotacao = cotacao.valor_cotacao_text.replace('R$','').replace('.','').replace(',','.')
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
    fields = ['data_indice', 'valor_cotacao_text']

    def get_success_url(self):
        return reverse_lazy('indice_list')


    def form_valid(self,form):
        cotacao = form.save(commit=False)
        cotacao.user_cad = self.request.user
        cotacao.valor_cotacao = cotacao.valor_cotacao_text.replace('R$','').replace('.','').replace(',','.')

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
        indice_cot = cotacao.indice

        cotacao.valor_cotacao = cotacao.valor_cotacao_text.replace('R$','').replace('.','').replace(',','.')

        cotacao.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True,indice_cot=indice_cot,cad_ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())






@login_required
def delete_cotacao(request, pk):
    cotacao = get_object_or_404(Cotacao,pk=pk)

    try:
        cotacao.delete()
    except:
        print('erro na exclusao')
    # messages.success(request, 'Grupo removido com sucesso !!')
    return HttpResponse('ok')


##########################################################################################
#                               EXTRATOS FINANCEIROS                                     #
##########################################################################################

@login_required
def extrato_contas(request):

    if request.is_ajax():
        template_name = '_extrato_contas.html'
    else:
        template_name = 'extrato_contas.html'

    filtrou = 'nao'
    data_hoje = datetime.today
    dt_saldo_ant = ''
    saldo_anterior = 0
    saldo_atual = 0
    totalizador_cre = 0
    totalizador_deb = 0
    saldo_c_limite = 0



    # movimentos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,tipo_movto='B')
    conta_finan = Contafinanceira.objects.filter(master_user=request.user.user_master)
    empresa = Company.objects.filter(master_user=request.user.user_master)
    lanctos = Movtos_lancamentos.objects.none()
    dados_conta = conta_finan
    form = FiltroLancamentosExtrato(conta_finan,empresa,request.GET or None)



    if form.is_valid():
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_lanc_fim', '')
        conta_finan = form.cleaned_data.get('conta_finan','')
        empresa = form.cleaned_data.get('empresa','')
        dt_saldo_ant = data_lanc_ini - timedelta(days=1)

        if empresa:
            movimentos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master
                                                           ,company=empresa).exclude(tipo_movto='C')
        else:
            movimentos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master).exclude(tipo_movto='C')

        if data_lanc_ini and data_lanc_fim:
            lanctos = movimentos.filter(dt_movimento__range=(data_lanc_ini,data_lanc_fim))


            if conta_finan:
                lanctos = lanctos.filter(conta_financeira=conta_finan)

        lanctos = lanctos.order_by('dt_movimento')

        # SALDO ANTERIOR

        # total creditos
        if empresa:
            movtos_creditos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                                sinal='R', dt_movimento__lt=data_lanc_ini,
                                                                company=empresa).exclude(tipo_movto='C')
        else:
            movtos_creditos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                                sinal='R', dt_movimento__lt=data_lanc_ini,
                                                                ).exclude(tipo_movto='C')
        if conta_finan:
            movtos_creditos = movtos_creditos.filter(conta_financeira=conta_finan)
        movtos_creditos = movtos_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))


        # total debitos
        if empresa:
            movtos_debitos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                               sinal='D', dt_movimento__lt=data_lanc_ini,
                                                               company=empresa).exclude(tipo_movto='C')
        else:
            movtos_debitos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                               sinal='D', dt_movimento__lt=data_lanc_ini,
                                                               ).exclude(tipo_movto='C')
        if conta_finan:
            movtos_debitos = movtos_debitos.filter(conta_financeira=conta_finan)
        movtos_debitos = movtos_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

        if movtos_creditos['vlr_creditos'] is None:
            movtos_creditos['vlr_creditos'] = 0

        if movtos_debitos['vlr_debitos'] is None:
            movtos_debitos['vlr_debitos'] = 0

        saldo_anterior = Decimal(movtos_creditos['vlr_creditos']) - Decimal(movtos_debitos['vlr_debitos'])
        #  FIM SALDO ANTERIOR


        # SALDO ATUAL

        # total creditos
        if empresa:
            movtos_creditos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                                sinal='R', dt_movimento__lte=data_lanc_fim,
                                                                company=empresa).exclude(tipo_movto='C')
        else:
            movtos_creditos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                                sinal='R', dt_movimento__lte=data_lanc_fim)\
                                                                .exclude(tipo_movto='C')

        if conta_finan:
            movtos_creditos = movtos_creditos.filter(conta_financeira=conta_finan)
        movtos_creditos = movtos_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))


        # total debitos
        if empresa:
            movtos_debitos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                               sinal='D', dt_movimento__lte=data_lanc_fim,
                                                               company=empresa).exclude(tipo_movto='C')
        else :
            movtos_debitos = Movtos_lancamentos.objects.filter(master_user=request.user.user_master,
                                                               sinal='D', dt_movimento__lte=data_lanc_fim
                                                               ).exclude(tipo_movto='C')

        if conta_finan:
            movtos_debitos = movtos_debitos.filter(conta_financeira=conta_finan)
        movtos_debitos = movtos_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

        if movtos_creditos['vlr_creditos'] is None:
            movtos_creditos['vlr_creditos'] = 0

        if movtos_debitos['vlr_debitos'] is None:
            movtos_debitos['vlr_debitos'] = 0

        saldo_atual = Decimal(movtos_creditos['vlr_creditos']) - Decimal(movtos_debitos['vlr_debitos'])
        # FIM SALDO ATUAL


        # VALORES DE CRÉDITO E DÉBITO DENTRO DO PERÍODO
        total_debitos = movimentos.filter(dt_movimento__range=(data_lanc_ini,data_lanc_fim),sinal='D')
        if conta_finan:
            total_debitos = total_debitos.filter(conta_financeira=conta_finan)
        total_debitos = total_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

        total_creditos = movimentos.filter(dt_movimento__range=(data_lanc_ini, data_lanc_fim),sinal='R')
        if conta_finan:
            total_creditos = total_creditos.filter(conta_financeira=conta_finan)
        total_creditos = total_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))

        if total_creditos['vlr_creditos'] is None:
            total_creditos['vlr_creditos'] = 0

        if total_debitos['vlr_debitos'] is None:
            total_debitos['vlr_debitos'] = 0


        totalizador_cre = total_creditos['vlr_creditos']
        totalizador_deb = total_debitos['vlr_debitos']
        # FIM VALORES DE CRÉDITO E DÉBITO


        # TRATA LIMITE DA CONTA
        if conta_finan:
            if conta_finan.usa_limite:
                vlr_limite = conta_finan.vlr_limite_text.replace('R$','').replace('.','').replace(',','.')
                saldo_c_limite = Decimal(saldo_atual) + Decimal(vlr_limite)



        # FIM TRATA LIMITE DA CONTA




    context = {
        'saldo_anterior' : saldo_anterior,
        'dt_saldo_ant': dt_saldo_ant,
        'lanctos': lanctos,
        'form': form,
        'filtrou': filtrou,
        'data_hoje' : data_hoje,
        'saldo_atual' : saldo_atual,
        'total_debitos' : totalizador_deb,
        'total_creditos': totalizador_cre,
        'dados_conta' : conta_finan,
        'saldo_c_limite' : saldo_c_limite,
    }

    return render(request, template_name, context)


##########################################################################################
#                                  DRE FINANCEIRA                                        #
##########################################################################################

@login_required
def dre_list(request):
    if request.is_ajax():
        template_name = '_corpo_dre.html'
    else:
        template_name = 'consulta_dre.html'

    data_hoje = datetime.today

    empresa = Company.objects.filter(master_user=request.user.user_master)
    soma_grupodre = None
    valor_plr_finan = None
    saldo_atual = 0
    saldos = []
    retorno_dre = []
    retorno_planosdre = []
    user = request.user

    form = FiltroDre(empresa, request.GET or None)

    if form.is_valid():
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_lanc_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        f_lancamento = form.cleaned_data.get('f_lancamento', '')
        f_vencimento = form.cleaned_data.get('f_vencimento', '')
        f_baixa = form.cleaned_data.get('f_baixa', '')



        retorno_dre,retorno_planosdre,saldos = calc_dre(empresa,f_lancamento,f_vencimento,f_baixa,data_lanc_ini,data_lanc_fim,user)


    context = {
        'form': form,
        'soma_grupodre' : soma_grupodre,
        'valor_plr_finan': valor_plr_finan,
        'saldo_atual' :saldo_atual,
        'saldo_contas_dre' : saldos,
        'retorno_dre' : retorno_dre,
        'retorono_planosdre': retorno_planosdre,
    }

    return render(request, template_name, context)


##########################################################################################
#                                  FLUXO CAIXA                                           #
##########################################################################################



@login_required
def fluxo_caixa(request):
    if request.is_ajax():
        template_name = 'fluxo_caixa.html'
    else:
        template_name = 'fluxo_caixa.html'


    contas = Contafinanceira.objects.filter(master_user=request.user.user_master)
    empresa = Company.objects.filter(master_user=request.user.user_master)
    data_saldo = datetime.now()
    data_hoje = datetime.now()
    usuario = request.user
    contas_pk = []
    saldos = saldo_conta(empresa,contas,data_saldo,usuario)
    saldo_final = None
    rec_atraso_lanc = None
    rec_atraso_tot = None
    desp_atraso_lanc = None
    desp_atraso_tot = None
    rec_tot = None
    desp_tot = None
    fluxo_dia = None
    lanctos = None
    fluxo_gerado = None


    form_fluxo = FormFluxoCaixa(empresa,contas,request.POST or None)

    if form_fluxo.is_valid():
        data_venc_ini = form_fluxo.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form_fluxo.cleaned_data.get('data_venc_fim', '')
        contas =        form_fluxo.cleaned_data.get('contas_financeiras', '')
        empresa =       form_fluxo.cleaned_data.get('empresa', '')
        atrasados =     form_fluxo.cleaned_data.get('considera_atraso','')


        for c in contas:
            contas_pk.append(c.pk)


        rec_atraso_lanc,rec_atraso_tot,desp_atraso_lanc,desp_atraso_tot = lanctos_atraso(empresa,contas_pk,data_venc_ini,usuario)
        rec_tot,desp_tot,fluxo_dia,lanctos,saldo_final = lanctos_avencer(empresa,contas_pk,data_venc_ini,data_venc_fim,usuario)
        fluxo_gerado = 'S'


        if atrasados:
            if rec_atraso_tot['vlr_saldo'] is None:
                 rec_atraso_tot['vlr_saldo'] = 0
            if desp_atraso_tot['vlr_saldo'] is None:
                 rec_atraso_tot['vlr_saldo'] = 0

            saldo_final = Decimal(saldo_final) + (Decimal(rec_atraso_tot['vlr_saldo']) - Decimal(desp_atraso_tot['vlr_saldo']))



    context = {
        'form_fluxo': form_fluxo,
        'fluxo_gerado': fluxo_gerado,
        'saldos' : saldos,
        'data_hoje' : data_hoje,
        'contas' : contas,
        'rec_atraso_lanc' : rec_atraso_lanc,
        'rec_atraso_tot' : rec_atraso_tot,
        'desp_atraso_lanc' : desp_atraso_lanc,
        'desp_atraso_tot' : desp_atraso_tot,
        'rec_tot' : rec_tot,
        'desp_tot': desp_tot,
        'fluxo_dia': fluxo_dia,
        'lanctos' : lanctos,
        'saldo_final' : saldo_final
    }

    return render(request, template_name, context)





create_indice = CreateIndice.as_view()
edit_indice = EditIndice.as_view()
create_conta = CreateConta.as_view()
create_cotacao_create_indice = CreateCotacao_create_indice.as_view()
create_cotacao_edit_indice = CreateCotacao_edit_indice.as_view()
edit_conta = EditConta.as_view()
create_cotacao_grid_indice = CreateCotacao_grid_indice.as_view()
create_indice_lancto = CreateIndice_lancto.as_view()
ajc_saldoconta = AjusteSaldo.as_view()


