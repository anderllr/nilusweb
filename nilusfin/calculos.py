from datetime import date, timedelta, datetime
from decimal import Decimal
from django.db.models import Sum
from niluscad.models import Company,Grupodre,PlanoFinan
from lancfinanceiros.models import Movtos_lancamentos,Lancamentos
from nilusfin.models import Contafinanceira



def calc_dre(empresa,f_lancamento,f_vencimento,f_baixa,data_lanc_ini,data_lanc_fim,user):

    saldos = []
    retorno_dre = []
    retorno_planosdre = []


    if empresa:
        lanctos = Lancamentos.objects.filter(master_user=user.user_master.pk, company=empresa)
    else:
        lanctos = Lancamentos.objects.filter(master_user=user.user_master.pk)



    if f_lancamento == True:
        lanctos = lanctos.filter(dt_lancamento__range=(data_lanc_ini, data_lanc_fim))
    if f_vencimento == True:
        lanctos = lanctos.filter(dt_vencimento__range=(data_lanc_ini, data_lanc_fim))
    if f_baixa == True:
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



def saldo_conta(empresa,contas,data_saldo,user):
    saldos = []
    print(contas)
    for c in contas:
        if empresa:
            movtos_creditos = Movtos_lancamentos.objects.filter(master_user=user.user_master,sinal='R'
                                                       ,dt_movimento__lte=data_saldo,conta_financeira=c,company=empresa
                                                       ).exclude(tipo_movto='C').aggregate(vlr=Sum('vlr_movimento'))

            print('movtos_credit')
            print(movtos_creditos)

            movtos_debitos =  Movtos_lancamentos.objects.filter(master_user=user.user_master,sinal='D'
                                                       ,dt_movimento__lte=data_saldo,conta_financeira=c,company=empresa
                                                       ).exclude(tipo_movto='C').aggregate(vlr=Sum('vlr_movimento'))

            print('movtos_debit')
            print(movtos_debitos)
        # else:
        #     movtos_creditos = Movtos_lancamentos.objects.filter(master_user=user.user_master, sinal='R'
        #                                         , dt_movimento__lte=data_saldo, conta_financeira=c
        #                                         ).exclude(tipo_movto='C').aggregate(vlr=Sum('vlr_movimento'))
        #
        #     print('movtos_credit')
        #     print(movtos_creditos)
        #
        #     movtos_debitos = Movtos_lancamentos.objects.filter(master_user=user.user_master, sinal='D'
        #                                         , dt_movimento__lte=data_saldo, conta_financeira=c,
        #                                         ).exclude(tipo_movto='C').aggregate(vlr=Sum('vlr_movimento'))
        #
        #     print('movtos_debit')
        #     print(movtos_debitos)


        if movtos_creditos['vlr'] is None:
            movtos_creditos['vlr'] = 0

        if movtos_debitos['vlr'] is None:
            movtos_debitos['vlr'] = 0

        saldo_conta = Decimal(movtos_creditos['vlr']) - Decimal(movtos_debitos['vlr'])

        if c.usa_limite:
            vlr_limite = c.vlr_limite
            saldo_final = Decimal(saldo_conta) + Decimal(vlr_limite)
        else:
            vlr_limite = 0
            saldo_final = saldo_conta

        saldos.append({"pk": c.pk ,"conta": c.descricao,"saldo" :saldo_conta,"vlr_limite" : vlr_limite,"saldo_final": saldo_final})


    return(saldos)


