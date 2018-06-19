from django.shortcuts import render
from django.utils.dateparse import parse_date
from lancfinanceiros.models import Lancamentos,Movtos_lancamentos
from niluscad.models import Cadgeral,PlanoFinan,Ccusto,Company
from nilusfin.models import Contafinanceira
from niluscont.models import OrdemServico
from django.http import HttpResponse,Http404
from datetime import date, timedelta, datetime
from django.db.models import Sum
from decimal import Decimal
from nilusfin.calculos import calc_dre
from accounts.models import User
from django.contrib.auth.decorators import login_required
from easy_pdf.views import PDFTemplateView
from django.contrib.auth.mixins import LoginRequiredMixin





class Rel_lanfinanceiros(LoginRequiredMixin,PDFTemplateView):
    template_name = 'rel_lanfinanceiros.html'


    def get_context_data(self, **kwargs):
        context = super(Rel_lanfinanceiros, self).get_context_data(**kwargs)
        lanctos = Lancamentos.objects.filter(master_user=self.request.user.pk)
        data_lanc_ini = self.request.GET.get('data_lanc_ini', '')
        data_lanc_fim = self.request.GET.get('data_lanc_fim', '')
        data_venc_ini = self.request.GET.get('data_venc_ini', '')
        data_venc_fim = self.request.GET.get('data_venc_fim', '')
        data_baix_ini = self.request.GET.get('data_baix_ini', '')
        data_baix_fim = self.request.GET.get('data_baix_fim', '')
        cadgeral = self.request.GET.get('cadgeral','')
        plano_finan = self.request.GET.get('plano_finan','')
        c_custo = self.request.GET.get('c_custo','')
        conta_finan = self.request.GET.get('conta_finan','')
        tipo_lancamento = self.request.GET.get('tipo_lancamento','T')
        sit_lancamento = self.request.GET.get('sit_lancamento','T')

        cadgeral_text = None
        plano_finan_text = None
        c_custo_text = None
        conta_finan_text = None

        if cadgeral:
            cadgeral_text = Cadgeral.objects.get(pk=int(cadgeral))
        if plano_finan:
            plano_finan_text = PlanoFinan.objects.get(pk=int(plano_finan))
        if c_custo:
            c_custo_text = Ccusto.objects.get(pk=int(c_custo))
        if conta_finan:
            conta_finan_text =  Contafinanceira.objects.get(pk=int(conta_finan))


        if data_venc_ini != '':
            data_venc_ini_dt = datetime.strptime(data_venc_ini, "%d/%m/%Y").date()
            lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini_dt)

        if data_venc_fim != '':
            data_venc_fim_dt = datetime.strptime(data_venc_fim, "%d/%m/%Y").date()
            lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim_dt + timedelta(days=1))

        if data_lanc_ini != '':
            data_lanc_ini_dt = datetime.strptime(data_lanc_ini, "%d/%m/%Y").date()
            lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini_dt)

        if data_lanc_fim != '':
            data_lanc_fim_dt = datetime.strptime(data_lanc_fim, "%d/%m/%Y").date()
            lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim_dt + timedelta(days=1))

        if data_baix_ini != '':
            data_baix_ini_dt = datetime.strptime(data_baix_ini, "%d/%m/%Y").date()
            lanctos = lanctos.filter(data_baixa__gte=data_baix_ini_dt)

        if data_baix_fim != '':
            data_baix_fim_dt = datetime.strptime(data_baix_fim, "%d/%m/%Y").date()
            lanctos = lanctos.filter(data_baixa__lt=data_baix_fim_dt + timedelta(days=1))

            # if empresa:
            #     lanctos = lanctos.filter(company=empresa)
            #     filtrou = 'ok'

        if cadgeral != '':
            lanctos = lanctos.filter(cadgeral=cadgeral)

        if plano_finan != '':
            lanctos = lanctos.filter(plr_financeiro=plano_finan)

        if c_custo != '':
            lanctos = lanctos.filter(c_custo=c_custo)

        if conta_finan != '':
            lanctos = lanctos.filter(conta_finan=conta_finan)

        if tipo_lancamento != 'T':
            lanctos = lanctos.filter(tipo_lancamento=tipo_lancamento)

        if sit_lancamento != 'T':
            if sit_lancamento == 'A':
                lanctos = lanctos.filter(situacao=False)
            elif sit_lancamento == 'B':
                lanctos = lanctos.filter(situacao=True)

        soma_lanctos_saldo = lanctos.aggregate(
            vlr_saldo=Sum('saldo'))

        soma_lanctos_vlr = lanctos.aggregate(vlr_lancto=Sum('vlr_lancamento'))

        context['lanctos'] = lanctos
        context['data_venc_ini'] = data_venc_ini
        context['data_venc_fim'] = data_venc_fim
        context['data_lanc_ini'] =  data_lanc_ini
        context['data_lanc_fim'] =  data_lanc_fim
        context['data_baix_ini'] = data_baix_ini
        context['data_baix_fim'] = data_baix_fim
        context['cadgeral'] =  cadgeral_text
        context['plano_finan'] =  plano_finan_text
        context['c_custo'] = c_custo_text
        context['conta_finan'] = conta_finan_text
        context['tipo_lancamento'] = tipo_lancamento
        context['sit_lancamento'] = sit_lancamento
        context['soma_saldo'] = soma_lanctos_saldo
        context['soma_vlr_lanctos'] = soma_lanctos_vlr
        return context

