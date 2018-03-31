from datetime import date, timedelta, datetime
from decimal import Decimal
from django.db.models import Sum
from niluscad.models import Company,Grupodre,PlanoFinan
from lancfinanceiros.models import Movtos_lancamentos,Lancamentos



def calc_dre(empresa,f_lancamento,f_vencimento,f_baixa,data_lanc_ini,data_lanc_fim,request):

    saldos = []
    retorno_dre = []
    retorno_planosdre = []


    if empresa:
        lanctos = Lancamentos.objects.filter(master_user=request.user.user_master, company=empresa)
    else:
        lanctos = Lancamentos.objects.filter(master_user=request.user.user_master)

    if f_lancamento:
        lanctos = lanctos.filter(dt_lancamento__range=(data_lanc_ini, data_lanc_fim))
    if f_vencimento:
        lanctos = lanctos.filter(dt_vencimento__range=(data_lanc_ini, data_lanc_fim))
    if f_baixa:
        lanctos = lanctos.filter(data_baixa__range=(data_lanc_ini, data_lanc_fim))

    soma_grupodre = lanctos.values('plr_financeiro__grupodre__descricao', 'plr_financeiro__grupodre__sinal',
                                   'plr_financeiro__grupodre__pk').annotate(vlr_lancamentos=Sum('vlr_lancamento'))
    soma_grupodre = soma_grupodre.order_by('plr_financeiro__grupodre__ordem')

    for s in soma_grupodre:
        retorno_dre.append(s)
        vlr_planofinan = lanctos.filter(plr_financeiro__grupodre=s['plr_financeiro__grupodre__pk'])
        vlr_planofinan = vlr_planofinan.values('plr_financeiro__descricao', 'plr_financeiro__grupodre__pk').annotate(
            vlr_lancamento=Sum('vlr_lancamento'))

        for p in vlr_planofinan:
            retorno_planosdre.append(p)

        if not saldos:
            if s['plr_financeiro__grupodre__sinal'] == '-':
                vlr_plano = Decimal(s['vlr_lancamentos']) * -1
            else:
                vlr_plano = Decimal(s['vlr_lancamentos'])
            saldos.append({"pk": s['plr_financeiro__grupodre__pk'], "vlr_saldo": s['vlr_lancamentos']})
        else:
            if s['plr_financeiro__grupodre__sinal'] == '-':
                vlr_plano = vlr_plano - Decimal(s['vlr_lancamentos'])
            else:
                vlr_plano = vlr_plano + Decimal(s['vlr_lancamentos'])
            saldos.append({"pk": s['plr_financeiro__grupodre__pk'], "vlr_saldo": vlr_plano})

    return(retorno_dre,retorno_planosdre,saldos)