def lanctos_atraso(empresa,contas,data_saldo,user):


    if empresa:
        # TOTALIZADORES INICIO
        rec_atraso_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                    company=empresa,conta_finan__in=contas,
                                                    situacao=False,dt_vencimento__lt=data_saldo
                                                    ).aggregate(vlr_saldo=Sum('saldo'))

        desp_atraso_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                    company=empresa,conta_finan__in=contas,
                                                    situacao=False, dt_vencimento__lt=data_saldo
                                                    ).aggregate(vlr_saldo=Sum('saldo'))
        #///////// TOTALIZADORES FIM /////////////////////////

        # LANCAMENTOS DETALHE INICIO
        rec_atraso_lanc = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                    company=empresa,conta_finan__in=contas,
                                                     situacao=False,dt_vencimento__lt=data_saldo)

        desp_atraso_lanc = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                    company=empresa,conta_finan__in=contas,
                                                    situacao=False, dt_vencimento__lt=data_saldo
                                                    )
        # ///////////////////LANCAMENTOS DETALHE FIM ////////////////////////////

    else:
        # TOTALIZADORES INICIO
        rec_atraso_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                    conta_finan__in=contas,situacao=False,
                                                    dt_vencimento__lt=data_saldo).aggregate(vlr_saldo=Sum('saldo'))

        desp_atraso_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                     conta_finan__in=contas,situacao=False,
                                                     dt_vencimento__lt=data_saldo).aggregate(vlr_saldo=Sum('saldo'))
        # ///////// TOTALIZADORES FIM /////////////////////////

        # LANCAMENTOS DETALHE INICIO
        rec_atraso_lanc = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                     conta_finan__in=contas,situacao=False,
                                                     dt_vencimento__lt=data_saldo).order_by('dt_vencimento')

        desp_atraso_lanc = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                      conta_finan__in=contas,situacao=False,
                                                      dt_vencimento__lt=data_saldo).order_by('dt_vencimento')
        # ///////////////////LANCAMENTOS DETALHE FIM ////////////////////////////


    return(rec_atraso_lanc,rec_atraso_tot,desp_atraso_lanc,desp_atraso_tot)


def lanctos_avencer(empresa,contas,data_venc_ini,data_venc_fim,user):

    saldo_final = 0
    tot_acum = 0
    fluxo_dia = []

    if empresa:
        rec_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                    company=empresa,conta_finan__in=contas,
                                                    situacao=False,dt_vencimento__range=(data_venc_ini, data_venc_fim)
                                                    ).aggregate(vlr_saldo=Sum('saldo'))

        desp_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                    company=empresa,conta_finan__in=contas,
                                                    situacao=False, dt_vencimento__range=(data_venc_ini, data_venc_fim)
                                                    ).aggregate(vlr_saldo=Sum('saldo'))
        lanctos = Lancamentos.objects.filter(master_user=user.user_master,
                                                    company=empresa,conta_finan__in=contas,
                                                     situacao=False,dt_vencimento__range=(data_venc_ini, data_venc_fim)
                                             ).order_by('dt_vencimento')
    else:
        rec_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='R',
                                                    conta_finan__in=contas,situacao=False,
                                             dt_vencimento__range=(data_venc_ini, data_venc_fim)).aggregate(vlr_saldo=Sum('saldo'))

        desp_tot = Lancamentos.objects.filter(master_user=user.user_master, tipo_lancamento='D',
                                                     conta_finan__in=contas,situacao=False,
                                              dt_vencimento__range=(data_venc_ini, data_venc_fim)).aggregate(vlr_saldo=Sum('saldo'))

        lanctos = Lancamentos.objects.filter(master_user=user.user_master,
                                             conta_finan__in=contas,
                                             situacao=False, dt_vencimento__range=(data_venc_ini, data_venc_fim)
                                             ).order_by('dt_vencimento')


    contas_escolhidas = Contafinanceira.objects.filter(master_user=user.user_master,pk__in=contas)
    saldo_contas = saldo_conta(empresa,contas_escolhidas,data_venc_ini,user)

    for s in saldo_contas:
        saldo_final = saldo_final + Decimal(s['saldo_final'])

    tot_acum = saldo_final
    dias_fluxo = lanctos.values('dt_vencimento').distinct().order_by('dt_vencimento')

    for d in dias_fluxo:
        tot_rec_dia = lanctos.filter(dt_vencimento=d['dt_vencimento'],tipo_lancamento='R').aggregate(vlr_saldo=Sum('saldo'))
        tot_desp_dia = lanctos.filter(dt_vencimento=d['dt_vencimento'],tipo_lancamento='D').aggregate(vlr_saldo=Sum('saldo'))

        if tot_rec_dia['vlr_saldo'] is None:
            tot_rec_dia['vlr_saldo'] = 0

        if tot_desp_dia['vlr_saldo'] is None:
            tot_desp_dia['vlr_saldo'] = 0

        tot_dia = Decimal(tot_rec_dia['vlr_saldo']) - Decimal(tot_desp_dia['vlr_saldo'])
        tot_acum = tot_acum + tot_dia

        if tot_acum is None:
            tot_acum = 0

        fluxo_dia.append({"data": d['dt_vencimento'] ,"tot_rec_dia": tot_rec_dia,"tot_desp_dia" :tot_desp_dia, "tot_dia" : tot_dia,"tot_acum": tot_acum})




    return(rec_tot,desp_tot,fluxo_dia,lanctos,tot_acum)