class Rel_Extratofinanceiro(LoginRequiredMixin,PDFTemplateView):
    template_name = 'rel_extratofinanceiro.html'


    def get_context_data(self, **kwargs):
        context = super(Rel_Extratofinanceiro, self).get_context_data(**kwargs)
        # lanctos = Movtos_lancamentos.objects.filter(master_user=self.request.user.pk,tipo_movto='B')
        data_lanc_ini = self.request.GET.get('data_lanc_ini', '')
        data_lanc_fim = self.request.GET.get('data_lanc_fim', '')
        conta_finan = self.request.GET.get('conta_finan','')
        empresa = self.request.GET.get('empresa','')


        conta_finan_text = None
        dados_empresa = None
        dt_saldo_ant = None
        saldo_atual = 0
        saldo_anterior = 0
        totalizador_cre = 0
        totalizador_deb = 0
        saldo_c_limite = 0


        if data_lanc_ini != '':
            data_lanc_ini_dt = datetime.strptime(data_lanc_ini, "%d/%m/%Y").date()

        if data_lanc_fim != '':
            data_lanc_fim_dt = datetime.strptime(data_lanc_fim, "%d/%m/%Y").date()

        if conta_finan:
            conta_finan_text = Contafinanceira.objects.get(pk=int(conta_finan))

        if empresa :
            dados_empresa = Company.objects.get(pk=int(empresa))


        if empresa:
            lanctos = Movtos_lancamentos.objects.filter(master_user=self.request.user.pk,
                                                        company=empresa).exclude(tipo_movto='C')
        else:
            lanctos = Movtos_lancamentos.objects.filter(master_user=self.request.user.pk).exclude(tipo_movto='C')


        if data_lanc_ini != '' and data_lanc_fim != '':
            dt_saldo_ant = data_lanc_ini_dt - timedelta(days=1)
            lanctos = lanctos.filter(dt_movimento__range=(data_lanc_ini_dt,data_lanc_fim_dt))
            if conta_finan:
                lanctos = lanctos.filter(conta_financeira=conta_finan)

            # SALDO ANTERIOR

            # creditos
            if empresa:
                movtos_creditos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                    sinal='R', dt_movimento__lt=data_lanc_ini_dt,
                                                                    company=empresa).exclude(tipo_movto='C')
            else:
                movtos_creditos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                    sinal='R', dt_movimento__lt=data_lanc_ini_dt).exclude(tipo_movto='C')
            if conta_finan:
                movtos_creditos = movtos_creditos.filter(conta_financeira=conta_finan)
            movtos_creditos = movtos_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))


            # debitos
            if empresa:
                movtos_debitos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                   sinal='D', dt_movimento__lt=data_lanc_ini_dt,
                                                                   company=empresa).exclude(tipo_movto='C')
            else:
                movtos_debitos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                   sinal='D', dt_movimento__lt=data_lanc_ini_dt).exclude(tipo_movto='C')

            if conta_finan:
                movtos_debitos = movtos_debitos.filter(conta_financeira=conta_finan)
            movtos_debitos = movtos_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

            if movtos_creditos['vlr_creditos'] is None:
                movtos_creditos['vlr_creditos'] = 0

            if movtos_debitos['vlr_debitos'] is None:
                movtos_debitos['vlr_debitos'] = 0

            saldo_anterior = Decimal(movtos_creditos['vlr_creditos']) - Decimal(movtos_debitos['vlr_debitos'])


            # SALDO ATUAL

            # creditos
            if empresa:
                movtos_creditos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                    sinal='R', dt_movimento__lte=data_lanc_fim_dt,
                                                                    company=empresa).exclude(tipo_movto='C')
            else:
                movtos_creditos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                    sinal='R', dt_movimento__lte=data_lanc_fim_dt).exclude(tipo_movto='C')
            if conta_finan:
                movtos_creditos = movtos_creditos.filter(conta_financeira=conta_finan)
            movtos_creditos = movtos_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))

            # debitos
            if empresa:
                movtos_debitos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                   sinal='D', dt_movimento__lte=data_lanc_fim_dt,
                                                                   company=empresa).exclude(tipo_movto='C')
            else:
                movtos_debitos = Movtos_lancamentos.objects.filter(master_user=self.request.user.user_master,
                                                                   sinal='D', dt_movimento__lte=data_lanc_fim_dt).exclude(tipo_movto='C')

            if conta_finan:
                movtos_debitos = movtos_debitos.filter(conta_financeira=conta_finan)
            movtos_debitos = movtos_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

            if movtos_creditos['vlr_creditos'] is None:
                movtos_creditos['vlr_creditos'] = 0

            if movtos_debitos['vlr_debitos'] is None:
                movtos_debitos['vlr_debitos'] = 0

            saldo_atual = Decimal(movtos_creditos['vlr_creditos']) - Decimal(movtos_debitos['vlr_debitos'])



            total_debitos = lanctos.filter(dt_movimento__range=(data_lanc_ini_dt, data_lanc_fim_dt),
                                              sinal='D')
            if conta_finan:
                total_debitos = total_debitos.filter(conta_financeira=conta_finan)
            total_debitos = total_debitos.aggregate(vlr_debitos=Sum('vlr_movimento'))

            total_creditos = lanctos.filter(dt_movimento__range=(data_lanc_ini_dt, data_lanc_fim_dt),
                                               sinal='R')
            if conta_finan:
                total_creditos = total_creditos.filter(conta_financeira=conta_finan)
            total_creditos = total_creditos.aggregate(vlr_creditos=Sum('vlr_movimento'))

            if total_creditos['vlr_creditos'] is None:
                total_creditos['vlr_creditos'] = 0

            if total_debitos['vlr_debitos'] is None:
                total_debitos['vlr_debitos'] = 0

            totalizador_cre = total_creditos['vlr_creditos']
            totalizador_deb = total_debitos['vlr_debitos']

            # TRATA LIMITE DA CONTA
            if conta_finan:
                if conta_finan_text.usa_limite:
                    vlr_limite = conta_finan_text.vlr_limite_text.replace('R$', '').replace('.', '').replace(',', '.')
                    saldo_c_limite = Decimal(saldo_atual) + Decimal(vlr_limite)

        context['lanctos'] = lanctos
        context['data_lanc_ini'] = data_lanc_ini
        context['data_lanc_fim'] = data_lanc_fim
        context['conta_finan'] = conta_finan_text
        context['dados_empresa'] = dados_empresa
        context['saldo_anterior'] = saldo_anterior
        context['dt_saldo_ant'] = dt_saldo_ant
        context['saldo_atual'] = saldo_atual
        context['total_debitos'] = totalizador_deb
        context['total_creditos'] = totalizador_cre
        context['dados_conta'] =  conta_finan_text
        context['saldo_c_limite'] = saldo_c_limite
        return context




