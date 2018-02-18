from django.shortcuts import render
from django.utils.dateparse import parse_date
from lancfinanceiros.models import Lancamentos,Movtos_lancamentos
from niluscad.models import Cadgeral,PlanoFinan,Ccusto
from nilusfin.models import Contafinanceira
from datetime import date, timedelta, datetime
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from easy_pdf.views import PDFTemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# @login_required
# def rel_lanfinanceiros(request):
#
#     # if request.is_ajax():
#     #     template_name = '_table_lancfin.html'
#     # else:
#     template_name = 'rel_lanfinanceiros.html'
#
#     filtrou = 'nao'
#
#     if request.user.is_masteruser is True:
#         lanctos = Lancamentos.objects.filter(master_user=request.user.pk)
#     else:
#         lanctos = Lancamentos.objects.filet(master_user=request.user.user_master)
#
#
#
#     data_lanc_ini = request.GET.get('data_lanc_ini', '')
#     data_lanc_fim = request.GET.get('data_lanc_fim', '')
#     data_venc_ini = request.GET.get('data_venc_ini', '')
#     data_venc_fim = request.GET.get('data_venc_fim', '')
#     data_baix_ini = request.GET.get('data_baix_ini', '')
#     data_baix_fim = request.GET.get('data_baix_fim', '')
#     cadgeral = request.GET.get('cadgeral','')
#     plano_finan = request.GET.get('plano_finan','')
#     c_custo = request.GET.get('c_custo','')
#     conta_finan = request.GET.get('conta_finan','')
#     tipo_lancamento = request.GET.get('tipo_lancamento','T')
#     sit_lancamento = request.GET.get('sit_lancamento','T')
#
#
#
#     if data_venc_ini != '':
#         data_venc_ini_dt = datetime.strptime(data_venc_ini, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(dt_vencimento__gte=data_venc_ini_dt)
#
#     if data_venc_fim != '':
#         data_venc_fim_dt = datetime.strptime(data_venc_fim, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(dt_vencimento__lt=data_venc_fim_dt + timedelta(days=1))
#
#     if data_lanc_ini != '':
#         data_lanc_ini_dt = datetime.strptime(data_lanc_ini, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(dt_lancamento__gte=data_lanc_ini_dt)
#
#     if data_lanc_fim != '':
#         data_lanc_fim_dt = datetime.strptime(data_lanc_fim, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(dt_lancamento__lt=data_lanc_fim_dt + timedelta(days=1))
#
#     if data_baix_ini != '':
#         data_baix_ini_dt = datetime.strptime(data_baix_ini, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(data_baixa__gte=data_baix_ini_dt)
#
#     if data_baix_fim != '':
#         data_baix_fim_dt = datetime.strptime(data_baix_fim, "%d/%m/%Y").date()
#         lanctos = lanctos.filter(data_baixa__lt=data_baix_fim_dt + timedelta(days=1))
#
#     # if empresa:
#     #     lanctos = lanctos.filter(company=empresa)
#     #     filtrou = 'ok'
#
#     if cadgeral != '':
#         lanctos = lanctos.filter(cadgeral=cadgeral)
#
#     if plano_finan != '':
#         lanctos = lanctos.filter(plr_financeiro=plano_finan)
#
#     if c_custo != '':
#         lanctos = lanctos.filter(c_custo=c_custo)
#
#     if conta_finan != '':
#         lanctos = lanctos.filter(conta_finan=conta_finan)
#
#     if tipo_lancamento != 'T':
#         lanctos = lanctos.filter(tipo_lancamento=tipo_lancamento)
#
#     if sit_lancamento != 'T':
#         if sit_lancamento == 'A':
#             lanctos = lanctos.filter(situacao=False)
#         elif sit_lancamento == 'B':
#             lanctos = lanctos.filter(situacao=True)
#
#     context = {
#         'lanctos': lanctos,
#         'data_venc_ini' : data_venc_ini,
#         'data_venc_fim': data_venc_fim,
#         'data_lanc_ini': data_lanc_ini,
#         'data_lanc_fim': data_lanc_fim,
#         'data_baix_ini' : data_baix_ini,
#         'data_baix_fim': data_baix_fim,
#         'cadgeral' : cadgeral,
#         'plano_finan': plano_finan,
#         'c_custo' : c_custo,
#         'conta_finan' : conta_finan,
#         'tipo_lancamento' : tipo_lancamento,
#         'sit_lancamento' : sit_lancamento,
#     }
#
#     return render(request, template_name,context)



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

        print(cadgeral_text)

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




rel_lanfinanceiros = Rel_lanfinanceiros.as_view()
