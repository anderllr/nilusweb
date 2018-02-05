from django.shortcuts import render
from django.utils.dateparse import parse_date
from lancfinanceiros.models import Lancamentos,Movtos_lancamentos
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def rel_lanfinanceiros(request):

    # if request.is_ajax():
    #     template_name = '_table_lancfin.html'
    # else:
    template_name = 'rel_lanfinanceiros.html'

    filtrou = 'nao'

    if request.user.is_masteruser is True:
        lanctos = Lancamentos.objects.filter(master_user=request.user.pk)
    else:
        lanctos = Lancamentos.objects.filet(master_user=request.user.user_master)



    data_lanc_ini = request.GET.get('data_lanc_ini', '')
    data_lanc_fim = request.GET.get('data_lanc_fim', '')
    data_venc_ini = request.GET.get('data_venc_ini', '')
    data_venc_fim = request.GET.get('data_venc_fim', '')
    data_baix_ini = request.GET.get('data_baix_ini', '')
    data_baix_fim = request.GET.get('data_baix_fim', '')
    cadgeral = request.GET.get('cadgeral','')
    plano_finan = request.GET.get('plano_finan','')
    c_custo = request.GET.get('c_custo','')
    conta_finan = request.GET.get('conta_finan','')
    tipo_lancamento = request.GET.get('tipo_lancamento','T')
    sit_lancamento = request.GET.get('sit_lancamento','T')



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

    context = {
        'lanctos': lanctos,
        'data_venc_ini' : data_venc_ini,
        'data_venc_fim': data_venc_fim,
        'data_lanc_ini': data_lanc_ini,
        'data_lanc_fim': data_lanc_fim,
        'data_baix_ini' : data_baix_ini,
        'data_baix_fim': data_baix_fim,
        'cadgeral' : cadgeral,
        'plano_finan': plano_finan,
        'c_custo' : c_custo,
        'conta_finan' : conta_finan,
        'tipo_lancamento' : tipo_lancamento,
        'sit_lancamento' : sit_lancamento,
    }

    return render(request, template_name,context)