class Rel_DRE(LoginRequiredMixin, PDFTemplateView):
     template_name = 'rel_demonstrativofinan.html'

     def get_context_data(self, **kwargs):
       context = super(Rel_DRE, self).get_context_data(**kwargs)
       data_lanc_ini = self.request.GET.get('data_lanc_ini','')
       data_lanc_fim = self.request.GET.get('data_lanc_fim','')
       empresa = self.request.GET.get('empresa','')
       f_lancamento = self.request.GET.get('f_lancamento','')
       f_vencimento = self.request.GET.get('f_vencimento', '')
       f_baixa = self.request.GET.get('f_baixa', '')


       dados_empresa = None
       tp_filtro = None
       user = self.request.user



       if data_lanc_ini != '':
           data_lanc_ini_dt = datetime.strptime(data_lanc_ini, "%d/%m/%Y").date()

       if data_lanc_fim != '':
           data_lanc_fim_dt = datetime.strptime(data_lanc_fim, "%d/%m/%Y").date()



       if empresa:
          dados_empresa = Company.objects.get(pk=int(empresa))

       if f_lancamento == 'on':
           f_lancamento = True
           tp_filtro = 'l'
       if f_vencimento == 'on':
           f_vencimento = True
           tp_filtro = 'v'
       if f_baixa == 'on':
           f_baixa = True
           tp_filtro = 'b'

       retorno_dre, retorno_planosdre, saldos = calc_dre(empresa, f_lancamento, f_vencimento, f_baixa, data_lanc_ini_dt,
                                                         data_lanc_fim_dt, user)



       context['data_lanc_ini'] = data_lanc_ini
       context['data_lanc_fim'] = data_lanc_fim
       context['retorno_dre'] = retorno_dre
       context['retorno_planosdre'] = retorno_planosdre
       context['saldo_contas_dre'] = saldos
       context['dados_empresa'] = dados_empresa
       context['tp_filtro'] = tp_filtro
       return context


class Rel_OS(LoginRequiredMixin, PDFTemplateView):

    def get_template_names(self):
        return ["rel_os_producao.html"]


    def get_form_kwargs(self):
        kwargs = super(Rel_OS, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Rel_OS, self).get_context_data(**kwargs)
        pk_os =  self.request.GET.get('pk','')
        ordem = OrdemServico.objects.get(pk=pk_os)
        prestador = User.objects.get(pk=ordem.prestador)

        context['ordem'] = ordem
        context['prestador'] = prestador
        return context


rel_os = Rel_OS.as_view()
rel_dre = Rel_DRE.as_view()
rel_lanfinanceiros = Rel_lanfinanceiros.as_view()
rel_extratofinanceiro = Rel_Extratofinanceiro.as_view()